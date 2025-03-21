from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

PRIORITY_MAPPING = {
    "Samples": 1,
    "Medicine": 2,
    "Documents": 3,
    "Linen": 4,
    "Others": 5
}

@app.route("/classify", methods=["POST"])
def classify():
    try:
        data = request.get_json()
        description = data.get("description", "")
        if not description:
            return jsonify({"error": "No description provided"}), 400

        model = genai.GenerativeModel("gemini-pro")

        #testing
        print("Available Gemini models:")
        for model in genai.list_models():
            print(model.name)


        prompt = f"""
        Classify this hospital delivery item into one of these categories:
        - Samples
        - Medicine
        - Documents
        - Linen
        - Others

        Description: {description}

        Return only the category name.
        """
        response = model.generate_content(prompt)
        category = response.text.strip()
        priority = PRIORITY_MAPPING.get(category, 5)

        return jsonify({"category": category, "priority": priority})
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500


@app.route("/", methods=["GET"])
def health():
    return "Gemini Flask API is running!"
