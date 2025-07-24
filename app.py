from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime
import re

app = Flask(__name__)

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('softball_stats.db')
    conn.row_factory = sqlite3.Row
    return conn

# Update your calculate_batting_stats function in app.py:

def calculate_batting_stats(stats_dict):
    """
    Calculate derived batting statistics from raw stats
    Returns a dictionary with calculated values
    """
    # Convert to regular dict if it's a sqlite Row
    if hasattr(stats_dict, '_mapping'):
        stats = dict(stats_dict)
    else:
        stats = stats_dict.copy()
    
    # Get raw values (handle None/NULL values)
    pa = stats.get('PA') or 0
    h = stats.get('H') or 0
    bb = stats.get('BB') or 0
    sf = stats.get('SF') or 0  # Make sure SF is included
    oe = stats.get('OE') or 0  # Reached on Error
    doubles = stats.get('Doubles') or stats.get('2B') or 0
    triples = stats.get('Triples') or stats.get('3B') or 0
    hr = stats.get('HR') or 0
    
    # Calculate At Bats (PA - BB - SF) 
    ab = pa - bb - sf
    stats['AB'] = max(0, ab)  # Ensure non-negative
    
    # Calculate Batting Average (H / AB)
    if ab > 0:
        stats['AVG'] = round(h / ab, 3)
    else:
        stats['AVG'] = 0.000
    
    # Calculate On Base Percentage - Board decision to include OE (Reached on Error)
    # Standard formula is (H + BB) / PA, but D1 board decided to include OE
    if pa > 0:
        stats['OBP'] = round((h + bb + oe) / pa, 3)
    else:
        stats['OBP'] = 0.000
    
    # Calculate Slugging Percentage (Total Bases / AB)
    # Total Bases = H + 2B + (2×3B) + (3×HR)
    total_bases = h + doubles + (2 * triples) + (3 * hr)
    if ab > 0:
        stats['SLG'] = round(total_bases / ab, 3)
    else:
        stats['SLG'] = 0.000
    
    # Calculate OPS (On-base Plus Slugging)
    stats['OPS'] = round(stats['OBP'] + stats['SLG'], 3)
    
    return stats

def format_percentage(value):
    """Format percentage values - FIXED: Handle values >= 1.000 properly"""
    if value == 0:
        return ".000"
    elif value >= 1.000:
        return f"{value:.3f}"  # Keep the leading digit for 1.000+
    else:
        return f"{value:.3f}"[1:]  # Remove the leading 0 for values < 1.000


def get_season_sort_key(team_name):
    """
    Create sort key for team seasons (newest to oldest)
    Vipers F21 > Vipers S21 > Vipers W21 > Vipers F20 > etc.
    """
    if not team_name or len(team_name) < 3:
        return (0, 0, 0)
    
    # Extract season from team name (e.g., "Vipers F12" -> "F12")
    parts = team_name.split()
    if len(parts) < 2:
        return (0, 0, 0)
    
    season_part = parts[-1]  # Last part should be like "F12", "S21", etc.
    
    if len(season_part) < 3:
        return (0, 0, 0)
    
    season_type = season_part[0]  # F, S, or W
    try:
        year = int(season_part[1:])  # 12, 21, etc.
    except:
        return (0, 0, 0)
    
    # Season order within year: Fall=3, Summer=2, Winter=1
    season_order = {'F': 3, 'S': 2, 'W': 1}.get(season_type, 0)
    
    return (year, season_order, 0)

# Helper function to get season from date using Seasons table
def get_season_from_date_advanced(date_str, seasons_dict):
    """
    More sophisticated season detection using the Seasons table
    """
    if not date_str:
        return "Unknown"
    
    try:
        # For now, use the simple logic but we can enhance this
        # Parse date string (MM/DD/YY format from the data)
        if '/' in date_str:
            parts = date_str.split('/')
            month = int(parts[0])
            year_part = parts[2].split()[0]  # Remove time part
            year = int(year_part)
            
            # Convert 2-digit year to 4-digit
            if year < 50:
                year += 2000
            else:
                year += 1900
            
            # Determine season based on month
            if month in [12, 1, 2]:  # Winter
                season_year = year if month == 12 else year
                season_code = f"W{str(season_year)[-2:]}"
            elif month in [3, 4, 5, 6, 7, 8]:  # Summer  
                season_code = f"S{str(year)[-2:]}"
            else:  # Fall (9, 10, 11)
                season_code = f"F{str(year)[-2:]}"
            
            # Look up in seasons_dict to get the FilterNumber
            for filter_num, season_info in seasons_dict.items():
                if season_info['short_name'] == season_code:
                    return season_code
            
            return season_code
    except:
        return "Unknown"
    
    return "Unknown"

# Make calculate_batting_stats and format_percentage available in all templates
@app.context_processor
def utility_processor():
    return dict(
        calculate_batting_stats=calculate_batting_stats,
        format_percentage=format_percentage
    )

