
import os
import streamlit as st
from src.infrastructure import pageConfig, backendHealthCheck
from src.domain import footer
import requests
import pandas as pd
import plotly.graph_objects as go

footer.hide_footer(st)
pageConfig.set_env_vars()
backend_url = os.environ['backend']

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
        model_names_response = requests.get(backend_url + "modelNames")
        if model_names_response.status_code == 200:
            model_names = model_names_response.json()
            if model_names:
                selected_model = st.selectbox("Select a model", model_names)
                step_3 = True
            else:
                st.write("No model found")
                step_3 = False
        else:
            st.error(
                "Failed to fetch model names:" +
                f" {model_names_response.status_code}")
            step_3 = False
    except Exception as e:
        step_3 = False
        st.error(f"An error occurred: {str(e)}")

if step_3 and selected_model:
    model_data_response = requests.post(
        backend_url + "modelData", params={'key': selected_model})

    if model_data_response.status_code == 200:
        model_data = model_data_response.json()
        # st.write("Model Data:")
        # st.json(model_data)  # Display the JSON data in a nice format
        # Convert 'valid_df' to DataFrame
        valid_df = pd.DataFrame(model_data["valid_df"])

        # Convert 'pred_df' to DataFrame
        pred_df = pd.read_json(model_data["pred_df"])
        if 'item_id' in valid_df.columns:
            item_ids = valid_df['item_id'].unique()
            selected_item_id = st.selectbox("Select an item ID", item_ids)
        else:
            st.error("Item ID column not found in the DataFrame.")
        step_4 = True
    else:
        step_4 = False
        st.error(
            f"Failed to fetch data for model {selected_model}:" +
            f"{model_data_response.status_code}")


def plot_item_predictions(item_id, valid_df, pred_df):
    # Filter for the selected item_id
    valid_item_df = valid_df[valid_df['item_id'] == item_id]
    pred_item_df = pred_df[pred_df['item_id'] == item_id]

    # Assuming the structure of your DataFrame is
    # consistent with the columns provided
    # Extract date columns (d_XXXX)
    date_columns = [col for col in valid_item_df if col.startswith('d_')]

    # Convert wide format to long format for easier plotting
    valid_long = pd.melt(valid_item_df, id_vars=[
                         'item_id'],
                         value_vars=date_columns,
                         var_name='date',
                         value_name='actual')
    pred_long = pd.melt(pred_item_df, id_vars=[
                        'item_id'], value_vars=date_columns,
                        var_name='date',
                        value_name='prediction')

    # Create plot
    fig = go.Figure()

    # Add actual sales trace
    fig.add_trace(go.Scatter(
        x=valid_long['date'], y=valid_long['actual'],
        mode='lines+markers', name='Actual'))

    # Add predicted sales trace
    fig.add_trace(go.Scatter(
        x=pred_long['date'], y=pred_long['prediction'],
        mode='lines+markers', name='Prediction'))

    # Update layout
    fig.update_layout(title=f'Actual vs Predicted Sales for Item {item_id}',
                      xaxis_title='Date', yaxis_title='Sales',
                      margin=dict(l=20, r=20, t=30, b=20))

    return fig


if step_4:
    # Plot and display
    fig = plot_item_predictions(selected_item_id, valid_df, pred_df)
    st.plotly_chart(fig)
