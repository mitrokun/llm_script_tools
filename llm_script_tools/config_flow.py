"""Config flow for LLM Script Tools."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback

from .const import DOMAIN

class LlmScriptToolsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for LLM Script Tools."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return LlmScriptToolsOptionsFlow(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial setup step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="LLM Script Tools", data={})

        return self.async_show_form(step_id="user")


class LlmScriptToolsOptionsFlow(OptionsFlow):
    """Handle options flow."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init")