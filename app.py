from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from PIL import Image
import base64
import io
import os

app = Flask(__name__)
CORS(app)

# Set your API key here or with an environment variable
openai.api_key = "sk-..."  # Replace with your actual key

@app.route("/analyze", methods=["POST"])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe any structural damage in this image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ],
            }
        ],
        max_tokens=500,
    )

    answer = response['choices'][0]['message']['content']
    return jsonify({"analysis": answer})