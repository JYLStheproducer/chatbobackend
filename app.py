from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os  # Added for potential environment variable usage

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://jylstheproducer.github.io"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})  # Configuration CORS spécifique pour GitHub Pages

# Fix 1: Added quotes around the API token
HUGGINGFACE_API_TOKEN = "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"

def ask_huggingface(question):
    # Fix 2: Renamed variable 'u' to 'url' for clarity
    url = "https://api-inference.huggingface.co/models/google/flan-t5-small"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    payload = {
        "inputs": question
    }
    # Fix 3: Use correct variable name 'url'
    response = requests.post(url, headers=headers, json=payload)
    
    try:
        # Improved error handling
        result = response.json()
        
        # Handle different response formats
        if isinstance(result, list):
            return result[0].get("generated_text", "No answer found")
        elif isinstance(result, dict):
            if "error" in result:
                return f"Model is loading: {result['estimated_time']:.1f}s remaining"
            return result.get("generated_text", "No answer found")
        return "Unexpected response format"
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Je suis désolé, une erreur est survenue."

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    if not message:
        return jsonify({"status": "error", "response": "Message vide."}), 400
    
    bot_response = ask_huggingface(message)
    return jsonify({"status": "success", "response": bot_response})

# Improved deployment settings
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 10000)),  # More deployment-friendly
        debug=False  # Important for production
    )
