import openai
import json
import os
from dotenv import load_dotenv
import pickle
import sklearn_xarray
import pmdarima
import joblib 

# load .env file
load_dotenv()
openai.api_key = os.getenv('API_KEY')


# Load (deserialize) the model from the file
# with open("arima_model.pkl", "rb") as file:
#     model = pickle.load(file)

model = joblib.load("arma_model.joblib")

#function for calling model that returns time-series prediction
def forecast_model (start_date, end_date, latitude, longitude):
   return model.predict(17)

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
#chat_with_model()
print(forecast_model('2024-10-30', '2024-12-30', 39.0968, -120.0324))

