"""API for LLM Script Tools."""
from __future__ import annotations

from homeassistant.components.homeassistant import async_should_expose
from homeassistant.components.script import DOMAIN as SCRIPT_DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import llm, device_registry, area_registry, entity_registry
from homeassistant.helpers.llm import ScriptTool, Tool

from .const import (
    DOMAIN, 
    CONF_LLM_LABEL, 
    CONF_USE_LABEL_FILTER, 
    CONF_PROMPT,
    DEFAULT_LLM_LABEL, 
    DEFAULT_USE_LABEL_FILTER,
    DEFAULT_PROMPT
)

class LlmScriptToolsAPI(llm.API):
    """API that exposes HA scripts as LLM tools."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Init the class."""
        super().__init__(
            hass=hass,
            id=DOMAIN,
            name="LLM Script Tools",
        )
        self.entry = entry

    async def async_get_api_instance(self, llm_context: llm.LLMContext) -> llm.APIInstance:
        """Return the instance of the API."""
        tools = self._async_get_tools(llm_context)
        location_prompt = self._get_location_prompt(llm_context)
        
        prompt = self._async_get_api_prompt(tools, location_prompt)

        return llm.APIInstance(
            api=self,
            api_prompt=prompt,
            llm_context=llm_context,
            tools=tools,
        )

    @callback
    def _get_location_prompt(self, llm_context: llm.LLMContext) -> str:
        """Determine the user's location based on the device ID."""
        if not llm_context.device_id:
            return ""

        dev_reg = device_registry.async_get(self.hass)
        area_reg = area_registry.async_get(self.hass)

        device = dev_reg.async_get(llm_context.device_id)
        if not device or not device.area_id:
            return ""

        area = area_reg.async_get_area(device.area_id)
        if not area:
            return ""

        return f"Current Location: {area.name}"

    @callback
    def _async_get_tools(self, llm_context: llm.LLMContext) -> list[Tool]:
        """Return a list of ScriptTools."""
        tools: list[Tool] = []
        scripts = self.hass.states.async_all(SCRIPT_DOMAIN)
        
        ent_reg = entity_registry.async_get(self.hass)
        assistant_id = llm_context.assistant or "conversation"

        # Читаем настройки
        use_filter = self.entry.options.get(CONF_USE_LABEL_FILTER, DEFAULT_USE_LABEL_FILTER)
        target_label = self.entry.options.get(CONF_LLM_LABEL, DEFAULT_LLM_LABEL)

        for script_state in scripts:
            entity_id = script_state.entity_id

            if not async_should_expose(self.hass, assistant_id, entity_id):
                continue

            if use_filter:
                entry = ent_reg.async_get(entity_id)
                # Если записи нет или лейбла нет - пропускаем
                if not entry or target_label not in entry.labels:
                    continue

            tools.append(ScriptTool(self.hass, entity_id))

        return tools

    @callback
    def _async_get_api_prompt(self, tools: list[Tool], location_info: str) -> str:
        """Return the prompt for the API."""
        
        # Получаем базовый промпт из настроек
        base_prompt = self.entry.options.get(CONF_PROMPT, DEFAULT_PROMPT)

        if not tools:
            target_label = self.entry.options.get(CONF_LLM_LABEL, DEFAULT_LLM_LABEL)
            return f"You have no scripts labeled '{target_label}' available."

        location_section = f"\n{location_info}\n" if location_info else ""

        return f"{base_prompt}\n{location_section}"
