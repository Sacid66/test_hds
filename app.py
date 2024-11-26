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
                        "Girilen metni analiz et ve sonuç ver. "
                        "1. Eğer metin bir İslam hadisine benziyorsa, 'Bu bir hadis!' yaz. "
                        "2. Eğer metin bir İslam hadisi değilse, 'Bu yazdığınız şey hadis değil!' yaz."
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
                        "Sana bir metin verildiğinde şunları yap: "
                        "1. Eğer metin bir İslam hadisine benziyorsa ve Kur'an ile uyumluysa, 'Bu bir hadis!' yaz. "
                        "2. Eğer metin bir İslam hadisine benzemiyor ve Kur'an ile çelişen ifadeler içeriyorsa, 'Bu yazdığınız şey hadis değil!' yaz. "
                        "Kur'an'daki ayetlerle metin arasındaki uyumu değerlendir ve metni analiz et."
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
