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
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Get all players with career batting totals
        query = """
        SELECT 
            p.personnumber,
            p.firstname,
            p.lastname,
            COUNT(DISTINCT bs.gamenumber) as games_played,
            SUM(bs.pa) as plate_appearances,
            SUM(bs.ab) as at_bats,
            SUM(bs.r) as runs,
            SUM(bs.h) as hits,
            SUM(bs.d) as doubles,
            SUM(bs.t) as triples,
            SUM(bs.hr) as home_runs,
            SUM(bs.rbi) as rbi,
            SUM(bs.bb) as walks,
            SUM(bs.so) as strikeouts,
            SUM(bs.sb) as stolen_bases,
            CASE 
                WHEN SUM(bs.ab) > 0 THEN ROUND(SUM(bs.h)::numeric / SUM(bs.ab)::numeric, 3)
                ELSE 0 
            END as batting_average,
            CASE 
                WHEN SUM(bs.pa) > 0 THEN ROUND((SUM(bs.h) + SUM(bs.bb) + SUM(bs.hp))::numeric / SUM(bs.pa)::numeric, 3)
                ELSE 0 
            END as on_base_percentage
        FROM people p
        LEFT JOIN battingstats bs ON p.personnumber = bs.playernumber
        GROUP BY p.personnumber, p.firstname, p.lastname
        HAVING COUNT(DISTINCT bs.gamenumber) > 0
        ORDER BY p.lastname, p.firstname
        """
        
        cursor.execute(query)
        players = cursor.fetchall()
        
        # Convert to list of dictionaries
        players_list = []
        for player in players:
            players_list.append({
                'id': player['personnumber'],
                'name': f"{player['firstname']} {player['lastname']}",
                'first_name': player['firstname'],
                'last_name': player['lastname'],
                'games': player['games_played'] or 0,
                'pa': player['plate_appearances'] or 0,
                'ab': player['at_bats'] or 0,
                'r': player['runs'] or 0,
                'h': player['hits'] or 0,
                'd': player['doubles'] or 0,
                't': player['triples'] or 0,
                'hr': player['home_runs'] or 0,
                'rbi': player['rbi'] or 0,
                'bb': player['walks'] or 0,
                'so': player['strikeouts'] or 0,
                'sb': player['stolen_bases'] or 0,
                'avg': player['batting_average'] or 0,
                'obp': player['on_base_percentage'] or 0
            })
        
        cursor.close()
        conn.close()
        
        return jsonify(players_list)
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/<int:player_id>/seasons')
def get_player_seasons(player_id):
    """Get seasons for a specific player"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Get seasons for this player with season totals
        query = """
        SELECT 
            EXTRACT(YEAR FROM gs.gamedate) as season,
            COUNT(DISTINCT bs.gamenumber) as games_played,
            SUM(bs.pa) as plate_appearances,
            SUM(bs.ab) as at_bats,
            SUM(bs.r) as runs,
            SUM(bs.h) as hits,
            SUM(bs.d) as doubles,
            SUM(bs.t) as triples,
            SUM(bs.hr) as home_runs,
            SUM(bs.rbi) as rbi,
            SUM(bs.bb) as walks,
            SUM(bs.so) as strikeouts,
            SUM(bs.sb) as stolen_bases,
            CASE 
                WHEN SUM(bs.ab) > 0 THEN ROUND(SUM(bs.h)::numeric / SUM(bs.ab)::numeric, 3)
                ELSE 0 
            END as batting_average,
            CASE 
                WHEN SUM(bs.pa) > 0 THEN ROUND((SUM(bs.h) + SUM(bs.bb) + SUM(bs.hp))::numeric / SUM(bs.pa)::numeric, 3)
                ELSE 0 
            END as on_base_percentage
        FROM battingstats bs
        JOIN gamestats gs ON bs.gamenumber = gs.gamenumber
        WHERE bs.playernumber = %s
        GROUP BY EXTRACT(YEAR FROM gs.gamedate)
        ORDER BY season DESC
        """
        
        cursor.execute(query, (player_id,))
        seasons = cursor.fetchall()
        
        # Convert to list of dictionaries
        seasons_list = []
        for season in seasons:
            seasons_list.append({
                'season': int(season['season']),
                'games': season['games_played'] or 0,
                'pa': season['plate_appearances'] or 0,
                'ab': season['at_bats'] or 0,
                'r': season['runs'] or 0,
                'h': season['hits'] or 0,
                'd': season['doubles'] or 0,
                't': season['triples'] or 0,
                'hr': season['home_runs'] or 0,
                'rbi': season['rbi'] or 0,
                'bb': season['walks'] or 0,
                'so': season['strikeouts'] or 0,
                'sb': season['stolen_bases'] or 0,
                'avg': season['batting_average'] or 0,
                'obp': season['on_base_percentage'] or 0
            })
        
        cursor.close()
        conn.close()
        
        return jsonify(seasons_list)
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/<int:player_id>/seasons/<int:season>/games')
def get_player_season_games(player_id, season):
    """Get game-by-game stats for a player in a specific season"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Get game-by-game stats for this player in this season
        query = """
        SELECT 
            gs.gamenumber,
            gs.gamedate,
            t.teamname,
            CASE WHEN bs.hometeam THEN 'Home' ELSE 'Away' END as home_away,
            bs.pa,
            bs.ab,
            bs.r,
            bs.h,
            bs.d,
            bs.t,
            bs.hr,
            bs.rbi,
            bs.bb,
            bs.so,
            bs.sb,
            CASE 
                WHEN bs.ab > 0 THEN ROUND(bs.h::numeric / bs.ab::numeric, 3)
                ELSE 0 
            END as game_avg
        FROM battingstats bs
        JOIN gamestats gs ON bs.gamenumber = gs.gamenumber
        JOIN teams t ON bs.teamnumber = t.teamnumber
        WHERE bs.playernumber = %s 
        AND EXTRACT(YEAR FROM gs.gamedate) = %s
        ORDER BY gs.gamedate, gs.gamenumber
        """
        
        cursor.execute(query, (player_id, season))
        games = cursor.fetchall()
        
        # Convert to list of dictionaries
        games_list = []
        for game in games:
            games_list.append({
                'game_number': game['gamenumber'],
                'date': game['gamedate'].strftime('%m/%d/%Y') if game['gamedate'] else '',
                'team': game['teamname'],
                'home_away': game['home_away'],
                'pa': game['pa'] or 0,
                'ab': game['ab'] or 0,
                'r': game['r'] or 0,
                'h': game['h'] or 0,
                'd': game['d'] or 0,
                't': game['t'] or 0,
                'hr': game['hr'] or 0,
                'rbi': game['rbi'] or 0,
                'bb': game['bb'] or 0,
                'so': game['so'] or 0,
                'sb': game['sb'] or 0,
                'avg': game['game_avg'] or 0
            })
        
        cursor.close()
        conn.close()
        
        return jsonify(games_list)
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/seasons')
def get_seasons():
    """Get all seasons"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Get all seasons
        query = """
        SELECT DISTINCT 
            EXTRACT(YEAR FROM gamedate) as season,
            COUNT(DISTINCT gamenumber) as total_games
        FROM gamestats 
        WHERE gamedate IS NOT NULL
        GROUP BY EXTRACT(YEAR FROM gamedate)
        ORDER BY season DESC
        """
        
        cursor.execute(query)
        seasons = cursor.fetchall()
        
        # Convert to list of dictionaries
        seasons_list = []
        for season in seasons:
            seasons_list.append({
                'season': int(season['season']),
                'total_games': season['total_games'] or 0
            })
        
        cursor.close()
        conn.close()
        
        return jsonify(seasons_list)
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/seasons/<int:season>/standings')
def get_season_standings(season):
    """Get final standings for a specific season"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Get team standings for this season
        query = """
        SELECT 
            t.teamnumber,
            t.teamname,
            COUNT(DISTINCT gs.gamenumber) as games_played,
            COUNT(CASE WHEN gs.hometeam AND gs.homescore > gs.awayscore THEN 1 END) +
            COUNT(CASE WHEN NOT gs.hometeam AND gs.awayscore > gs.homescore THEN 1 END) as wins,
            COUNT(CASE WHEN gs.hometeam AND gs.homescore < gs.awayscore THEN 1 END) +
            COUNT(CASE WHEN NOT gs.hometeam AND gs.awayscore < gs.homescore THEN 1 END) as losses,
            COUNT(CASE WHEN gs.homescore = gs.awayscore THEN 1 END) as ties,
            ROUND(
                (COUNT(CASE WHEN gs.hometeam AND gs.homescore > gs.awayscore THEN 1 END) +
                 COUNT(CASE WHEN NOT gs.hometeam AND gs.awayscore > gs.homescore THEN 1 END))::numeric /
                NULLIF(COUNT(DISTINCT gs.gamenumber), 0)::numeric, 3
            ) as win_percentage
        FROM teams t
        JOIN gamestats gs ON (t.teamnumber = gs.hometeamnumber OR t.teamnumber = gs.awayteamnumber)
        WHERE EXTRACT(YEAR FROM gs.gamedate) = %s
        GROUP BY t.teamnumber, t.teamname
        ORDER BY win_percentage DESC, wins DESC
        """
        
        cursor.execute(query, (season,))
        standings = cursor.fetchall()
        
        # Convert to list of dictionaries
        standings_list = []
        for team in standings:
            standings_list.append({
                'team_id': team['teamnumber'],
                'team_name': team['teamname'],
                'games': team['games_played'] or 0,
                'wins': team['wins'] or 0,
                'losses': team['losses'] or 0,
                'ties': team['ties'] or 0,
                'win_pct': team['win_percentage'] or 0
            })
        
        cursor.close()
        conn.close()
        
        return jsonify(standings_list)
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/teams/<int:team_id>/season/<int:season>')
def get_team_season_details(team_id, season):
    """Get team details for a specific season"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Get team info
        team_query = "SELECT teamname FROM teams WHERE teamnumber = %s"
        cursor.execute(team_query, (team_id,))
        team_result = cursor.fetchone()
        team_name = team_result['teamname'] if team_result else 'Unknown Team'
        
        # Get roster
        roster_query = """
        SELECT DISTINCT 
            p.personnumber,
            p.firstname,
            p.lastname,
            COUNT(DISTINCT bs.gamenumber) as games_played
        FROM people p
        JOIN battingstats bs ON p.personnumber = bs.playernumber
        JOIN gamestats gs ON bs.gamenumber = gs.gamenumber
        WHERE bs.teamnumber = %s AND EXTRACT(YEAR FROM gs.gamedate) = %s
        GROUP BY p.personnumber, p.firstname, p.lastname
        ORDER BY p.lastname, p.firstname
        """
        
        cursor.execute(roster_query, (team_id, season))
        roster = cursor.fetchall()
        
        # Get batting stats
        batting_query = """
        SELECT 
            p.firstname,
            p.lastname,
            COUNT(DISTINCT bs.gamenumber) as games,
            SUM(bs.pa) as pa,
            SUM(bs.ab) as ab,
            SUM(bs.r) as r,
            SUM(bs.h) as h,
            SUM(bs.d) as d,
            SUM(bs.t) as t,
            SUM(bs.hr) as hr,
            SUM(bs.rbi) as rbi,
            SUM(bs.bb) as bb,
            SUM(bs.so) as so,
            SUM(bs.sb) as sb,
            CASE 
                WHEN SUM(bs.ab) > 0 THEN ROUND(SUM(bs.h)::numeric / SUM(bs.ab)::numeric, 3)
                ELSE 0 
            END as avg,
            CASE 
                WHEN SUM(bs.pa) > 0 THEN ROUND((SUM(bs.h) + SUM(bs.bb) + SUM(bs.hp))::numeric / SUM(bs.pa)::numeric, 3)
                ELSE 0 
            END as obp
        FROM battingstats bs
        JOIN people p ON bs.playernumber = p.personnumber
        JOIN gamestats gs ON bs.gamenumber = gs.gamenumber
        WHERE bs.teamnumber = %s AND EXTRACT(YEAR FROM gs.gamedate) = %s
        GROUP BY p.personnumber, p.firstname, p.lastname
        HAVING COUNT(DISTINCT bs.gamenumber) > 0
        ORDER BY avg DESC, p.lastname, p.firstname
        """
        
        cursor.execute(batting_query, (team_id, season))
        batting_stats = cursor.fetchall()
        
        # Get pitching stats
        pitching_query = """
        SELECT 
            p.firstname,
            p.lastname,
            COUNT(DISTINCT ps.gamenumber) as games,
            SUM(ps.ip) as innings_pitched,
            SUM(ps.bf) as batters_faced,
            SUM(ps.r) as runs,
            SUM(ps.er) as earned_runs,
            SUM(ps.h) as hits,
            SUM(ps.bb) as walks,
            SUM(ps.so) as strikeouts,
            SUM(ps.w) as wins,
            SUM(ps.l) as losses,
            SUM(ps.sv) as saves,
            CASE 
                WHEN SUM(ps.ip) > 0 THEN ROUND(SUM(ps.er)::numeric * 7 / SUM(ps.ip)::numeric, 2)
                ELSE 0 
            END as era,
            CASE 
                WHEN SUM(ps.ip) > 0 THEN ROUND((SUM(ps.h) + SUM(ps.bb))::numeric / (SUM(ps.ip) / 7)::numeric, 2)
                ELSE 0 
            END as whip
        FROM pitchingstats ps
        JOIN people p ON ps.playernumber = p.personnumber
        JOIN gamestats gs ON ps.gamenumber = gs.gamenumber
        WHERE ps.teamnumber = %s AND EXTRACT(YEAR FROM gs.gamedate) = %s
        GROUP BY p.personnumber, p.firstname, p.lastname
        HAVING COUNT(DISTINCT ps.gamenumber) > 0
        ORDER BY era ASC, p.lastname, p.firstname
        """
        
        cursor.execute(pitching_query, (team_id, season))
        pitching_stats = cursor.fetchall()
        
        # Get game scores
        games_query = """
        SELECT 
            gamenumber,
            gamedate,
            hometeamnumber,
            awayteamnumber,
            homescore,
            awayscore,
            CASE 
                WHEN hometeamnumber = %s AND homescore > awayscore THEN 'W'
                WHEN awayteamnumber = %s AND awayscore > homescore THEN 'W'
                WHEN homescore = awayscore THEN 'T'
                ELSE 'L'
            END as result
        FROM gamestats
        WHERE (hometeamnumber = %s OR awayteamnumber = %s)
        AND EXTRACT(YEAR FROM gamedate) = %s
        ORDER BY gamedate, gamenumber
        """
        
        cursor.execute(games_query, (team_id, team_id, team_id, team_id, season))
        games = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'team_name': team_name,
            'roster': [{'id': p['personnumber'], 'name': f"{p['firstname']} {p['lastname']}", 'games': p['games_played']} for p in roster],
            'batting_stats': [dict(p) for p in batting_stats],
            'pitching_stats': [dict(p) for p in pitching_stats],
            'games': [{
                'game_number': g['gamenumber'],
                'date': g['gamedate'].strftime('%m/%d/%Y') if g['gamedate'] else '',
                'result': g['result'],
                'score': f"{g['homescore']}-{g['awayscore']}" if g['homescore'] is not None and g['awayscore'] is not None else 'N/A'
            } for g in games]
        })
        
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 