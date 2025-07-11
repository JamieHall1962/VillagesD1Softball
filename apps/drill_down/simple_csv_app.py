"""
Simple CSV-based D1 Softball Stats App
Reads directly from CSV files for easy development
"""

from flask import Flask, render_template, request, jsonify
import csv
from pathlib import Path
import os
from collections import defaultdict

app = Flask(__name__)

@app.template_filter('nostripleadingzero')
def nostripleadingzero(value):
    """Format a float as .xxx (no leading zero, always 3 decimals)"""
    try:
        return ('%.3f' % value).lstrip('0')
    except Exception:
        return value

# Data paths
DATA_DIR = Path(__file__).parent / 'data'
SITE_DIR = Path(__file__).parent / 'site'

def load_csv_data(filename):
    """Load CSV data and return as list of dictionaries"""
    filepath = DATA_DIR / filename
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

# Load CSV data
print("Loading CSV data...")
players_data = load_csv_data('People.csv')
batting_data = load_csv_data('BattingStats.csv')
pitching_data = load_csv_data('PitchingStats.csv')
games_data = load_csv_data('GameStats.csv')
teams_data = load_csv_data('Teams.csv')
filters_data = load_csv_data('Filters.csv')
print("Data loaded successfully!")

def safe_int(value, default=0):
    """Safely convert value to int"""
    try:
        return int(value) if value else default
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    """Safely convert value to float"""
    try:
        return float(value) if value else default
    except (ValueError, TypeError):
        return default

def calculate_player_stats(player_number, batting_data):
    """Calculate comprehensive stats for a player including U2 correction for games played"""
    player_batting = [row for row in batting_data if safe_int(row.get('PlayerNumber')) == player_number]
    if not player_batting:
        return None

    total_pa = sum(safe_int(row.get('PA', 0)) for row in player_batting)
    total_r = sum(safe_int(row.get('R', 0)) for row in player_batting)
    total_h = sum(safe_int(row.get('H', 0)) for row in player_batting)
    total_2b = sum(safe_int(row.get('D', 0)) for row in player_batting)
    total_3b = sum(safe_int(row.get('T', 0)) for row in player_batting)
    total_hr = sum(safe_int(row.get('HR', 0)) for row in player_batting)
    total_bb = sum(safe_int(row.get('BB', 0)) for row in player_batting)
    total_sf = sum(safe_int(row.get('SF', 0)) for row in player_batting)
    total_oe = sum(safe_int(row.get('OE', 0)) for row in player_batting)
    total_rbi = sum(safe_int(row.get('RBI', 0)) for row in player_batting)
    total_so = sum(safe_int(row.get('SO', 0)) for row in player_batting)
    total_tb = sum(safe_int(row.get('TB', 0)) for row in player_batting)
    if total_tb == 0:
        total_tb = total_h + total_2b + 2*total_3b + 3*total_hr
    total_hp = sum(safe_int(row.get('HP', 0)) for row in player_batting)
    total_sh = sum(safe_int(row.get('SH', 0)) for row in player_batting)
    total_1b = total_h - total_2b - total_3b - total_hr

    # Calculate at-bats (PA - BB - HP - SH - SF)
    total_ab = total_pa - total_bb - total_hp - total_sh - total_sf

    # Games played with U2 correction
    unique_games = len(set((safe_int(row.get('TeamNumber')), safe_int(row.get('GameNumber'))) for row in player_batting))
    total_u2 = sum(safe_int(row.get('U2', 0)) for row in player_batting)
    games_played = unique_games + total_u2

    # Averages
    avg = total_h / total_ab if total_ab > 0 else 0
    obp = (total_h + total_bb + total_hp) / total_pa if total_pa > 0 else 0
    slg = total_tb / total_ab if total_ab > 0 else 0

    return {
        'games_played': games_played,
        'pa': total_pa,
        'ab': total_ab,
        'r': total_r,
        'h': total_h,
        '1b': total_1b,
        '2b': total_2b,
        '3b': total_3b,
        'hr': total_hr,
        'rbi': total_rbi,
        'bb': total_bb,
        'sf': total_sf,
        'oe': total_oe,
        'tb': total_tb,
        'avg': avg,
        'slg': slg,
        'obp': obp,
        'so': total_so,
        'unique_games': unique_games,
        'u2_games': total_u2
    }

