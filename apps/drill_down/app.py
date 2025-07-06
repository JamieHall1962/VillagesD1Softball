import os
import pandas as pd
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Example: Load CSV data at startup (adjust paths as needed)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
players_csv = os.path.join(DATA_DIR, 'People.csv')
batting_csv = os.path.join(DATA_DIR, 'BattingStats.csv')
teams_csv = os.path.join(DATA_DIR, 'Teams.csv')
games_csv = os.path.join(DATA_DIR, 'GameStats.csv')

players_df = pd.read_csv(players_csv)
batting_df = pd.read_csv(batting_csv)
teams_df = pd.read_csv(teams_csv)
games_df = pd.read_csv(games_csv)

@app.route("/")
def home():
    return "D1 Softball Stats App is running!"

@app.route("/players")
def players():
    # Example: Return player names as JSON
    player_list = players_df[['PersonNumber', 'FirstName', 'LastName']].to_dict(orient='records')
    return jsonify(player_list)

# Add more routes as needed for your app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port) 