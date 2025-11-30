# llm_script_tools
Grant the Home Assistant conversation agent access only to scripts (as tools).

Copy the integration directory to custom_components, restart, add the `LLM Script Tools` integration, and select the new item in the conversation settings.

<img width="237" height="138" alt="image" src="https://github.com/user-attachments/assets/148c18c0-abae-42d6-8d5b-89b902dc785a" />

In `api.py`, you can adjust the prompt for scripts, which will be added to the main prompt.
