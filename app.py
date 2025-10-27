from flask import Flask, render_template, request, jsonify
import random
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# --- Funkcijos JSON load/save ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("vardai", []), data.get("spalvos", []), data.get("rezultatai", {})
    else:
        vardai = ["Jonas", "Mantas", "Laura", "Asta", "Tomas", "Rūta", "Dovydas"]
        spalvos = ["Raudona", "Žalia", "Mėlyna", "Geltona", "Oranžinė", "Violetinė", "Rožinė"]
        rezultatai = {}
        save_data(vardai, spalvos, rezultatai)
        return vardai, spalvos, rezultatai

def save_data(vardai, spalvos, rezultatai):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "vardai": vardai,
            "spalvos": spalvos,
            "rezultatai": rezultatai
        }, f, ensure_ascii=False, indent=4)

# --- Įkeliam duomenis ---
vardai, spalvos, rezultatai = load_data()

# --- Pagrindinis puslapis ---
@app.route("/")
def index():
    return render_template("index.html", vardai=vardai, rezultatai=rezultatai)

# --- Traukti spalvą endpoint ---
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

    save_data(vardai, spalvos, rezultatai)
    return jsonify({"vardas": vardas, "spalva": spalva})

# --- RESET endpoint (dedam čia, prieš __main__) ---
@app.route("/reset")
def reset():
    global vardai, spalvos, rezultatai
    vardai = ["Jonas", "Mantas", "Laura", "Asta", "Tomas", "Rūta", "Dovydas"]
    spalvos = ["Raudona", "Žalia", "Mėlyna", "Geltona", "Oranžinė", "Violetinė", "Rožinė"]
    rezultatai = {}
    save_data(vardai, spalvos, rezultatai)
    return "Sistema atstatyta!"

# --- Startas ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