# Initialize database
def init_db():
    conn = get_db_connection()
    
    # Create tables based on your schema
    conn.execute('''
        CREATE TABLE IF NOT EXISTS "pitching_stats" (
            TeamNumber INTEGER,
            GameNumber INTEGER,
            PlayerNumber INTEGER,
            HomeTeam INTEGER,
            IP REAL,
            BB INTEGER,
            W INTEGER,
            L INTEGER,
            IBB INTEGER
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS "game_stats" (
            TeamNumber INTEGER,
            GameNumber INTEGER,
            GStatNumber INTEGER,
            Date TEXT,
            Innings INTEGER,
            HomeTeam INTEGER,
            Opponent TEXT,
            OpponentTeamNumber INTEGER,
            Runs INTEGER,
            RunsInning1 INTEGER,
            RunsInning2 INTEGER,
            RunsInning3 INTEGER,
            RunsInning4 INTEGER,
            RunsInning5 INTEGER,
            RunsInning6 INTEGER,
            RunsInning7 INTEGER,
            RunsInning8 INTEGER,
            RunsInning9 INTEGER,
            OppRuns INTEGER,
            OppRunsInning1 INTEGER,
            OppRunsInning2 INTEGER,
            OppRunsInning3 INTEGER,
            OppRunsInning4 INTEGER,
            OppRunsInning5 INTEGER,
            OppRunsInning6 INTEGER,
            OppRunsInning7 INTEGER,
            OppRunsInning8 INTEGER,
            OppRunsInning9 INTEGER
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS "batting_stats" (
            TeamNumber INTEGER,
            GameNumber INTEGER,
            PlayerNumber INTEGER,
            HomeTeam INTEGER,
            PA INTEGER,
            R INTEGER,
            H INTEGER,
            "2B" INTEGER,
            "3B" INTEGER,
            HR INTEGER,
            OE INTEGER,
            BB INTEGER,
            RBI INTEGER,
            SF INTEGER DEFAULT 0,
            G INTEGER
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS "Teams" (
            TeamNumber INTEGER PRIMARY KEY,
            LongTeamName TEXT,
            Manager TEXT
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS "Seasons" (
            "FilterNumber" TEXT,
            "season_name" TEXT,
            short_name TEXT
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS "People" (
            PersonNumber INTEGER PRIMARY KEY,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            player_id INTEGER
        )
    ''')
    
    conn.commit()
    conn.close()

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Players section
@app.route('/players')
def players():
    conn = get_db_connection()
    
    # Get all players with career stats (exclude subs)
    query = '''
        SELECT 
            p.PersonNumber,
            p.FirstName,
            p.LastName,
            SUM(b.G) as Games,
            SUM(b.PA) as PA,
            SUM(b.R) as R,
            SUM(b.H) as H,
            SUM(b."2B") as Doubles,
            SUM(b."3B") as Triples,
            SUM(b.HR) as HR,
            SUM(b.BB) as BB,
            SUM(b.RBI) as RBI,
            SUM(b.SF) as SF,
            SUM(b.OE) as OE
        FROM People p
        LEFT JOIN batting_stats b ON p.PersonNumber = b.PlayerNumber
        WHERE p.LastName != 'Subs'
            AND p.FirstName NOT LIKE '%Sub%' 
            AND p.LastName NOT LIKE '%Sub%'
            AND p.FirstName != 'Sub'
            AND p.LastName != 'Sub'
            AND LOWER(p.FirstName) NOT LIKE '%substitute%'
            AND LOWER(p.LastName) NOT LIKE '%substitute%'
        GROUP BY p.PersonNumber, p.FirstName, p.LastName
        HAVING SUM(b.PA) > 0
        ORDER BY SUM(b.G) DESC, p.LastName, p.FirstName
    '''
    
    raw_players = conn.execute(query).fetchall()
    conn.close()
    
    # Calculate stats for each player
    players = []
    for player in raw_players:
        player_stats = calculate_batting_stats(dict(player))
        players.append(player_stats)
    
    return render_template('players.html', players=players)



@app.route('/player/<int:player_id>')
def player_detail(player_id):
    conn = get_db_connection()
    
    # Get player info
    player = conn.execute('''
        SELECT PersonNumber, FirstName, LastName 
        FROM People 
        WHERE PersonNumber = ?
    ''', (player_id,)).fetchone()
    
    if not player:
        return "Player not found", 404
    
    # Get season lookup for creating links
    seasons_lookup = {}
    seasons_data = conn.execute('SELECT FilterNumber, short_name FROM Seasons').fetchall()
    for season in seasons_data:
        seasons_lookup[season['short_name']] = season['FilterNumber']
    
    # Get career batting stats - ONLY individual games (G = 1)
    career_query = '''
        SELECT 
            SUM(G) as Games,
            SUM(PA) as PA,
            SUM(R) as R,
            SUM(H) as H,
            SUM("2B") as Doubles,
            SUM("3B") as Triples,
            SUM(HR) as HR,
            SUM(BB) as BB,
            SUM(RBI) as RBI,
            SUM(SF) as SF,
            SUM(OE) as OE
        FROM batting_stats
        WHERE PlayerNumber = ?
    '''
    
    career_batting = conn.execute(career_query, (player_id,)).fetchone()
    career_stats = calculate_batting_stats(dict(career_batting)) if career_batting else {}
    
    # Get individual batting records
    records_query = '''
        SELECT 
            b.TeamNumber,
            t.LongTeamName,
            b.G as Games,
            b.PA,
            b.R,
            b.H,
            b."2B" as Doubles,
            b."3B" as Triples,
            b.HR,
            b.BB,
            b.RBI,
            b.SF,
            b.OE
        FROM batting_stats b
        JOIN Teams t ON b.TeamNumber = t.TeamNumber
        WHERE b.PlayerNumber = ?
        ORDER BY t.LongTeamName DESC
    '''
    
    individual_records = conn.execute(records_query, (player_id,)).fetchall()
    
    # Group records by team and add season FilterNumbers
    teams_data = {}
    for record in individual_records:
        team_name = record['LongTeamName']
        team_number = record['TeamNumber']
        
        # Extract season code from team name (like "F24", "W25", etc.)
        season_match = re.search(r'([A-Z]\d{2})$', team_name)
        season_filter_number = None
        if season_match:
            season_code = season_match.group(1)
            season_filter_number = seasons_lookup.get(season_code)
        
        if team_name not in teams_data:
            teams_data[team_name] = {
                'team_number': team_number,
                'season_filter_number': season_filter_number,
                'individual_records': [],
                'aggregated_records': []
            }
        
        if record['Games'] > 1:
            teams_data[team_name]['aggregated_records'].append(dict(record))
        else:
            teams_data[team_name]['individual_records'].append(dict(record))
    
    # Calculate team totals for teams with individual games
    individual_teams = []
    aggregated_teams = []
    
    for team_name, team_data in teams_data.items():
        if team_data['individual_records']:
            # Has individual game data - sum them up
            team_total = {
                'Games': 0, 'PA': 0, 'R': 0, 'H': 0, 'Doubles': 0,
                'Triples': 0, 'HR': 0, 'BB': 0, 'RBI': 0, 'SF': 0, 'OE': 0
            }
            for record in team_data['individual_records']:
                for key in team_total:
                    team_total[key] += record.get(key, 0)
            
            team_stats = calculate_batting_stats(team_total)
            team_stats['team_name'] = team_name
            team_stats['team_number'] = team_data['team_number']
            team_stats['season_filter_number'] = team_data['season_filter_number']
            individual_teams.append(team_stats)
        
        if team_data['aggregated_records']:
            # Has aggregated records - these are season totals
            for record in team_data['aggregated_records']:
                team_stats = calculate_batting_stats(dict(record))
                team_stats['team_name'] = team_name
                team_stats['team_number'] = team_data['team_number']
                team_stats['season_filter_number'] = team_data['season_filter_number']
                aggregated_teams.append(team_stats)
    
    # Sort both lists by season (newest to oldest)
    individual_teams.sort(key=lambda x: get_season_sort_key(x['team_name']), reverse=True)
    aggregated_teams.sort(key=lambda x: get_season_sort_key(x['team_name']), reverse=True)
    
    # Calculate total seasons
    total_seasons = len(individual_teams) + len(aggregated_teams)
    
    # Get pitching stats if any
    pitching_query = '''
        SELECT 
            COUNT(*) as Games,
            SUM(IP) as IP,
            SUM(BB) as BB,
            SUM(W) as W,
            SUM(L) as L,
            SUM(IBB) as IBB
        FROM pitching_stats
        WHERE PlayerNumber = ? AND IP <= 9
    '''
    
    pitching_stats = conn.execute(pitching_query, (player_id,)).fetchone()
    
    conn.close()
    
    return render_template('player_detail.html', 
                         player=player, 
                         career_stats=career_stats,
                         team_list=individual_teams,
                         aggregated_teams=aggregated_teams,
                         total_seasons=total_seasons,
                         pitching_stats=pitching_stats)


