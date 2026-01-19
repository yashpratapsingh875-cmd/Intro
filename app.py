from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import requests
import os
import uuid

app = Flask(__name__)
CORS(app)

TELEGRAM_TOKEN = "PASTE_NEW_TOKEN_HERE"
CHAT_ID = "6392736953"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route("/")
def home():
    return "Backend is running OK"
@app.route("/generate", methods=["POST"])
def generate():
    name = request.form.get("name")
    age = request.form.get("age")
    status = request.form.get("status")
    study_detail = request.form.get("study_detail")
    address = request.form.get("address")
    insta = request.form.get("insta")

    photo = request.files.get("photo")

    filename = f"{insta}_{uuid.uuid4().hex}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Create image
    img = Image.new("RGB", (700, 400), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font_big = ImageFont.truetype("DejaVuSans.ttf", 32)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 20)
    except:
        font_big = font_small = ImageFont.load_default()

    # Insta ID top
    draw.text((20, 20), f"@{insta}", fill="black", font=font_big)

    y = 80
    draw.text((20, y), f"Name: {name}", fill="black", font=font_small); y+=30
    draw.text((20, y), f"Age: {age}", fill="black", font=font_small); y+=30
    draw.text((20, y), f"Status: {status}", fill="black", font=font_small); y+=30
    draw.text((20, y), f"Study/Job: {study_detail}", fill="black", font=font_small); y+=30
    draw.text((20, y), f"Address: {address}", fill="black", font=font_small)

    # Paste photo
    user_img = Image.open(photo).resize((180, 220))
    img.paste(user_img, (480, 100))

    img.save(filepath)

    # Send to Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    with open(filepath, "rb") as f:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": f})

    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run()