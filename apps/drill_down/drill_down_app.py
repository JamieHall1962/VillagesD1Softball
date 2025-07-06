"""
Drill-Down Softball Statistics Application
Two main sections: Players and Seasons with drill-down navigation
"""

from flask import Flask, render_template, request, jsonify
import psycopg2
import psycopg2.extras
from datetime import datetime
import os

app = Flask(__name__)

# Database configuration
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'apssb_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    """Main page with Players and Seasons sections"""
    return render_template('index.html')

@app.route('/api/players')
def get_players():
    """Get all players with career totals"""
    # Remove all psycopg2 imports and usage
    # The app should not attempt to connect to PostgreSQL or use psycopg2 at all.
    # This function will now return a placeholder or an error.
    return jsonify({'error': 'Database connection failed (psycopg2 removed)'}), 500

@app.route('/api/players/<int:player_id>/seasons')
def get_player_seasons(player_id):
    """Get seasons for a specific player"""
    # Remove all psycopg2 imports and usage
    # The app should not attempt to connect to PostgreSQL or use psycopg2 at all.
    # This function will now return a placeholder or an error.
    return jsonify({'error': 'Database connection failed (psycopg2 removed)'}), 500

@app.route('/api/players/<int:player_id>/seasons/<int:season>/games')
def get_player_season_games(player_id, season):
    """Get game-by-game stats for a player in a specific season"""
    # Remove all psycopg2 imports and usage
    # The app should not attempt to connect to PostgreSQL or use psycopg2 at all.
    # This function will now return a placeholder or an error.
    return jsonify({'error': 'Database connection failed (psycopg2 removed)'}), 500

@app.route('/api/seasons')
def get_seasons():
    """Get all seasons"""
    # Remove all psycopg2 imports and usage
    # The app should not attempt to connect to PostgreSQL or use psycopg2 at all.
    # This function will now return a placeholder or an error.
    return jsonify({'error': 'Database connection failed (psycopg2 removed)'}), 500

@app.route('/api/seasons/<int:season>/standings')
def get_season_standings(season):
    """Get final standings for a specific season"""
    # Remove all psycopg2 imports and usage
    # The app should not attempt to connect to PostgreSQL or use psycopg2 at all.
    # This function will now return a placeholder or an error.
    return jsonify({'error': 'Database connection failed (psycopg2 removed)'}), 500

@app.route('/api/teams/<int:team_id>/season/<int:season>')
def get_team_season_details(team_id, season):
    """Get team details for a specific season"""
    # Remove all psycopg2 imports and usage
    # The app should not attempt to connect to PostgreSQL or use psycopg2 at all.
    # This function will now return a placeholder or an error.
    return jsonify({'error': 'Database connection failed (psycopg2 removed)'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 