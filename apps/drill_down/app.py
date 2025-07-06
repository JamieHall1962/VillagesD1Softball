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
    # Aggregate player stats for the table
    # Assume BattingStats.csv has columns: PersonNumber, Season, Gm, PA, AB, R, H, 1B, 2B, 3B, HR, RBI, BB, SF, OE, TB, BA, Slg, OBP
    # Group by PersonNumber and sum numeric columns
    agg_cols = ['Gm', 'PA', 'AB', 'R', 'H', '1B', '2B', '3B', 'HR', 'RBI', 'BB', 'SF', 'OE', 'TB']
    sum_stats = batting_df.groupby('PersonNumber')[agg_cols].sum().reset_index()
    # Calculate BA, Slg, OBP if not present
    if 'BA' not in sum_stats.columns:
        sum_stats['BA'] = (sum_stats['H'] / sum_stats['AB']).round(3)
    if 'Slg' not in sum_stats.columns:
        sum_stats['Slg'] = (sum_stats['TB'] / sum_stats['AB']).round(3)
    if 'OBP' not in sum_stats.columns:
        sum_stats['OBP'] = ((sum_stats['H'] + sum_stats['BB']) / sum_stats['PA']).round(3)
    # Merge with player names
    merged = sum_stats.merge(players_df[['PersonNumber', 'FirstName', 'LastName']], left_on='PersonNumber', right_on='PersonNumber', how='left')
    merged['Name'] = merged['FirstName'].fillna('') + ' ' + merged['LastName'].fillna('')
    # Add Rank
    merged = merged.sort_values(by=['H', 'Gm'], ascending=[False, False]).reset_index(drop=True)
    merged['Rank'] = merged.index + 1
    # Reorder columns
    display_cols = ['Rank', 'Name'] + agg_cols + ['BA', 'Slg', 'OBP']
    player_list = merged[display_cols].to_dict(orient='records')
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
    # Get player info
    player = players_df[players_df['PersonNumber'] == player_id]
    if not player.empty:
        player = player.iloc[0].to_dict()
    else:
        player = None
    # Get season-by-season stats
    player_seasons = batting_df[batting_df['PersonNumber'] == player_id]
    if not player_seasons.empty:
        season_stats = player_seasons.groupby('Season').sum(numeric_only=True).reset_index()
    else:
        season_stats = None
    return render_template('player_detail.html', player=player, season_stats=season_stats)

@app.route('/player/<int:player_id>/games')
def player_games(player_id):
    # Get all games for the player
    player_games = games_df[games_df['PersonNumber'] == player_id]
    return render_template('player_games.html', games=player_games.to_dict(orient='records'))

# Add more routes for player detail, seasons, games, etc. as needed

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port) 