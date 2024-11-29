from flask import Flask, render_template, request, jsonify
import openai
import json
import os
from dotenv import load_dotenv

# Load secret .env file
load_dotenv()
openai.api_key = os.getenv('API_KEY')

app = Flask(__name__)

def forecast_model(start_date, end_date, latitude, longitude):
    # Dummy implementation of the forecast model function
    return f"Forecast from {start_date} to {end_date} at ({latitude}, {longitude})"

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
            
            return jsonify({"response": f"Function Result: {result}"})
        
        return jsonify({"response": assistant_message['content']})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)