@app.route('/')
def index():
    """Main page"""
    return render_template('simple_index.html')

@app.route('/players')
def players():
    """Players list page"""
    players_data_list = []
    for player in players_data:
        if safe_int(player.get('PersonNumber')) == -7 or not player.get('PersonNumber'):
            continue
        
        # Skip players whose names end with "Subs" (team substitutes)
        player_name = f"{player.get('FirstName', '')} {player.get('LastName', '')}"
        if player_name.endswith('Subs'):
            continue
            
        stats = calculate_player_stats(safe_int(player.get('PersonNumber')), batting_data)
        if stats:
            players_data_list.append({
                'id': safe_int(player.get('PersonNumber')),
                'name': player_name,
                'games_played': stats['games_played'],
                'pa': stats['pa'],
                'ab': stats['ab'],
                'r': stats['r'],
                'h': stats['h'],
                '1b': stats['1b'],
                '2b': stats['2b'],
                '3b': stats['3b'],
                'hr': stats['hr'],
                'rbi': stats['rbi'],
                'bb': stats['bb'],
                'sf': stats['sf'],
                'oe': stats['oe'],
                'tb': stats['tb'],
                'avg': stats['avg'],
                'slg': stats['slg'],
                'obp': stats['obp'],
            })
    players_data_list.sort(key=lambda x: x['games_played'], reverse=True)
    return render_template('simple_players.html', players=players_data_list)

@app.route('/player/<int:player_id>')
def player_detail(player_id):
    """Individual player detail page"""
    
    # Find the player
    player = None
    for p in players_data:
        if safe_int(p.get('PersonNumber')) == player_id:
            player = p
            break
    
    if not player:
        return "Player not found", 404
    
    # Skip players whose names end with "Subs" (team substitutes)
    player_name = f"{player.get('FirstName', '')} {player.get('LastName', '')}"
    if player_name.endswith('Subs'):
        return "Player not found", 404
    
    stats = calculate_player_stats(player_id, batting_data)
    
    if not stats:
        return "No stats found for player", 404
    
    # Get team breakdown
    player_batting = [row for row in batting_data if safe_int(row.get('PlayerNumber')) == player_id]
    team_stats = []
    
    # Create season mapping
    season_to_filter = {}
    for row in filters_data:
        filter_num = safe_int(row.get('FilterNumber'))
        season_name_full = row.get('FilterName', '')
        
        # Convert "Winter 2011" to "W11"
        parts = season_name_full.split()
        if len(parts) >= 2:
            season_type = parts[0]  # Winter, Summer, Fall
            year = parts[1]  # 2011, 2012, etc.
            
            # Convert to short codes
            type_code = {'Winter': 'W', 'Summer': 'S', 'Fall': 'F'}.get(season_type, '')
            year_code = year[-2:]  # Last 2 digits of year
            
            if type_code and year_code:
                season_code = f"{type_code}{year_code}"
                season_to_filter[season_code] = filter_num
    
    # Group by team
    team_groups = defaultdict(list)
    for row in player_batting:
        team_num = safe_int(row.get('TeamNumber'))
        team_groups[team_num].append(row)
    
    for team_num, team_batting in team_groups.items():
        # Find team name
        team_name = f"Team {team_num}"
        for team in teams_data:
            if safe_int(team.get('TeamNumber')) == team_num:
                team_name = team.get('LongTeamName', f"Team {team_num}")
                break
        
        # Calculate team stats
        team_pa = sum(safe_int(row.get('PA', 0)) for row in team_batting)
        team_h = sum(safe_int(row.get('H', 0)) for row in team_batting)
        team_ab = sum(safe_int(row.get('PA', 0)) - safe_int(row.get('BB', 0)) - safe_int(row.get('HP', 0)) - safe_int(row.get('SH', 0)) - safe_int(row.get('SF', 0)) for row in team_batting)
        team_bb = sum(safe_int(row.get('BB', 0)) for row in team_batting)
        team_hp = sum(safe_int(row.get('HP', 0)) for row in team_batting)
        
        team_avg = team_h / team_ab if team_ab > 0 else 0
        team_obp = (team_h + team_bb + team_hp) / team_pa if team_pa > 0 else 0
        
        # Extract season code from team name
        season_code = None
        for word in team_name.split():
            if any(word.startswith(prefix) for prefix in ['W', 'S', 'F']) and len(word) == 3 and word[1:].isdigit():
                season_code = word
                break
        
        filter_number = season_to_filter.get(season_code, 0) if season_code else 0
        
        team_stats.append({
            'team_name': team_name,
            'team_number': team_num,
            'filter_number': filter_number,
            'season_code': season_code,
            'pa': team_pa,
            'h': team_h,
            'avg': team_avg,
            'obp': team_obp
        })
    
    # Sort by season (Winter first, then Summer, then Fall)
    def season_sort_key(team):
        if not team['season_code']:
            return (4, 0)  # Put unknown seasons last
        season_type = team['season_code'][0]
        year = int(team['season_code'][1:])
        type_order = {'W': 1, 'S': 2, 'F': 3}
        return (type_order.get(season_type, 4), year)
    
    team_stats.sort(key=season_sort_key, reverse=True)
    
    return render_template('player_detail.html', 
                         player=player, 
                         stats=stats, 
                         team_stats=team_stats)

