"""Constants for the LLM Script Tools integration."""

DOMAIN = "llm_script_tools"

# Keys
CONF_LLM_LABEL = "llm_label"
CONF_USE_LABEL_FILTER = "use_label_filter"
CONF_PROMPT = "prompt"

# Defaults
DEFAULT_LLM_LABEL = "llm"
DEFAULT_USE_LABEL_FILTER = True
DEFAULT_PROMPT = (
    "## Scripts Capabilities\n"
    "You have access to Home Assistant scripts (tools).\n"
    "Rules:\n"
    "1. Call a tool ONLY if the request clearly implies it. Otherwise, reply as your persona.\n"
    "2. If 'Current Location' is set, prioritize local scripts. Do NOT control other rooms unless explicitly named.\n"
    "3. AFTER calling a tool, switch to 'Robot Mode': be extremely dry and technical. Maximum 5 words."
)
