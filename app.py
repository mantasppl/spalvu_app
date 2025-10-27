from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

vardai = ["Jonas", "Mantas", "Laura", "Asta", "Tomas", "Rūta", "Dovydas"]
spalvos = ["Raudona", "Žalia", "Mėlyna", "Geltona", "Oranžinė", "Violetinė", "Rožinė"]
rezultatai = {}

@app.route("/")
def index():
    return render_template("index.html", vardai=vardai, rezultatai=rezultatai)

@app.route("/istraukti", methods=["POST"])
def istraukti():
    vardas = request.form.get("vardas")
    if vardas not in vardai:
        return jsonify({"klaida": "Šis vardas jau pasirinko spalvą arba neegzistuoja."})
    if not spalvos:
        return jsonify({"klaida": "Nebelikę spalvų."})
    spalva = random.choice(spalvos)
    rezultatai[vardas] = spalva
    vardai.remove(vardas)
    spalvos.remove(spalva)
    return jsonify({"vardas": vardas, "spalva": spalva})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
