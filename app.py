from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# Configuration CORS autorisant GitHub Pages uniquement
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://jylstheproducer.github.io"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

HUGGINGFACE_API_TOKEN = "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"

def ask_huggingface(question):
    url = "https://api-inference.huggingface.co/models/google/flan-t5-small"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    payload = {
        "inputs": question
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()

        if isinstance(result, list):
            return result[0].get("generated_text", "No answer found")
        elif isinstance(result, dict):
            if "error" in result:
                return f"Model is loading: {result.get('estimated_time', 0):.1f}s remaining"
            return result.get("generated_text", "No answer found")
        return "Unexpected response format"
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Je suis désolé, une erreur est survenue."

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200  # Répondre aux requêtes de preflight

    data = request.get_json()
    message = data.get("message", "")
    if not message:
        return jsonify({"status": "error", "response": "Message vide."}), 400

    bot_response = ask_huggingface(message)
    return jsonify({"status": "success", "response": bot_response})

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 10000)),
        debug=False
    )