@app.route('/seasons')
def seasons():
    """Seasons list page"""
    seasons_list = []
    for row in filters_data:
        filter_num = safe_int(row.get('FilterNumber'))
        season_name = row.get('FilterName', '')
        
        # Convert "Winter 2011" to "W11"
        parts = season_name.split()
        if len(parts) >= 2:
            season_type = parts[0]  # Winter, Summer, Fall
            year = parts[1]  # 2011, 2012, etc.
            
            # Convert to short codes
            type_code = {'Winter': 'W', 'Summer': 'S', 'Fall': 'F'}.get(season_type, '')
            year_code = year[-2:]  # Last 2 digits of year
            
            if type_code and year_code:
                season_code = f"{type_code}{year_code}"
                seasons_list.append({
                    'filter_number': filter_num,
                    'name': season_name,
                    'code': season_code
                })
    
    # Sort by season (Winter first, then Summer, then Fall)
    def season_sort_key(season):
        if not season['code']:
            return (4, 0)  # Put unknown seasons last
        season_type = season['code'][0]
        year = int(season['code'][1:])
        type_order = {'W': 1, 'S': 2, 'F': 3}
        return (type_order.get(season_type, 4), year)
    
    seasons_list.sort(key=season_sort_key, reverse=True)
    return render_template('seasons.html', seasons=seasons_list)

