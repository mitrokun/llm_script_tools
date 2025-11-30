"""API for LLM Script Tools."""
from __future__ import annotations

from homeassistant.components.homeassistant import async_should_expose
from homeassistant.components.script import DOMAIN as SCRIPT_DOMAIN
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import llm
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
        prompt = self._async_get_api_prompt(tools)

        return llm.APIInstance(
            api=self,
            api_prompt=prompt,
            llm_context=llm_context,
            tools=tools,
        )

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
    def _async_get_api_prompt(self, tools: list[Tool]) -> str:
        """Return the prompt for the API."""
        if not tools:
            return "You have no scripts exposed. Tell the user to expose scripts to Assist."

        script_names = [f"- {tool.name}: {tool.description or 'No description'}" for tool in tools]
        script_list_str = "\n".join(script_names)

        return (
            "## Scripts Capabilities\n"
            "You have access to the following Home Assistant scripts to control the environment.\n"
            "Use these tools ONLY if the user's request clearly implies executing one of them.\n"
            "If no script matches the request, continue the conversation according to your persona without calling any tools.\n"
            "\n" 
            "Available Scripts:\n"
            f"{script_list_str}"
        )