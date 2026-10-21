
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:3b"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_reply():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    prompt = f"""
    You are LazyReply AI.
    Write a short, polite, natural reply to the message below.
    Return only the reply. Do not explain it.

    Message: {message}
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        reply = response.json().get("response", "").strip()

        return jsonify({"reply": reply})

    except requests.RequestException:
        return jsonify({
            "error": "Cannot connect to Ollama. Check that Ollama is running and the model is installed."
        }), 503


if __name__ == "__main__":
    app.run(debug=True, port=5001)