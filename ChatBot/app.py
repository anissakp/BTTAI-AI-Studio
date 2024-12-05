from flask import Flask, render_template, request, jsonify
import openai
import json
import os
from dotenv import load_dotenv
import xarray as xr
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import io
import base64

# Load secret .env file
load_dotenv()
openai.api_key = os.getenv('API_KEY')

app = Flask(__name__)

# load the model
loaded_model = tf.keras.models.load_model('lstm_model.h5')

# load the test input, used to do the prediction 
loaded_test_input = np.load('test_input.npy')
loaded_train_y_input = np.load('y_train.npy')
# the chlorophyll subset
loaded_chl_subset = xr.open_dataarray('chl_subset.nc')

scaler_y = MinMaxScaler(feature_range=(0, 1))
y_train_scaled = scaler_y.fit_transform(loaded_train_y_input.reshape(-1, 1))

def forecast_model(start_date, end_date, latitude, longitude):
    current_input = loaded_test_input
    n_future_steps = 4
    future_predictions = []
    for _ in range(n_future_steps):
        # Predict the next timestep
        pred = loaded_model.predict(current_input)
    
        # Append the prediction to the list
        future_predictions.append(pred)
    
        # Update the input sequence: add the prediction and remove the oldest timestep
        current_input = np.append(current_input[:, 1:, :], pred.reshape(1, 1, -1), axis=1)

    # Combine all predictions
    future_predictions = np.array(future_predictions)
    # print(future_predictions.shape)
    # print(future_predictions)

    future_predictions = scaler_y.inverse_transform(future_predictions.reshape(-1, 1))
    future_predictions = future_predictions.reshape(n_future_steps, -1)
    print(future_predictions)
    print(future_predictions.shape)

    # Select a timestep to visualize (e.g., the first timestep in the test set)
    # Select a timestep to visualize (e.g., the first timestep in the test set)
    timestep = 0

    predictions = future_predictions.reshape((future_predictions.shape[0], loaded_chl_subset.shape[1], loaded_chl_subset.shape[2]))
    # Extract the data for the selected timestep
    y_pred_timestep = predictions[timestep]

    # Extract the actual coordinates
    x_coords = loaded_chl_subset.coords['x'].values
    y_coords = loaded_chl_subset.coords['y'].values

    # Create the visualization
    plt.figure(figsize=(8, 6))
    plt.pcolormesh(x_coords, y_coords, y_pred_timestep, cmap='viridis', shading='auto')
    plt.colorbar(label='Chlorophyll Value')
    plt.title(f'Predicted Chlorophyll Values at Timestep {timestep}')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    # Save the plot to an in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Convert the buffer to a base64-encoded string
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Return the base64-encoded string
    return img_base64


tools = [
    {
        "type": "function",
        "function": {
            "name": "forecast_model",
            "description": "Get the water indices forecast from the model.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "Start date in YYYY-MM-DD format."},
                    "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format."},
                    "latitude": {"type": "number", "description": "Latitude of location."},
                    "longitude": {"type": "number", "description": "Longitude of location."}
                },
                "required": ["start_date", "end_date", "latitude", "longitude"]
            },
        }
    }
]

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    try:
        user_input = request.form.get("msg")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        messages = [
            {"role": "system", "content": "You are a helpful assistant that can create time-series forecast graphs for water quality of water bodies."},
            {"role": "user", "content": user_input}
        ]

        # Call OpenAI API with function calling
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use a supported model
            messages=messages,
            tools=tools
        )

        assistant_message = response['choices'][0]['message']

        # Check if a tool call was made
        if 'tool_calls' in assistant_message and assistant_message['tool_calls']:
            tool_call = assistant_message['tool_calls'][0]
            arguments = json.loads(tool_call['function']['arguments'])

            start_date = arguments.get('start_date')
            end_date = arguments.get('end_date')
            latitude = arguments.get('latitude')
            longitude = arguments.get('longitude')

            # Call the local function to generate the graph
            result = forecast_model(start_date, end_date, latitude, longitude)
            
            #return jsonify({"response": f"Function Result: {result}"})
            return jsonify({"message": assistant_message['content'], "image": result})
        
        return jsonify({"response": assistant_message['content']})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)