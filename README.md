# llm_script_tools
Grant the Home Assistant conversation agent access only to scripts (as tools).

Copy the integration directory to custom_components, restart, add the `LLM Script Tools` integration, and select the new item in the conversation settings.

<img width="237" height="138" alt="image" src="https://github.com/user-attachments/assets/148c18c0-abae-42d6-8d5b-89b902dc785a" />

By default, additional script filtering is enabled using the `LLM` label, which allows you to separate scripts for the built-in local handler (exposed for assist) and tools provided for llm (exposed + label).

<img width="579" height="171" alt="image" src="https://github.com/user-attachments/assets/60fc5985-8df0-422c-9dc8-3d53fb352dc7" />

You can disable this in the settings. You can also configure a script prompt in the settings, that will be added to the main prompt.
