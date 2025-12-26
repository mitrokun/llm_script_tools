"""Config flow for LLM Script Tools."""
from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant.config_entries import (
    ConfigFlow,
    ConfigFlowResult,
    ConfigEntry,
    OptionsFlowWithConfigEntry,
)
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    BooleanSelector,
    TextSelector,
    TemplateSelector,
)

from .const import (
    DOMAIN,
    CONF_LLM_LABEL,
    CONF_USE_LABEL_FILTER,
    CONF_PROMPT,
    DEFAULT_LLM_LABEL,
    DEFAULT_USE_LABEL_FILTER,
    DEFAULT_PROMPT,
)

class LlmScriptToolsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for LLM Script Tools."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlowWithConfigEntry:
        """Create the options flow."""
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


class LlmScriptToolsOptionsFlow(OptionsFlowWithConfigEntry):
    """Handle options flow."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # self.config_entry теперь доступен автоматически благодаря OptionsFlowWithConfigEntry
        # Читаем текущие настройки или берем дефолтные
        current_filter = self.options.get(
            CONF_USE_LABEL_FILTER, DEFAULT_USE_LABEL_FILTER
        )
        current_label = self.options.get(
            CONF_LLM_LABEL, DEFAULT_LLM_LABEL
        )
        current_prompt = self.options.get(
            CONF_PROMPT, DEFAULT_PROMPT
        )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_PROMPT, 
                        default=current_prompt
                    ): TemplateSelector(),
                    vol.Required(
                        CONF_USE_LABEL_FILTER, 
                        default=current_filter
                    ): BooleanSelector(),
                    vol.Optional(
                        CONF_LLM_LABEL, 
                        default=current_label
                    ): TextSelector(),
                }
            ),
        )