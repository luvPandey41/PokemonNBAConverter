from flask import Flask, jsonify, request, render_template
import main

app = Flask(__name__)

#Post lets you actually give data from frontend(javascript) to backend (python), whereas get is mainly used for the opposite
@app.route("/match", methods=["POST"])
def match():
    data = request.get_json()
    player = data.get("player")

    pokemon_data = main.find_pokemons_for_player(player)

    return jsonify({
        "player": player,
        "stats" : pokemon_data
    })

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)