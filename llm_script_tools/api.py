"""API for LLM Script Tools."""
from __future__ import annotations

from homeassistant.components.homeassistant import async_should_expose
from homeassistant.components.script import DOMAIN as SCRIPT_DOMAIN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import llm, device_registry, area_registry
from homeassistant.helpers.llm import ScriptTool, Tool

from .const import DOMAIN

class LlmScriptToolsAPI(llm.API):
    """API that exposes HA scripts as LLM tools."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Init the class."""
        super().__init__(
            hass=hass,
            id=DOMAIN,
            name="LLM Script Tools",
        )

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
        
        assistant_id = llm_context.assistant or "conversation"

        for script_state in scripts:
            if not async_should_expose(self.hass, assistant_id, script_state.entity_id):
                continue

            tools.append(ScriptTool(self.hass, script_state.entity_id))

        return tools

    @callback
    def _async_get_api_prompt(self, tools: list[Tool], location_info: str) -> str:
        """Return the prompt for the API."""
        if not tools:
            return "You have no scripts exposed."

        script_names = [f"- {tool.name}: {tool.description or 'No description'}" for tool in tools]
        script_list_str = "\n".join(script_names)

        location_section = f"\n{location_info}\n" if location_info else ""

        return (
            "## Scripts Capabilities\n"
            "You have access to the following Home Assistant scripts to control the environment.\n"
            "Use these tools ONLY if the user's request clearly implies executing one of them.\n"
            "If no script matches the request, continue the conversation according to your persona without calling any tools.\n"
            f"{location_section}"
            "\n"
            "Available Scripts:\n"
            f"{script_list_str}"
        )