# Player_games route
@app.route('/player/<int:player_id>/games')
def player_games(player_id):
    conn = get_db_connection()
    
    # Get player info
    player = conn.execute('''
        SELECT PersonNumber, FirstName, LastName 
        FROM People 
        WHERE PersonNumber = ?
    ''', (player_id,)).fetchone()
    
    if not player:
        return "Player not found", 404
    
    # Get career stats for summary
    career_query = '''
        SELECT 
            SUM(G) as Games,
            SUM(PA) as PA,
            SUM(R) as R,
            SUM(H) as H,
            SUM("2B") as Doubles,
            SUM("3B") as Triples,
            SUM(HR) as HR,
            SUM(BB) as BB,
            SUM(RBI) as RBI,
            SUM(SF) as SF,
            SUM(OE) as OE
        FROM batting_stats
        WHERE PlayerNumber = ?
    '''
    
    career_batting = conn.execute(career_query, (player_id,)).fetchone()
    career_stats = calculate_batting_stats(dict(career_batting)) if career_batting else {}
    
    # Get seasons lookup  
    seasons_data = conn.execute('SELECT FilterNumber, season_name, short_name FROM Seasons').fetchall()
    seasons_dict = {row['FilterNumber']: {'season_name': row['season_name'], 'short_name': row['short_name']} for row in seasons_data}
    
    # Get game logs with opposing pitcher info (USING OPPONENTGSTATNUMBER)
    games_query = '''
        SELECT 
            g.Date,
            g.Opponent,
            g.Runs,
            g.OppRuns,
            g.OpponentTeamNumber,
            g.GameNumber,
            CASE 
                WHEN g.Runs > g.OppRuns THEN 'W'
                WHEN g.Runs < g.OppRuns THEN 'L'
                ELSE 'T'
            END as Result,
            b.PA,
            b.R,
            b.H,
            b."2B" as Doubles,
            b."3B" as Triples,
            b.HR,
            b.BB,
            b.RBI,
            b.SF,
            b.OE,
            -- Get opposing pitcher who got the decision
            opp_pitcher.FirstName as OppPitcherFirst,
            opp_pitcher.LastName as OppPitcherLast,
            opp_pitcher.PlayerNumber as OppPitcherNumber
        FROM batting_stats b
        JOIN game_stats g ON b.TeamNumber = g.TeamNumber AND b.GameNumber = g.GameNumber
        LEFT JOIN (
            -- Find opposing pitcher using OpponentGStatNumber - SIMPLE AND RELIABLE
            SELECT 
                ps.PlayerNumber,
                opp_game.GStatNumber,
                p.FirstName,
                p.LastName
            FROM pitching_stats ps
            JOIN People p ON ps.PlayerNumber = p.PersonNumber
            JOIN game_stats opp_game ON ps.TeamNumber = opp_game.TeamNumber AND ps.GameNumber = opp_game.GameNumber
            WHERE (ps.W > 0 OR ps.L > 0)
        ) opp_pitcher ON g.OpponentGStatNumber = opp_pitcher.GStatNumber
        WHERE b.PlayerNumber = ? AND b.G = 1
        ORDER BY 
            CASE 
                WHEN substr(g.Date, 7, 2) < '50' THEN '20' || substr(g.Date, 7, 2)
                ELSE '19' || substr(g.Date, 7, 2)
            END DESC,
            substr(g.Date, 1, 2) DESC,
            substr(g.Date, 4, 2) DESC
    '''
    
    raw_games = conn.execute(games_query, (player_id,)).fetchall()
    
    # Calculate stats for each game
    games = []
    
    for game in raw_games:
        game_stats = calculate_batting_stats(dict(game))
        game_stats['season'] = get_season_from_date_advanced(game['Date'], seasons_dict)
        game_stats['score'] = f"{game['Runs']}-{game['OppRuns']}"
        
        # Clean opponent name and format opposing pitcher
        game_stats['Opponent'] = re.sub(r'\s+[A-Z]\d{2}$', '', game['Opponent'])
        
        if game['OppPitcherFirst'] and game['OppPitcherLast']:
            game_stats['OppPitcher'] = f"{game['OppPitcherFirst']} {game['OppPitcherLast']}"
            game_stats['OppPitcherNumber'] = game['OppPitcherNumber']
        else:
            # Use team name + Subs for games without recorded pitcher
            clean_opponent = re.sub(r'\s+[A-Z]\d{2}$', '', game['Opponent'])
            game_stats['OppPitcher'] = f"{clean_opponent} Subs"
            game_stats['OppPitcherNumber'] = None
            
        # Format date to remove time
        if game['Date']:
            game_stats['Date'] = game['Date'].split()[0]
        games.append(game_stats)
    
    conn.close()
    
    return render_template('player_games.html', 
                         player=player,
                         games=games,
                         career_stats=career_stats)
