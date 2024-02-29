
import os
import streamlit as st
from src.infrastructure import pageConfig, backendHealthCheck
from src.domain import footer
import requests

backend_url = os.environ['backend']

footer.hide_footer(st)
pageConfig.set_env_vars()

step_1, step_2, step_3, step_4 = False, False, False, False

# Step 1 Background health check
# st.write("Let's make sure our backend is running")
backendHealthCheck.add_health_check_button(st,
                                           backend_url=backend_url)
step_1 = backendHealthCheck.health_check(backend_url=backend_url)

if step_1:
    # Fetch the model config
    config_response = requests.get(backend_url+'modelLevelConfig')
    # Check if the request was successful
    if config_response.status_code == 200:
        # Parse the JSON response
        config_response_json = config_response.json()
        # Display the response data
        st.write("Current backend running at this config")

        st.write(f"Model Level - {config_response_json['model_level']}")
        st.write(f"Training Epochs - {config_response_json['epochs']}")
        step_2 = True
    else:
        step_2 = False
        st.error(
            f"""Error: {config_response.status_code}
             - Failed to fetch config from API.""")

# Now let's fetch the model dropdown
if step_2:
    try:
        step_3 = True

    except Exception as e:
        step_3 = False
        raise e

if step_3:
    try:
        step_4 = True
    except Exception as e:
        step_4 = False
        raise e