@app.route('/season/<int:filter_number>')
def season_detail(filter_number):
    """Season detail page with standings"""
    # Find the season
    season_info = None
    for row in filters_data:
        if safe_int(row.get('FilterNumber')) == filter_number:
            season_info = row
            break
    
    if not season_info:
        return "Season not found", 404
    
    season_name = season_info.get('FilterName', '')
    
    # Convert "Winter 2011" to "W11"
    parts = season_name.split()
    if len(parts) >= 2:
        season_type = parts[0]  # Winter, Summer, Fall
        year = parts[1]  # 2011, 2012, etc.
        
        # Convert to short codes
        type_code = {'Winter': 'W', 'Summer': 'S', 'Fall': 'F'}.get(season_type, '')
        year_code = year[-2:]  # Last 2 digits of year
        
        if type_code and year_code:
            season_code = f"{type_code}{year_code}"
        else:
            season_code = None
    else:
        season_code = None
    
    # Get teams for this season
    season_teams = []
    for team in teams_data:
        team_name = team.get('LongTeamName', '')
        # Check if team name contains the season code
        if season_code and season_code in team_name:
            season_teams.append(team)
    
    # Calculate standings for each team
    standings = []
    for team in season_teams:
        team_num = safe_int(team.get('TeamNumber'))
        team_name = team.get('LongTeamName', f"Team {team_num}")
        
        # Get team games
        team_games = [row for row in games_data if safe_int(row.get('TeamNumber')) == team_num]
        
        # Calculate wins, losses, runs
        wins = 0
        losses = 0
        runs_for = 0
        runs_against = 0
        
        for game in team_games:
            team_score = safe_int(game.get('TeamScore', 0))
            opponent_score = safe_int(game.get('OpponentScore', 0))
            
            runs_for += team_score
            runs_against += opponent_score
            
            if team_score > opponent_score:
                wins += 1
            elif team_score < opponent_score:
                losses += 1
        
        # Calculate team batting stats
        team_batting = [row for row in batting_data if safe_int(row.get('TeamNumber')) == team_num]
        
        total_pa = sum(safe_int(row.get('PA', 0)) for row in team_batting)
        total_h = sum(safe_int(row.get('H', 0)) for row in team_batting)
        total_bb = sum(safe_int(row.get('BB', 0)) for row in team_batting)
        total_hp = sum(safe_int(row.get('HP', 0)) for row in team_batting)
        total_ab = sum(safe_int(row.get('PA', 0)) - safe_int(row.get('BB', 0)) - safe_int(row.get('HP', 0)) - safe_int(row.get('SH', 0)) - safe_int(row.get('SF', 0)) for row in team_batting)
        total_2b = sum(safe_int(row.get('D', 0)) for row in team_batting)
        total_3b = sum(safe_int(row.get('T', 0)) for row in team_batting)
        total_hr = sum(safe_int(row.get('HR', 0)) for row in team_batting)
        total_tb = sum(safe_int(row.get('TB', 0)) for row in team_batting)
        if total_tb == 0:
            total_tb = total_h + total_2b + 2*total_3b + 3*total_hr
        
        games_played = wins + losses
        win_pct = wins / games_played if games_played > 0 else 0
        ba = total_h / total_ab if total_ab > 0 else 0
        obp = (total_h + total_bb + total_hp) / total_pa if total_pa > 0 else 0
        slg = total_tb / total_ab if total_ab > 0 else 0
        rpg = runs_for / games_played if games_played > 0 else 0
        rpg_against = runs_against / games_played if games_played > 0 else 0
        run_diff = runs_for - runs_against
        
        standings.append({
            'team_name': team_name,
            'team_number': team_num,
            'wins': wins,
            'losses': losses,
            'win_pct': win_pct,
            'runs_for': runs_for,
            'runs_against': runs_against,
            'run_diff': run_diff,
            'rpg': rpg,
            'rpg_against': rpg_against,
            'ba': ba,
            'obp': obp,
            'slg': slg,
            'hr': total_hr,
            'games_played': games_played
        })
    
    # Sort by winning percentage
    standings.sort(key=lambda x: x['win_pct'], reverse=True)
    
    # Calculate games back
    if standings:
        first_place_wins = standings[0]['wins']
        first_place_losses = standings[0]['losses']
        
        for team in standings:
            team_wins = team['wins']
            team_losses = team['losses']
            
            if first_place_wins + first_place_losses > 0:
                gb = ((first_place_wins - team_wins) + (team_losses - first_place_losses)) / 2
                team['gb'] = gb
            else:
                team['gb'] = 0
    
    # Check for divisions
    divisions = {}
    for team in standings:
        team_name = team['team_name']
        # Look for division in parentheses
        if '(' in team_name and ')' in team_name:
            start = team_name.find('(')
            end = team_name.find(')')
            division = team_name[start+1:end]
            if division != 'D1/2':  # Skip combined division notation
                if division not in divisions:
                    divisions[division] = []
                divisions[division].append(team)
        else:
            if 'No Division' not in divisions:
                divisions['No Division'] = []
            divisions['No Division'].append(team)
    
    # Special handling for S15, S16, S17
    if season_code in ['S15', 'S16', 'S17']:
        special_note = "Note: This season had combined D1/D2 divisions. Only D1 player stats were recorded."
    else:
        special_note = None
    
    return render_template('season_detail.html', 
                         season=season_info, 
                         standings=standings, 
                         divisions=divisions,
                         special_note=special_note)

