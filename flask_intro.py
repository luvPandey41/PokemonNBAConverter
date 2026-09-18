from flask import Flask, jsonify
import main

result = main.prompt()


app = Flask(__name__)

@app.route("/pokemon")
def index():
    return jsonify(result)

#unedited
@app.route("/pokemon/<name>")
def get_pokemon(name):
    name = name.lower()

    pokemon_data = main.find_pokemons_for_player("lebron james")

    if name not in pokemon_data:
        return jsonify({"error": "Pokemon not found"})

    return jsonify({
        "name": name,
        "score": pokemon_data[name]
    })

if __name__ == "__main__":
    app.run(debug=True)