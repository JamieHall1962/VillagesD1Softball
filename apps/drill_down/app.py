import os
import pandas as pd
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')

# Data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
players_csv = os.path.join(DATA_DIR, 'People.csv')
batting_csv = os.path.join(DATA_DIR, 'BattingStats.csv')
teams_csv = os.path.join(DATA_DIR, 'Teams.csv')
games_csv = os.path.join(DATA_DIR, 'GameStats.csv')

# Load data
players_df = pd.read_csv(players_csv)
batting_df = pd.read_csv(batting_csv)
teams_df = pd.read_csv(teams_csv)
games_df = pd.read_csv(games_csv)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/players")
def players():
    player_list = []
    for _, row in players_df.iterrows():
        player_list.append({
            "player_id": row.get("PersonNumber"),
            "display_name": f"{row.get('FirstName', '')} {row.get('LastName', '')}",
            "date_joined": row.get("DateJoined", ""),  # Adjust if your CSV uses a different column
            "status": "active",  # Or use a real field if available
            "disambiguation_notes": row.get("Notes", "")  # Adjust if your CSV uses a different column
        })
    return render_template("players.html", players=player_list)

@app.route("/api/players")
def api_players():
    player_list = players_df[['PersonNumber', 'FirstName', 'LastName']].to_dict(orient='records')
    return jsonify(player_list)

@app.route('/seasons')
def seasons():
    return render_template('seasons.html')

@app.route('/player/<int:player_id>')
def player_detail(player_id):
    import pandas as pd
    people_df = pd.read_csv('apps/drill_down/data/People.csv')
    player = people_df[people_df['PersonNumber'] == player_id].to_dict(orient='records')
    if player:
        player = player[0]
    else:
        player = None
    return render_template('player_detail.html', player=player)

# Add more routes for player detail, seasons, games, etc. as needed

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port) 