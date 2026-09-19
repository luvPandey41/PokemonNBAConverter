from flask import Flask, jsonify, request
import main

app = Flask(__name__)

#Post lets you actually give data from frontend(javascript) to backend (python), whereas get is mainly used for the opposite
@app.route("/match", methods=["POST"])
def match():
    data = request.get_json()

    return jsonify()({
        "data recieved": data
    })

@app.route("/pokemon")
def index():
    name = request.args.get("player")
    name = name.lower()

    pokemon_data = main.find_pokemons_for_player(name)

    return jsonify({
        "player": name,
        "stats": pokemon_data
    })

if __name__ == "__main__":
    app.run(debug=True)