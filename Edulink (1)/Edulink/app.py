from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests from your frontend

# Configure the API
genai.configure(api_key="AIzaSyC7ozv0f6WZhHD02HbTFDAIFG9ck9U5bvQ")

# Initialize the model
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_query = data.get("message", "")
        
        if not user_query:
            return jsonify({"error": "Empty query"}), 400

        prompt = "You are an expert AI assistant. Answer in a simple and clear way. " + user_query
        messages = [{"role": "user", "parts": [{"text": prompt}]}]

        response = model.generate_content(messages)
        ai_response = response.text if hasattr(response, "text") else "Sorry, I couldn't generate a response."

        return jsonify({"response": ai_response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
