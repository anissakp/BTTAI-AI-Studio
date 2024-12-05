import openai
import json
import os
from dotenv import load_dotenv
import xarray as xr
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# load .env file
load_dotenv()
openai.api_key = os.getenv('API_KEY')


# Load (deserialize) the model from the file
# with open("arima_model.pkl", "rb") as file:
#     model = pickle.load(file)

#model = joblib.load("arma_model.joblib")

#function for calling model that returns time-series prediction

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
    plt.show()

    # dummy implementation of the forecast model function
    #return f"Forecast from {start_date} to {end_date} at ({latitude}, {longitude})"


tools = [
    {
        "type": "function",
        "function": {
            "name": "forecast_model",
            "description": "Get the water indices forecast from the model. Call this whenever you need to know the time-series forecast, for example when a customer asks 'What is the water quality in Lake Tahoe from '2024-10-30' to '2024-12-30'",
            "parameters": {
                "type": "object",
                "properties": {
                   "start_date": {
                        "type": "string",
                        "description": "The start date for the data timeframe in YYYY-MM-DD format."
                    },
                    "end_date": {
                        "type": "string",
                        "description": "The end date for the data timeframe in YYYY-MM-DD format."
                    },
                    "latitude": {
                        "type": "number",
                        "description": "The latitude of the water body location."
                    },
                    "longitude": {
                        "type": "number",
                        "description": "The longitude of the water body location."
                    }
        },
        "required": ["start_date", "end_date", "latitude", "longitude"]
            },
        }
    }
]


def chat_with_model():
    # start an empty message history
    messages = [
        {"role": "system", "content": "You are a helpful assistant that can create time-series forecast graphs for water quality of water bodies."}
    ]

    while True:
        # get user input
        user_input = input("User: ")
        messages.append({"role": "user", "content": user_input})

        # call OpenAI API with function calling
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )

        # extract the assistant's response and check if there's a function call
        assistant_message = response.choices[0].message
        messages.append(assistant_message)

        # check if a function call was made
        if assistant_message.tool_calls:
                tool_call = response.choices[0].message.tool_calls[0]
                arguments = json.loads(tool_call.function.arguments)

                start_date = arguments.get('start_date')
                end_date = arguments.get('end_date')
                latitude = arguments.get('latitude')
                longitude = arguments.get('longitude')
                
                # call the local function to generate the graph
                result = forecast_model(start_date, end_date, latitude, longitude)

                # add the function result as a message in the chat history
                messages.append({"role": "function", "name": "forecast_model", "content": result})
                print(f"Assistant (Function Result): {result}")
                break
        else:
                # print the assistant's text response
                print(f"Assistant: {assistant_message.content}")

# run the chat
chat_with_model()
#print(forecast_model('2024-10-30', '2024-12-30', 39.0968, -120.0324))

