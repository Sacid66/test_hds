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

# 1. HADİS KONTROLÜ
@app.route("/check_hadis", methods=["POST"])
def check_hadis():
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
                        "Sana verilen metni mutlaka analiz et ve şunları yap: "
                        "1. Metin bir İslam hadisine benziyorsa, mutlaka 'Bu metin bir hadise benziyor' yaz ve hangi hadise benzediğini açıkla. "
                        "2. Metin hiçbir şekilde bir İslam hadisine benzemiyorsa, 'Bu bir hadis değildir' yaz. "
                        "Karar verirken metnin bağlamına ve kelime yapısına bak. Tereddüt etmeyip kesin bir karar ver."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Metin: {text}",
                },
            ],
        )
        result = response["choices"][0]["message"]["content"].strip()

        # Yanıtı kontrol et
        if "Bu bir hadis değildir" in result:
            return jsonify({"is_hadis": False, "message": result})
        else:
            return jsonify({"is_hadis": True, "message": result})

    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500


# 2. HADİS ANALİZİ
@app.route("/analyze_hadis", methods=["POST"])
def analyze_hadis():
    data = request.json
    hadis = data.get("hadis")
    action = data.get("action")

    if not hadis or not action:
        return jsonify({"error": "Hadis ve aksiyon boş olamaz"}), 400

    # OpenAI API çağrısı
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sen bir İslam hadisi analiz sistemisin. "
                        "Verilen hadisi ve seçilen aksiyonu analiz et. "
                        "Eğer verilen hadis, sahih kaynaklarda geçen bilgilere uyuyorsa, analiz sonuçlarını açıkla. "
                        "Analiz yaparken metinle ilgili kapsamlı bilgi ver ve metni açıklığa kavuştur."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Hadis: {hadis}\nAksiyon: {action}",
                },
            ],
        )
        result = response["choices"][0]["message"]["content"].strip()
        return jsonify({"result": result})

    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)