# Seasons Route
@app.route('/seasons')
def seasons():
    conn = get_db_connection()
    
    # Get all seasons with basic info
    seasons_query = '''
        SELECT 
            s.FilterNumber,
            s.season_name,
            s.short_name,
            s.Champion,
            COUNT(DISTINCT t.TeamNumber) as num_teams
        FROM Seasons s
        LEFT JOIN Teams t ON t.LongTeamName LIKE '%' || s.short_name || '%'
        GROUP BY s.FilterNumber, s.season_name, s.short_name, s.Champion
        ORDER BY 
            CASE 
                WHEN s.short_name LIKE '%08' THEN 2008
                WHEN s.short_name LIKE '%09' THEN 2009
                WHEN s.short_name LIKE '%10' THEN 2010
                WHEN s.short_name LIKE '%11' THEN 2011
                WHEN s.short_name LIKE '%12' THEN 2012
                WHEN s.short_name LIKE '%13' THEN 2013
                WHEN s.short_name LIKE '%14' THEN 2014
                WHEN s.short_name LIKE '%15' THEN 2015
                WHEN s.short_name LIKE '%16' THEN 2016
                WHEN s.short_name LIKE '%17' THEN 2017
                WHEN s.short_name LIKE '%18' THEN 2018
                WHEN s.short_name LIKE '%19' THEN 2019
                WHEN s.short_name LIKE '%20' THEN 2020
                WHEN s.short_name LIKE '%21' THEN 2021
                WHEN s.short_name LIKE '%22' THEN 2022
                WHEN s.short_name LIKE '%23' THEN 2023
                WHEN s.short_name LIKE '%24' THEN 2024
                WHEN s.short_name LIKE '%25' THEN 2025
                ELSE 0
            END DESC,
            CASE 
                WHEN s.short_name LIKE 'F%' THEN 3
                WHEN s.short_name LIKE 'S%' THEN 2  
                WHEN s.short_name LIKE 'W%' THEN 1
                ELSE 0
            END DESC
    '''
    
    seasons_data = conn.execute(seasons_query).fetchall()
    
    # Get overall league statistics
    overall_stats = conn.execute('''
        SELECT 
            COUNT(DISTINCT s.FilterNumber) as total_seasons,
            COUNT(DISTINCT t.TeamNumber) as total_teams,
            COUNT(DISTINCT g.GameNumber) as total_games,
            COUNT(DISTINCT p.PersonNumber) as total_players
        FROM Seasons s
        LEFT JOIN Teams t ON t.LongTeamName LIKE '%' || s.short_name || '%'
        LEFT JOIN game_stats g ON g.TeamNumber = t.TeamNumber
        LEFT JOIN batting_stats b ON b.TeamNumber = t.TeamNumber
        LEFT JOIN People p ON p.PersonNumber = b.PlayerNumber
        WHERE p.LastName != 'Subs' OR p.LastName IS NULL
    ''').fetchone()
    
    conn.close()
    
    return render_template('seasons.html', 
                         seasons=seasons_data,
                         overall_stats=overall_stats)



