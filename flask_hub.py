from flask import Flask, render_template, jsonify, request;
import main


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/roster/<team_id>")
def returnTeam(team_id):
    #make it so that a .json file is checked first before actually doing an api call, avoiding it if possible. No database tho. This should be part of getroster function. 
    return jsonify(main.get_roster(int(team_id)))


@app.route("/results")
def results():
    player_id = request.args.get("player_id", type = int) #tuff query paramter (processes url which has /results?player_id=2544)
    return render_template("results.html", player_id = player_id)

if __name__ == "__main__":
    app.run(debug=True)


