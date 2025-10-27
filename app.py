from flask import Flask, render_template, request, jsonify
import random
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# Funkcija, kuri įkelia duomenis
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("vardai", []), data.get("spalvos", []), data.get("rezultatai", {})
    else:
        # Default duomenys
        vardai = ["Jonas", "Mantas", "Laura", "Asta", "Tomas", "Rūta", "Dovydas"]
        spalvos = ["Raudona", "Žalia", "Mėlyna", "Geltona", "Oranžinė", "Violetinė", "Rožinė"]
        rezultatai = {}
        save_data(vardai, spalvos, rezultatai)
        return vardai, spalvos, rezultatai

# Funkcija, kuri išsaugo duomenis
def save_data(vardai, spalvos, rezultatai):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "vardai": vardai,
            "spalvos": spalvos,
            "rezultatai": rezultatai
        }, f, ensure_ascii=False, indent=4)

# Įkeliam duomenis į atmintį
vardai, spalvos, rezultatai = load_data()

@app.route("/")
def index():
    return render_template("index.html", vardai=vardai, rezultatai=rezultatai)

@app.route("/istraukti", methods=["POST"])
def istraukti():
    global vardai, spalvos, rezultatai

    vardas = request.form.get("vardas")

    if vardas not in vardai:
        return jsonify({"klaida": "Šis vardas jau pasirinko spalvą arba neegzistuoja."})

    if not spalvos:
        return jsonify({"klaida": "Nebelikę spalvų."})

    spalva = random.choice(spalvos)
    rezultatai[vardas] = spalva
    vardai.remove(vardas)
    spalvos.remove(spalva)

    # Išsaugom JSON
    save_data(vardai, spalvos, rezultatai)

    return jsonify({"vardas": vardas, "spalva": spalva})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