@app.route('/season/<filter_number>')
def season_detail(filter_number):
    conn = get_db_connection()
    
    # Get season info
    season = conn.execute('''
        SELECT * FROM Seasons WHERE FilterNumber = ?
    ''', (filter_number,)).fetchone()
    
    if not season:
        return "Season not found", 404
    
    # Get teams for this season with their records


    teams_query = '''
        SELECT 
            t.TeamNumber,
            t.LongTeamName,
            t.Manager,
            COUNT(CASE WHEN g.Runs > g.OppRuns THEN 1 END) as Wins,
            COUNT(CASE WHEN g.Runs < g.OppRuns THEN 1 END) as Losses,
            SUM(g.Runs) as RunsScored,
            SUM(g.OppRuns) as RunsAllowed
        FROM Teams t
        LEFT JOIN game_stats g ON t.TeamNumber = g.TeamNumber
        WHERE t.LongTeamName LIKE '%' || ? || '%'
        GROUP BY t.TeamNumber, t.LongTeamName, t.Manager
        ORDER BY Wins DESC, (SUM(g.Runs) - SUM(g.OppRuns)) DESC
    '''
    
    teams_raw = conn.execute(teams_query, (season['short_name'],)).fetchall()
    

    # Process teams to add display names and detect divisions
    teams = []
    has_divisions = False
    divisions = {}
    
    for team in teams_raw:
        team_dict = dict(team)
        team_name = team_dict['LongTeamName']
        
        # Remove season codes (any format like W25, F24, S22, etc.)
        team_name = re.sub(r'\s+[A-Z]\d{2}$', '', team_name)            
        team_dict['team_display_name'] = team_name
            
        # Check for ANY divisions in parentheses
        division_match = re.search(r'\(([^)]+)\)', team_name)
        if division_match:
            has_divisions = True
            division_name = division_match.group(1)  # Extract what's inside parentheses
                
            if division_name not in divisions:
                divisions[division_name] = []
            divisions[division_name].append(team_dict)
        
        teams.append(team_dict)
        
    # Calculate Games Behind within divisions
    if has_divisions:
        for division_name, division_teams in divisions.items():
            # Sort by wins desc, then run differential
            division_teams.sort(key=lambda x: (x['Wins'], (x['RunsScored'] or 0) - (x['RunsAllowed'] or 0)), reverse=True)
            
            if division_teams:
                leader_wins = division_teams[0]['Wins']
                leader_losses = division_teams[0]['Losses']
                
                for team in division_teams:
                    # Calculate winning percentage
                    total_games = team['Wins'] + team['Losses']
                    if total_games > 0:
                        team['Pct'] = round(team['Wins'] / total_games, 3)
                    else:
                        team['Pct'] = 0.000
                    
                    # Calculate Games Behind
                    if team['Wins'] == leader_wins and team['Losses'] == leader_losses:
                        team['GB'] = '-'
                    else:
                        gb = ((leader_wins - team['Wins']) + (team['Losses'] - leader_losses)) / 2.0
                        team['GB'] = f"{gb:.1f}" if gb % 1 != 0 else str(int(gb))
    else:
        # Single division - calculate GB and Pct
        teams.sort(key=lambda x: (x['Wins'], (x['RunsScored'] or 0) - (x['RunsAllowed'] or 0)), reverse=True)
        if teams:
            leader_wins = teams[0]['Wins']
            leader_losses = teams[0]['Losses']
            
            for team in teams:
                # Calculate winning percentage
                total_games = team['Wins'] + team['Losses']
                if total_games > 0:
                    team['Pct'] = round(team['Wins'] / total_games, 3)
                else:
                    team['Pct'] = 0.000
                    
                # Calculate Games Behind
                if team['Wins'] == leader_wins and team['Losses'] == leader_losses:
                    team['GB'] = '-'
                else:
                    gb = ((leader_wins - team['Wins']) + (team['Losses'] - leader_losses)) / 2.0
                    team['GB'] = f"{gb:.1f}" if gb % 1 != 0 else str(int(gb))

    
    # Get season stats for calculating minimum PA
    season_stats = conn.execute('''
        SELECT 
            COUNT(DISTINCT g.GameNumber) as TotalGames,
            COUNT(DISTINCT p.PersonNumber) as TotalPlayers,
            SUM(b.HR) as TotalHRs
        FROM game_stats g
        JOIN Teams t ON g.TeamNumber = t.TeamNumber
        LEFT JOIN batting_stats b ON b.TeamNumber = t.TeamNumber AND b.GameNumber = g.GameNumber
        LEFT JOIN People p ON p.PersonNumber = b.PlayerNumber
        WHERE t.LongTeamName LIKE '%' || ? || '%'
            AND (p.LastName != 'Subs' OR p.LastName IS NULL)
    ''', (season['short_name'],)).fetchone()

    
    total_games = season_stats['TotalGames'] or 0
    min_pa_for_leaders = int(total_games * 2.5)
    

    
    # Get batting leaders
    batting_leaders_query = '''
        SELECT 
            p.PersonNumber, p.FirstName, p.LastName, t.LongTeamName,
            SUM(b.PA) as PA, SUM(b.H) as H, SUM(b.BB) as BB, SUM(b.SF) as SF
        FROM People p
        JOIN batting_stats b ON p.PersonNumber = b.PlayerNumber
        JOIN Teams t ON b.TeamNumber = t.TeamNumber
        WHERE t.LongTeamName LIKE '%' || ? || '%'
            AND p.LastName != 'Subs'
        GROUP BY p.PersonNumber, p.FirstName, p.LastName, t.LongTeamName
        HAVING SUM(b.PA) >= ?
        ORDER BY CAST(SUM(b.H) AS FLOAT) / SUM(b.PA - b.BB - b.SF) DESC
        LIMIT 10
    '''
    
   
    batting_leaders_raw = conn.execute(batting_leaders_query, (season['short_name'], min_pa_for_leaders)).fetchall()
    

    # Process batting leaders
    batting_leaders = []
    for player in batting_leaders_raw:
        player_dict = calculate_batting_stats(dict(player))
        team_name = player_dict['LongTeamName']
        # Remove season codes (any format like W25, F24, S22, etc.)
        team_name = re.sub(r'\s+[A-Z]\d{2}$', '', team_name)
        player_dict['team_display_name'] = team_name
        batting_leaders.append(player_dict)
    

    
    # Get HR leaders
    hr_leaders_query = '''
        SELECT 
            p.PersonNumber, p.FirstName, p.LastName, t.LongTeamName, SUM(b.HR) as HR
        FROM People p
        JOIN batting_stats b ON p.PersonNumber = b.PlayerNumber
        JOIN Teams t ON b.TeamNumber = t.TeamNumber
        WHERE t.LongTeamName LIKE '%' || ? || '%'
            AND p.LastName != 'Subs'
        GROUP BY p.PersonNumber, p.FirstName, p.LastName, t.LongTeamName
        HAVING SUM(b.HR) > 0
        ORDER BY SUM(b.HR) DESC
        LIMIT 5
    '''
    
    hr_leaders_raw = conn.execute(hr_leaders_query, (season['short_name'],)).fetchall()

    # Process HR leaders
    hr_leaders = []
    for player in hr_leaders_raw:
        player_dict = dict(player)
        team_name = player_dict['LongTeamName']
        # Remove season codes (any format like W25, F24, S22, etc.)
        team_name = re.sub(r'\s+[A-Z]\d{2}$', '', team_name)
        player_dict['team_display_name'] = team_name
        hr_leaders.append(player_dict)
    

    return render_template('season_detail.html', 
                            season=season, 
                            teams=teams,
                            divisions=divisions if has_divisions else None,
                            has_divisions=has_divisions,
                            total_teams=len(teams),
                            batting_leaders=batting_leaders,  # Use the variable!
                            hr_leaders=hr_leaders,           # Use the variable!
                            season_stats=season_stats,       # Use the variable!
                            min_pa_for_leaders=min_pa_for_leaders,  # Use the variable!
                            league_avg='.000')

# Season Batting Stats Route
@app.route('/season/<filter_number>/batting')
def season_batting(filter_number):
    """Season-specific batting statistics page"""
    
    conn = get_db_connection()
    
    # Get season info
    season = conn.execute('''
        SELECT * FROM Seasons WHERE FilterNumber = ?
    ''', (filter_number,)).fetchone()
    
    if not season:
        conn.close()
        return "Season not found", 404
    
    # Get games played for this season (using same pattern as season_detail)
    season_stats = conn.execute('''
        SELECT 
            COUNT(DISTINCT g.GameNumber) as TotalGames,
            COUNT(DISTINCT p.PersonNumber) as TotalPlayers,
            SUM(b.HR) as TotalHRs
        FROM game_stats g
        JOIN Teams t ON g.TeamNumber = t.TeamNumber
        LEFT JOIN batting_stats b ON b.TeamNumber = t.TeamNumber AND b.GameNumber = g.GameNumber
        LEFT JOIN People p ON p.PersonNumber = b.PlayerNumber
        WHERE t.LongTeamName LIKE '%' || ? || '%'
            AND (p.LastName != 'Subs' OR p.LastName IS NULL)
    ''', (season['short_name'],)).fetchone()
    
    games_played = season_stats['TotalGames'] if season_stats else 0
    qualified_pa_threshold = int(games_played * 2.5)
    
    # Get all batting stats for players in this season (using same pattern as season_detail)
    batting_query = '''
        SELECT 
            p.PersonNumber,
            p.FirstName,
            p.LastName,
            SUM(b.G) as Games,
            SUM(b.PA) as PA,
            SUM(b.R) as R,
            SUM(b.H) as H,
            SUM(b."2B") as Doubles,
            SUM(b."3B") as Triples,
            SUM(b.HR) as HR,
            SUM(b.BB) as BB,
            SUM(b.RBI) as RBI,
            SUM(b.SF) as SF,
            SUM(b.OE) as OE
        FROM People p
        JOIN batting_stats b ON p.PersonNumber = b.PlayerNumber
        JOIN Teams t ON b.TeamNumber = t.TeamNumber
        WHERE t.LongTeamName LIKE '%' || ? || '%'
            AND p.LastName != 'Subs'
        GROUP BY p.PersonNumber, p.FirstName, p.LastName
        HAVING SUM(b.G) > 0
    '''
    
    raw_players = conn.execute(batting_query, (season['short_name'],)).fetchall()
    
    # Calculate batting averages and sort by OBP
    players = []
    for player in raw_players:
        player_stats = calculate_batting_stats(dict(player))
        players.append(player_stats)
    
    # Sort by OBP (descending), then PA (descending)
    players.sort(key=lambda x: (x.get('OBP', 0), x.get('PA', 0)), reverse=True)
    
    conn.close()
    
    return render_template('season_batting.html',
                         season=season,
                         players=players,
                         qualified_pa_threshold=qualified_pa_threshold,
                         season_filter_number=filter_number)












