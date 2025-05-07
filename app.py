from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
<<<<<<< HEAD
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://jylstheproducer.github.io"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})  # Configuration CORS spécifique pour GitHub Pages
=======
>>>>>>> 755b96a9659ed07ba1d87cc6c8c71b1b1a051945

# Autoriser uniquement le frontend sur GitHub Pages
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://jylstheproducer.github.io"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Clé API Hugging Face depuis variable d'environnement
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "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")

def ask_huggingface(question):
    url = "https://api-inference.huggingface.co/models/google/flan-t5-small"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
    }
    payload = {"inputs": question}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        result = response.json()

        if isinstance(result, list):
            return result[0].get("generated_text", "Aucune réponse générée.")
        elif "error" in result:
            # Gestion du temps de chargement du modèle
            if "estimated_time" in result:
                return f"Le modèle se charge. Veuillez patienter environ {result['estimated_time']:.1f} secondes."
            return "Erreur du modèle : " + result["error"]
        else:
            return result.get("generated_text", "Format de réponse inattendu.")
    except Exception as e:
        print(f"Erreur Hugging Face : {str(e)}")
        return "Je suis désolé, une erreur est survenue lors de la connexion au modèle."

# Route API principale
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"status": "error", "response": "Message vide."}), 400

    bot_response = ask_huggingface(message)
    return jsonify({"status": "success", "response": bot_response})

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
<<<<<<< HEAD
        port=int(os.environ.get("PORT", 10000)),  # More deployment-friendly
        debug=False  # Important for production
    )
=======
        port=int(os.environ.get("PORT", 10000)),
        debug=False
    )

>>>>>>> 755b96a9659ed07ba1d87cc6c8c71b1b1a051945
