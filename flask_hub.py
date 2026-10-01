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
    #make it so that a .json file is checked first before actually doing an api call, avoiding it if possible. No database tho. This should be part of getroster function. 
    return jsonify(main.get_roster(int(team_id)))

if __name__ == "__main__":
    app.run(debug=True)