# Season Rosters Route
@app.route('/team/<int:team_number>')
def team_detail(team_number):
    conn = get_db_connection()
    
    # Get team info
    team = conn.execute('''
        SELECT TeamNumber, LongTeamName, Manager 
        FROM Teams 
        WHERE TeamNumber = ?
    ''', (team_number,)).fetchone()
    
    if not team:
        return "Team not found", 404
    
    # Clean team display name
    team_display_name = re.sub(r'\s+[A-Z]\d{2}$', '', team['LongTeamName'])
    

    # Get team roster with stats (INCLUDING Subs)
    roster_query = '''
        SELECT 
            p.PersonNumber,
            p.FirstName,
            p.LastName,
            SUM(b.G) as Games,
            SUM(b.PA) as PA,
            SUM(b.R) as R,
            SUM(b.H) as H,
            SUM(b."2B") as Doubles,
            SUM(b."3B") as Triples,
            SUM(b.HR) as HR,
            SUM(b.BB) as BB,
            SUM(b.RBI) as RBI,
            SUM(b.SF) as SF,
            SUM(b.OE) as OE,
            CASE WHEN p.LastName = 'Subs' OR p.FirstName LIKE '%Sub%' THEN 1 ELSE 0 END as IsSub
        FROM People p
        JOIN batting_stats b ON p.PersonNumber = b.PlayerNumber
        WHERE b.TeamNumber = ? 
        GROUP BY p.PersonNumber, p.FirstName, p.LastName
        ORDER BY 
            CASE WHEN p.LastName = 'Subs' OR p.FirstName LIKE '%Sub%' THEN 1 ELSE 0 END,
            CAST(SUM(b.H + b.BB + b.OE) AS FLOAT) / SUM(b.PA) DESC
    '''
    
    roster_raw = conn.execute(roster_query, (team_number,)).fetchall()
    
    # Calculate stats for each player
    roster = []
    for player in roster_raw:
        player_stats = calculate_batting_stats(dict(player))
        roster.append(player_stats)
    
    # Get game results
    results_query = '''
        SELECT 
            g.GameNumber,
            g.Date,
            g.Opponent,
            g.Runs,
            g.OppRuns,
            CASE 
                WHEN g.Runs > g.OppRuns THEN 'W'
                WHEN g.Runs < g.OppRuns THEN 'L'
                ELSE 'T'
            END as Result
        FROM game_stats g
        WHERE g.TeamNumber = ?
        ORDER BY g.Date DESC
    '''
    results_raw = conn.execute(results_query, (team_number,)).fetchall()

    results = []
    for game in results_raw:
        game_dict = dict(game)
        # Clean opponent name - remove season codes like F24, W25, S22, etc.
        opponent_name = game_dict['Opponent']
        clean_opponent = re.sub(r'\s+[A-Z]\d{2}$', '', opponent_name)
        game_dict['Opponent'] = clean_opponent
        results.append(game_dict)
    

    # Get season info for breadcrumbs
    season_code = re.search(r'([A-Z]\d{2})$', team['LongTeamName'])
    season_filter_number = None
    season_name = None
    if season_code:
        season_data = conn.execute('''
            SELECT FilterNumber, season_name FROM Seasons WHERE short_name = ?
        ''', (season_code.group(1),)).fetchone()
        if season_data:
            season_filter_number = season_data['FilterNumber']
            season_name = season_data['season_name']
    
    conn.close()
    return render_template('team_detail.html',
                        team=team,
                        team_display_name=team_display_name,
                        roster=roster,
                        results=results,
                        season_filter_number=season_filter_number,
                        season_name=season_name)


