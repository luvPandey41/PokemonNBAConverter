from flask import Flask, render_template, jsonify
import main


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test")
def test():
    return jsonify([{
        "name": "LeBron James",
        "id": 2544,
        "position": "Forward"
    }])


@app.route("/roster/<team_id>")
def returnTeam(team_id):
    return jsonify(main.getRoster(team_id))

if __name__ == "__main__":
    app.run(debug=True)