@app.route('/team/<int:team_number>/<int:filter_number>')
def team_detail(team_number, filter_number):
    """Team detail page with roster and stats"""
    # Find the team
    team = None
    for t in teams_data:
        if safe_int(t.get('TeamNumber')) == team_number:
            team = t
            break
    
    if not team:
        return "Team not found", 404
    
    team_name = team.get('LongTeamName', f"Team {team_number}")
    
    # Get team batting stats
    team_batting = [row for row in batting_data if safe_int(row.get('TeamNumber')) == team_number]
    
    # Group by player
    player_stats = defaultdict(lambda: {
        'pa': 0, 'ab': 0, 'r': 0, 'h': 0, '1b': 0, '2b': 0, '3b': 0, 'hr': 0, 'rbi': 0,
        'bb': 0, 'sf': 0, 'oe': 0, 'tb': 0, 'so': 0, 'games': set()
    })
    
    for row in team_batting:
        player_num = safe_int(row.get('PlayerNumber'))
        player_stats[player_num]['pa'] += safe_int(row.get('PA', 0))
        player_stats[player_num]['r'] += safe_int(row.get('R', 0))
        player_stats[player_num]['h'] += safe_int(row.get('H', 0))
        player_stats[player_num]['2b'] += safe_int(row.get('D', 0))
        player_stats[player_num]['3b'] += safe_int(row.get('T', 0))
        player_stats[player_num]['hr'] += safe_int(row.get('HR', 0))
        player_stats[player_num]['rbi'] += safe_int(row.get('RBI', 0))
        player_stats[player_num]['bb'] += safe_int(row.get('BB', 0))
        player_stats[player_num]['sf'] += safe_int(row.get('SF', 0))
        player_stats[player_num]['oe'] += safe_int(row.get('OE', 0))
        player_stats[player_num]['so'] += safe_int(row.get('SO', 0))
        player_stats[player_num]['tb'] += safe_int(row.get('TB', 0))
        
        # Track unique games
        game_key = (safe_int(row.get('TeamNumber')), safe_int(row.get('GameNumber')))
        player_stats[player_num]['games'].add(game_key)
    
    # Calculate final stats for each player
    roster = []
    for player_num, stats in player_stats.items():
        # Find player name
        player_name = f"Player {player_num}"
        for player in players_data:
            if safe_int(player.get('PersonNumber')) == player_num:
                player_name = f"{player.get('FirstName', '')} {player.get('LastName', '')}"
                break
        
        # Skip players whose names end with "Subs"
        if player_name.endswith('Subs'):
            continue
        
        # Calculate derived stats
        games_played = len(stats['games'])
        total_ab = stats['pa'] - stats['bb'] - 0 - 0 - stats['sf']  # No HP in softball
        stats['1b'] = stats['h'] - stats['2b'] - stats['3b'] - stats['hr']
        
        if stats['tb'] == 0:
            stats['tb'] = stats['h'] + stats['2b'] + 2*stats['3b'] + 3*stats['hr']
        
        avg = stats['h'] / total_ab if total_ab > 0 else 0
        obp = (stats['h'] + stats['bb']) / stats['pa'] if stats['pa'] > 0 else 0
        slg = stats['tb'] / total_ab if total_ab > 0 else 0
        
        roster.append({
            'player_number': player_num,
            'name': player_name,
            'games_played': games_played,
            'pa': stats['pa'],
            'ab': total_ab,
            'r': stats['r'],
            'h': stats['h'],
            '1b': stats['1b'],
            '2b': stats['2b'],
            '3b': stats['3b'],
            'hr': stats['hr'],
            'rbi': stats['rbi'],
            'bb': stats['bb'],
            'sf': stats['sf'],
            'oe': stats['oe'],
            'tb': stats['tb'],
            'avg': avg,
            'obp': obp,
            'slg': slg,
            'so': stats['so']
        })
    
    # Sort by OBP
    roster.sort(key=lambda x: x['obp'], reverse=True)
    
    return render_template('team_detail.html', 
                         team=team, 
                         roster=roster, 
                         filter_number=filter_number)