@app.route('/boxscore/<int:team_number>/<int:game_number>')
def boxscore(team_number, game_number):
    conn = get_db_connection()
    
    # Get game info
    game = conn.execute('''
        SELECT * FROM game_stats 
        WHERE TeamNumber = ? AND GameNumber = ?
    ''', (team_number, game_number)).fetchone()
    
    if not game:
        return "Game not found", 404
    
    # Get home team info
    home_team = conn.execute('''
        SELECT t.TeamNumber, t.LongTeamName, t.Manager
        FROM Teams t
        WHERE t.TeamNumber = ?
    ''', (team_number,)).fetchone()
    
    # Get opponent team directly using OpponentTeamNumber - NO string matching needed!
    opponent_team = None
    opponent_game_number = None

    if game['OpponentTeamNumber']:
        # Get opponent team info directly
        opponent_team = conn.execute('''
            SELECT TeamNumber, LongTeamName, Manager
            FROM Teams 
            WHERE TeamNumber = ?
        ''', (game['OpponentTeamNumber'],)).fetchone()
        
        if opponent_team:
            # Find opponent's GameNumber for this same date by matching our team as their opponent
            opponent_game_record = conn.execute('''
                SELECT GameNumber 
                FROM game_stats 
                WHERE TeamNumber = ? 
                  AND Date = ?
                  AND OpponentTeamNumber = ?
            ''', (opponent_team['TeamNumber'], game['Date'], team_number)).fetchone()
            
            if opponent_game_record:
                opponent_game_number = opponent_game_record['GameNumber']

    # Clean team names - remove season codes from BOTH teams
    import re
    home_team_name = re.sub(r'\s+[A-Z]\d{2}$', '', home_team['LongTeamName'])
    opponent_team_name = re.sub(r'\s+[A-Z]\d{2}$', '', game['Opponent'])

    # Get batting stats for home team (INCLUDING Subs for totals)
    home_batting_all = conn.execute('''
        SELECT 
            p.FirstName, p.LastName, p.PersonNumber,
            b.PA, b.R, b.H, b."2B" as Doubles, b."3B" as Triples, 
            b.HR, b.RBI, b.BB, b.OE, b.SF,
            CASE WHEN p.LastName = 'Subs' OR p.FirstName LIKE '%Sub%' THEN 1 ELSE 0 END as IsSub
        FROM People p
        JOIN batting_stats b ON p.PersonNumber = b.PlayerNumber
        WHERE b.TeamNumber = ? AND b.GameNumber = ? AND b.G = 1
        ORDER BY 
            CASE WHEN p.LastName = 'Subs' OR p.FirstName LIKE '%Sub%' THEN 1 ELSE 0 END,
            b.PA DESC, p.LastName
    ''', (team_number, game_number)).fetchall()

    # Get batting stats for opponent team (using their GameNumber)
    opponent_batting_all = []
    if opponent_team and opponent_game_number:
        opponent_batting_all = conn.execute('''
            SELECT 
                p.FirstName, p.LastName, p.PersonNumber,
                b.PA, b.R, b.H, b."2B" as Doubles, b."3B" as Triples,
                b.HR, b.RBI, b.BB, b.OE, b.SF,
                CASE WHEN p.LastName = 'Subs' OR p.FirstName LIKE '%Sub%' THEN 1 ELSE 0 END as IsSub
            FROM People p
            JOIN batting_stats b ON p.PersonNumber = b.PlayerNumber
            WHERE b.TeamNumber = ? AND b.GameNumber = ? AND b.G = 1
            ORDER BY 
                CASE WHEN p.LastName = 'Subs' OR p.FirstName LIKE '%Sub%' THEN 1 ELSE 0 END,
                b.PA DESC, p.LastName
        ''', (opponent_team['TeamNumber'], opponent_game_number)).fetchall()

    # Calculate batting stats and team totals for home team
    home_batting_stats = []
    home_team_totals = {'PA': 0, 'R': 0, 'H': 0, 'Doubles': 0, 'Triples': 0, 'HR': 0, 'RBI': 0, 'BB': 0, 'OE': 0, 'SF': 0}

    for player in home_batting_all:
        stats = calculate_batting_stats(dict(player))
        home_batting_stats.append(stats)
        
        # Add to team totals
        for key in home_team_totals:
            home_team_totals[key] += (stats.get(key) or 0)

    # Calculate team totals stats
    home_team_totals = calculate_batting_stats(home_team_totals)

    # Calculate batting stats and team totals for opponent team
    opponent_batting_stats = []
    opponent_team_totals = {'PA': 0, 'R': 0, 'H': 0, 'Doubles': 0, 'Triples': 0, 'HR': 0, 'RBI': 0, 'BB': 0, 'OE': 0, 'SF': 0}

    for player in opponent_batting_all:
        stats = calculate_batting_stats(dict(player))
        opponent_batting_stats.append(stats)
        
        # Add to team totals
        for key in opponent_team_totals:
            opponent_team_totals[key] += (stats.get(key) or 0)

    # Calculate team totals stats
    opponent_team_totals = calculate_batting_stats(opponent_team_totals)

    # Get pitching stats for home team - INCLUDE Subs
    home_pitching = conn.execute('''
        SELECT 
            p.FirstName, p.LastName,
            ps.IP, ps.BB, ps.IBB, ps.W, ps.L,
            CASE WHEN p.LastName = 'Subs' OR p.FirstName LIKE '%Sub%' THEN 1 ELSE 0 END as IsSub
        FROM People p
        JOIN pitching_stats ps ON p.PersonNumber = ps.PlayerNumber
        WHERE ps.TeamNumber = ? AND ps.GameNumber = ? AND ps.IP > 0
        ORDER BY 
            CASE WHEN p.LastName = 'Subs' OR p.FirstName LIKE '%Sub%' THEN 1 ELSE 0 END,
            ps.IP DESC
    ''', (team_number, game_number)).fetchall()

    # Get pitching stats for opponent team (using their GameNumber)  
    opponent_pitching = []
    if opponent_team and opponent_game_number:
        opponent_pitching = conn.execute('''
            SELECT 
                p.FirstName, p.LastName,
                ps.IP, ps.BB, ps.IBB, ps.W, ps.L,
                CASE WHEN p.LastName = 'Subs' OR p.FirstName LIKE '%Sub%' THEN 1 ELSE 0 END as IsSub
            FROM People p
            JOIN pitching_stats ps ON p.PersonNumber = ps.PlayerNumber
            WHERE ps.TeamNumber = ? AND ps.GameNumber = ? AND ps.IP > 0
            ORDER BY 
                CASE WHEN p.LastName = 'Subs' OR p.FirstName LIKE '%Sub%' THEN 1 ELSE 0 END,
                ps.IP DESC
        ''', (opponent_team['TeamNumber'], opponent_game_number)).fetchall()

    # Get season info for breadcrumbs
    season_code = re.search(r'([A-Z]\d{2})$', home_team['LongTeamName'])
    season_filter_number = None
    season_name = None
    
    if season_code:
        season_data = conn.execute('''
            SELECT FilterNumber, season_name FROM Seasons WHERE short_name = ?
        ''', (season_code.group(1),)).fetchone()
        if season_data:
            season_filter_number = season_data['FilterNumber']
            season_name = season_data['season_name']
    
    conn.close()
    
    return render_template('boxscore.html',
                         game=game,
                         home_team=home_team,
                         opponent_team=opponent_team,
                         home_team_name=home_team_name,
                         opponent_team_name=opponent_team_name,
                         home_batting_stats=home_batting_stats,
                         opponent_batting_stats=opponent_batting_stats,
                         home_team_totals=home_team_totals,           
                         opponent_team_totals=opponent_team_totals,   
                         home_pitching=home_pitching,
                         opponent_pitching=opponent_pitching,
                         season_filter_number=season_filter_number,
                         season_name=season_name)


