from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv
import os

# .env dosyasını yükleme
load_dotenv()

# Flask uygulaması
app = Flask(__name__)

# OpenAI API Anahtarı
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

# 1. HADİS KONTROLÜ (Basit doğrulama)
@app.route("/check_hadis_simple", methods=["POST"])
def check_hadis_simple():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "Metin boş olamaz"}), 400

    # OpenAI API çağrısı
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sen bir İslam hadisi doğrulama sistemisin. "
                        "Girilen metni analiz et ve sadece şu iki sonuçtan birini ver: "
                        "'Bu bir hadis!' veya 'Bu yazdığınız şey hadis değil!'. "
                        "Karar verirken Kur'an'daki yaratılış ayetlerini ve İslam Hadis literatürünü dikkate al."
                    ),
                },
                {"role": "user", "content": f"Metin: {text}"},
            ],
        )
        result = response["choices"][0]["message"]["content"].strip()

        # Yanıtı kontrol et
        if "Bu yazdığınız şey hadis değil!" in result:
            return jsonify({"is_hadis": False, "message": result})
        elif "Bu bir hadis!" in result:
            return jsonify({"is_hadis": True, "message": result})
        else:
            return jsonify({"is_hadis": False, "message": "Bir hata oluştu, metin değerlendirilemedi."})

    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

# 2. HADİS ANALİZİ (Kur'an uyumlu detaylı analiz)
@app.route("/check_hadis_advanced", methods=["POST"])
def check_hadis_advanced():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "Metin boş olamaz"}), 400

    # OpenAI API çağrısı
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sen bir İslam hadisi doğrulama ve analiz sistemisin. "
                        "Girilen metni analiz et ve sadece şu iki sonuçtan birini ver: "
                        "'Bu bir hadis!' veya 'Bu yazdığınız şey hadis değil!'. "
                        "Eğer metin bir İslam hadisine benziyorsa ve Kur'an ile çelişmiyorsa, 'Bu bir hadis!' yaz. "
                        "Eğer metin Kur'an ile çelişen ifadeler içeriyorsa veya bir İslam hadisine benzemiyorsa, 'Bu yazdığınız şey hadis değil!' yaz. "
                        "Karar verirken Kur'an'daki yaratılış ayetlerini ve İslam Hadis literatürünü dikkate al."
                    ),
                },
                {"role": "user", "content": f"Metin: {text}"},
            ],
        )
        result = response["choices"][0]["message"]["content"].strip()

        # Yanıtı kontrol et
        if "Bu yazdığınız şey hadis değil!" in result:
            return jsonify({"is_hadis": False, "message": result})
        elif "Bu bir hadis!" in result:
            return jsonify({"is_hadis": True, "message": result})
        else:
            return jsonify({"is_hadis": False, "message": "Bir hata oluştu, metin değerlendirilemedi."})

    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Render'ın belirlediği PORT'u kullanıyoruz
    app.run(host="0.0.0.0", port=port)