@app.route('/team/<int:team_number>/<int:filter_number>/games')
def team_games(team_number, filter_number):
    """Team game results page"""
    # Find the team
    team = None
    for t in teams_data:
        if safe_int(t.get('TeamNumber')) == team_number:
            team = t
            break
    
    if not team:
        return "Team not found", 404
    
    team_name = team.get('LongTeamName', f"Team {team_number}")
    
    # Get team games
    team_games = [row for row in games_data if safe_int(row.get('TeamNumber')) == team_number]
    
    # Process games
    games_list = []
    wins = 0
    losses = 0
    
    for game in team_games:
        game_date = game.get('GameDate', '')
        opponent = game.get('Opponent', '')
        team_score = safe_int(game.get('TeamScore', 0))
        opponent_score = safe_int(game.get('OpponentScore', 0))
        is_home = game.get('HomeAway', '') == 'H'
        
        if team_score > opponent_score:
            result = 'W'
            wins += 1
        elif team_score < opponent_score:
            result = 'L'
            losses += 1
        else:
            result = 'T'
        
        games_list.append({
            'date': game_date,
            'opponent': opponent,
            'team_score': team_score,
            'opponent_score': opponent_score,
            'result': result,
            'is_home': is_home
        })
    
    # Sort by date
    games_list.sort(key=lambda x: x['date'])
    
    win_pct = wins / (wins + losses) if (wins + losses) > 0 else 0
    
    return render_template('team_games.html', 
                         team=team, 
                         games=games_list, 
                         wins=wins, 
                         losses=losses, 
                         win_pct=win_pct,
                         filter_number=filter_number)

@app.route('/player/<int:player_id>/games')
def player_games(player_id):
    """Player game log page"""
    # Find the player
    player = None
    for p in players_data:
        if safe_int(p.get('PersonNumber')) == player_id:
            player = p
            break
    
    if not player:
        return "Player not found", 404
    
    player_name = f"{player.get('FirstName', '')} {player.get('LastName', '')}"
    
    # Get player batting stats
    player_batting = [row for row in batting_data if safe_int(row.get('PlayerNumber')) == player_id]
    
    # Get team info for each game
    games_list = []
    for row in player_batting:
        team_num = safe_int(row.get('TeamNumber'))
        game_num = safe_int(row.get('GameNumber'))
        
        # Find team name
        team_name = f"Team {team_num}"
        for team in teams_data:
            if safe_int(team.get('TeamNumber')) == team_num:
                team_name = team.get('LongTeamName', f"Team {team_num}")
                break
        
        # Find game info
        game_info = None
        for game in games_data:
            if safe_int(game.get('TeamNumber')) == team_num and safe_int(game.get('GameNumber')) == game_num:
                game_info = game
                break
        
        if game_info:
            game_date = game_info.get('GameDate', '')
            opponent = game_info.get('Opponent', '')
            team_score = safe_int(game_info.get('TeamScore', 0))
            opponent_score = safe_int(game_info.get('OpponentScore', 0))
            is_home = game_info.get('HomeAway', '') == 'H'
            
            if team_score > opponent_score:
                result = 'W'
            elif team_score < opponent_score:
                result = 'L'
            else:
                result = 'T'
        else:
            game_date = ''
            opponent = ''
            team_score = 0
            opponent_score = 0
            is_home = False
            result = ''
        
        # Calculate game stats
        pa = safe_int(row.get('PA', 0))
        ab = pa - safe_int(row.get('BB', 0)) - 0 - 0 - safe_int(row.get('SF', 0))  # No HP in softball
        h = safe_int(row.get('H', 0))
        r = safe_int(row.get('R', 0))
        rbi = safe_int(row.get('RBI', 0))
        bb = safe_int(row.get('BB', 0))
        so = safe_int(row.get('SO', 0))
        
        avg = h / ab if ab > 0 else 0
        obp = (h + bb) / pa if pa > 0 else 0
        
        games_list.append({
            'date': game_date,
            'team_name': team_name,
            'opponent': opponent,
            'result': result,
            'pa': pa,
            'ab': ab,
            'h': h,
            'r': r,
            'rbi': rbi,
            'bb': bb,
            'so': so,
            'avg': avg,
            'obp': obp,
            'team_score': team_score,
            'opponent_score': opponent_score,
            'is_home': is_home
        })
    
    # Sort by date
    games_list.sort(key=lambda x: x['date'])
    
    # Calculate W/L record
    wins = sum(1 for game in games_list if game['result'] == 'W')
    losses = sum(1 for game in games_list if game['result'] == 'L')
    ties = sum(1 for game in games_list if game['result'] == 'T')
    total_games = wins + losses + ties
    win_pct = wins / total_games if total_games > 0 else 0
    
    return render_template('player_games.html', 
                         player=player, 
                         games=games_list, 
                         wins=wins, 
                         losses=losses, 
                         ties=ties, 
                         win_pct=win_pct)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False) 