@app.route('/pitching')
def pitching():
    conn = get_db_connection()
    
    # Get all pitchers with career stats (exclude subs, only include those with actual pitching)
    query = '''
        SELECT 
            p.PersonNumber,
            p.FirstName,
            p.LastName,
            COUNT(*) as Games,
            SUM(ps.IP) as IP,
            SUM(ps.BB) as BB,
            SUM(ps.W) as W,
            SUM(ps.L) as L,
            SUM(ps.IBB) as IBB,
            CASE 
                WHEN SUM(ps.IP) > 0 
                THEN ROUND(CAST((SUM(ps.BB) - SUM(ps.IBB)) AS FLOAT) / SUM(ps.IP), 2)
                ELSE 0.00
            END as BB_per_IP,
            CASE 
                WHEN (SUM(ps.W) + SUM(ps.L)) > 0 
                THEN ROUND(CAST(SUM(ps.W) AS FLOAT) / (SUM(ps.W) + SUM(ps.L)), 3)
                ELSE 0.000
            END as Win_Pct
        FROM People p
        JOIN pitching_stats ps ON p.PersonNumber = ps.PlayerNumber
        WHERE p.LastName != 'Subs'
            AND p.FirstName NOT LIKE '%Sub%' 
            AND p.LastName NOT LIKE '%Sub%'
            AND p.FirstName != 'Sub'
            AND p.LastName != 'Sub'
            AND LOWER(p.FirstName) NOT LIKE '%substitute%'
            AND LOWER(p.LastName) NOT LIKE '%substitute%'
            AND ps.IP > 0
        GROUP BY p.PersonNumber, p.FirstName, p.LastName
        HAVING SUM(ps.IP) > 0
        ORDER BY COUNT(*) DESC, SUM(ps.IP) DESC, p.LastName, p.FirstName
    '''
    
    pitchers = conn.execute(query).fetchall()
    conn.close()
    
    return render_template('pitching.html', pitchers=pitchers)


# Add new pitcher detail route:
@app.route('/pitcher/<int:pitcher_id>')
def pitcher_detail(pitcher_id):
    conn = get_db_connection()
    
    # Get pitcher info
    pitcher = conn.execute('''
        SELECT PersonNumber, FirstName, LastName 
        FROM People 
        WHERE PersonNumber = ?
    ''', (pitcher_id,)).fetchone()
    
    if not pitcher:
        return "Pitcher not found", 404
    
    # Get season lookup for creating links
    seasons_lookup = {}
    seasons_data = conn.execute('SELECT FilterNumber, short_name FROM Seasons').fetchall()
    for season in seasons_data:
        seasons_lookup[season['short_name']] = season['FilterNumber']
    
    # Get career pitching stats
    career_query = '''
        SELECT 
            COUNT(*) as Games,
            SUM(IP) as IP,
            SUM(BB) as BB,
            SUM(W) as W,
            SUM(L) as L,
            SUM(IBB) as IBB
        FROM pitching_stats
        WHERE PlayerNumber = ? AND IP > 0
    '''
    
    career_pitching = conn.execute(career_query, (pitcher_id,)).fetchone()
    
    # Calculate career derived stats
    career_stats = dict(career_pitching) if career_pitching else {}
    if career_stats.get('IP', 0) > 0:
        career_stats['BB_per_IP'] = round((career_stats['BB'] - career_stats['IBB']) / career_stats['IP'], 2)
    else:
        career_stats['BB_per_IP'] = 0.00
        
    if (career_stats.get('W', 0) + career_stats.get('L', 0)) > 0:
        career_stats['Win_Pct'] = round(career_stats['W'] / (career_stats['W'] + career_stats['L']), 3)
    else:
        career_stats['Win_Pct'] = 0.000
    
    # Get season-by-season records
    records_query = '''
        SELECT 
            ps.TeamNumber,
            t.LongTeamName,
            COUNT(*) as Games,
            SUM(ps.IP) as IP,
            SUM(ps.BB) as BB,
            SUM(ps.W) as W,
            SUM(ps.L) as L,
            SUM(ps.IBB) as IBB
        FROM pitching_stats ps
        JOIN Teams t ON ps.TeamNumber = t.TeamNumber
        WHERE ps.PlayerNumber = ? AND ps.IP > 0
        GROUP BY ps.TeamNumber, t.LongTeamName
        ORDER BY t.LongTeamName DESC
    '''
    
    season_records_raw = conn.execute(records_query, (pitcher_id,)).fetchall()
    
    # Process season records
    season_records = []
    for record in season_records_raw:
        record_dict = dict(record)
        team_name = record_dict['LongTeamName']
        
        # Extract season code from team name
        season_match = re.search(r'([A-Z]\d{2})$', team_name)
        season_filter_number = None
        if season_match:
            season_code = season_match.group(1)
            season_filter_number = seasons_lookup.get(season_code)
        
        # Clean team name
        clean_team_name = re.sub(r'\s+[A-Z]\d{2}$', '', team_name)
        record_dict['team_display_name'] = clean_team_name
        record_dict['season_filter_number'] = season_filter_number
        
        # Calculate derived stats
        if record_dict['IP'] > 0:
            record_dict['BB_per_IP'] = round((record_dict['BB'] - record_dict['IBB']) / record_dict['IP'], 2)
        else:
            record_dict['BB_per_IP'] = 0.00
            
        if (record_dict['W'] + record_dict['L']) > 0:
            record_dict['Win_Pct'] = round(record_dict['W'] / (record_dict['W'] + record_dict['L']), 3)
        else:
            record_dict['Win_Pct'] = 0.000
        
        season_records.append(record_dict)
    
    # Sort by season (newest to oldest)
    season_records.sort(key=lambda x: get_season_sort_key(x['LongTeamName']), reverse=True)
    
    conn.close()
    
    return render_template('pitcher_detail.html', 
                         pitcher=pitcher, 
                         career_stats=career_stats,
                         season_records=season_records,
                         total_seasons=len(season_records))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False)