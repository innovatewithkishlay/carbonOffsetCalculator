from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
import certifi

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Load API key from .env file
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta2/models/gemini-pro:generateMessage"

@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Get user input from the request
    user_input = request.json.get("prompt")
    if not user_input:
        return jsonify({"error": "No prompt provided"}), 400

    # Prepare the request to the Gemini API
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {"prompt": {"text": user_input}}

    try:
        # Send the request to the Gemini API
        response = requests.post(GEMINI_URL, headers=headers, json=data, params=params, verify=certifi.where())
        response_data = response.json()

        # Check if the response is valid
        if response.status_code == 200 and "candidates" in response_data:
            bot_reply = response_data["candidates"][0]["content"]
            return jsonify({"reply": bot_reply}), 200
        else:
            return jsonify({"error": "Unexpected response format", "details": response_data}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)