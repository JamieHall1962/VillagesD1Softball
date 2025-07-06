"""
Simple CSV-based D1 Softball Stats App
Reads directly from CSV files for easy development
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
from pathlib import Path
import os

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

# Load CSV data
print("Loading CSV data...")
players_df = pd.read_csv(DATA_DIR / 'People.csv')
batting_df = pd.read_csv(DATA_DIR / 'BattingStats.csv')
pitching_df = pd.read_csv(DATA_DIR / 'PitchingStats.csv')
games_df = pd.read_csv(DATA_DIR / 'GameStats.csv')
teams_df = pd.read_csv(DATA_DIR / 'Teams.csv')
print("Data loaded successfully!")

def load_data():
    """Load CSV data files"""
    data_dir = 'data'
    
    # Load main data files
    batting_df = pd.read_csv(os.path.join(data_dir, 'BattingStats.csv'))
    people_df = pd.read_csv(os.path.join(data_dir, 'People.csv'))
    teams_df = pd.read_csv(os.path.join(data_dir, 'Teams.csv'))
    
    return batting_df, people_df, teams_df

def calculate_player_stats(player_number, batting_df):
    """Calculate comprehensive stats for a player including U2 correction for games played"""
    player_batting = batting_df[batting_df['PlayerNumber'] == player_number]
    if len(player_batting) == 0:
        return None

    total_pa = player_batting['PA'].sum()
    total_r = player_batting['R'].sum()
    total_h = player_batting['H'].sum()
    total_2b = player_batting['D'].sum() if 'D' in player_batting.columns else 0
    total_3b = player_batting['T'].sum() if 'T' in player_batting.columns else 0
    total_hr = player_batting['HR'].sum()
    total_bb = player_batting['BB'].sum()
    total_sf = player_batting['SF'].sum() if 'SF' in player_batting.columns else 0
    total_oe = player_batting['OE'].sum() if 'OE' in player_batting.columns else 0
    total_rbi = player_batting['RBI'].sum()
    total_so = player_batting['SO'].sum() if 'SO' in player_batting.columns else 0
    total_tb = player_batting['TB'].sum() if 'TB' in player_batting.columns else (
        total_h + total_2b + 2*total_3b + 3*total_hr)
    total_hp = player_batting['HP'].sum() if 'HP' in player_batting.columns else 0
    total_sh = player_batting['SH'].sum() if 'SH' in player_batting.columns else 0
    total_1b = total_h - total_2b - total_3b - total_hr

    # Calculate at-bats (PA - BB - HP - SH - SF)
    total_ab = total_pa - total_bb - total_hp - total_sh - total_sf

    # Games played with U2 correction
    unique_games = len(player_batting.groupby(['TeamNumber', 'GameNumber']))
    total_u2 = player_batting['U2'].sum() if 'U2' in player_batting.columns else 0
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
    batting_df, people_df, teams_df = load_data()
    players_data = []
    for _, player in people_df.iterrows():
        if pd.isna(player['PersonNumber']) or player['PersonNumber'] == -7:
            continue
        
        # Skip players whose names end with "Subs" (team substitutes)
        player_name = f"{player['FirstName']} {player['LastName']}"
        if player_name.endswith('Subs'):
            continue
            
        stats = calculate_player_stats(player['PersonNumber'], batting_df)
        if stats:
            players_data.append({
                'id': int(player['PersonNumber']),
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
    players_data.sort(key=lambda x: x['games_played'], reverse=True)
    return render_template('simple_players.html', players=players_data)

@app.route('/player/<int:player_id>')
def player_detail(player_id):
    """Individual player detail page"""
    batting_df, people_df, teams_df = load_data()
    
    # Find the player
    player = people_df[people_df['PersonNumber'] == player_id]
    if len(player) == 0:
        return "Player not found", 404
    
    player = player.iloc[0]
    
    # Skip players whose names end with "Subs" (team substitutes)
    player_name = f"{player['FirstName']} {player['LastName']}"
    if player_name.endswith('Subs'):
        return "Player not found", 404
    
    stats = calculate_player_stats(player_id, batting_df)
    
    if not stats:
        return "No stats found for player", 404
    
    # Get team breakdown
    player_batting = batting_df[batting_df['PlayerNumber'] == player_id]
    team_stats = []
    
    # Load filters to get season mapping
    filters_df = pd.read_csv('data/Filters.csv')
    season_to_filter = {}
    for _, row in filters_df.iterrows():
        filter_num = row['FilterNumber']
        season_name_full = row['FilterName']
        
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
    
    for team_num in player_batting['TeamNumber'].unique():
        team_batting = player_batting[player_batting['TeamNumber'] == team_num]
        
        # Find team name
        team_info = teams_df[teams_df['TeamNumber'] == team_num]
        if len(team_info) > 0:
            team_name = team_info.iloc[0]['LongTeamName']
        else:
            team_name = f"Team {team_num}"
        
        # Calculate team stats
        team_unique_games = len(team_batting.groupby('GameNumber'))
        team_u2 = team_batting['U2'].sum() if 'U2' in team_batting.columns else 0
        team_games = team_unique_games + team_u2
        
        # Calculate all stats for this team
        team_pa = team_batting['PA'].sum()
        team_r = team_batting['R'].sum()
        team_h = team_batting['H'].sum()
        team_2b = team_batting['D'].sum() if 'D' in team_batting.columns else 0
        team_3b = team_batting['T'].sum() if 'T' in team_batting.columns else 0
        team_hr = team_batting['HR'].sum()
        team_rbi = team_batting['RBI'].sum()
        team_bb = team_batting['BB'].sum()
        team_sh = team_batting['SH'].sum() if 'SH' in team_batting.columns else 0
        team_sf = team_batting['SF'].sum() if 'SF' in team_batting.columns else 0
        team_oe = team_batting['OE'].sum() if 'OE' in team_batting.columns else 0
        team_1b = team_h - team_2b - team_3b - team_hr
        
        # Calculate at-bats (PA - BB - SH - SF)
        team_ab = team_pa - team_bb - team_sh - team_sf
        team_tb = team_h + team_2b + 2*team_3b + 3*team_hr
        
        # Calculate averages
        team_avg = team_h / team_ab if team_ab > 0 else 0
        team_obp = (team_h + team_bb) / team_pa if team_pa > 0 else 0
        team_slg = team_tb / team_ab if team_ab > 0 else 0
        
        # Extract season from team name (e.g., "Avalanche W11" -> "W11")
        season_part = team_name.split()[-1] if ' ' in team_name else ''
        
        # Get filter number for this season
        filter_number = season_to_filter.get(season_part, None)
        
        team_stats.append({
            'team_number': int(team_num),
            'team_name': team_name,
            'season': season_part,
            'filter_number': filter_number,
            'games_played': team_games,
            'pa': team_pa,
            'ab': team_ab,
            'r': team_r,
            'h': team_h,
            '1b': team_1b,
            '2b': team_2b,
            '3b': team_3b,
            'hr': team_hr,
            'rbi': team_rbi,
            'bb': team_bb,
            'sf': team_sf,
            'oe': team_oe,
            'tb': team_tb,
            'avg': team_avg,
            'slg': team_slg,
            'obp': team_obp,
            'unique_games': team_unique_games,
            'u2_games': team_u2
        })
    
    # Sort teams by season (newest first - W16, S16, F16, W15, S15, F15, etc.)
    def season_sort_key(team):
        season = team['season']
        if not season:
            return '0000'  # Put teams without season info at the end
        
        # Extract year and season type
        if len(season) >= 2:
            year = season[-2:]  # Last 2 digits
            season_type = season[:-2]  # W, S, F
            
            # Season type priority: W (Winter) = 1, S (Summer) = 2, F (Fall) = 3
            # Winter starts the year in January, so it's the first season
            type_priority = {'W': 1, 'S': 2, 'F': 3}.get(season_type, 0)
            
            return f"{year}{type_priority:01d}"
        return '0000'
    
    team_stats.sort(key=season_sort_key, reverse=True)
    
    return render_template('player_detail.html', 
                         player=player, 
                         stats=stats, 
                         team_stats=team_stats)

@app.route('/seasons')
def seasons():
    """Seasons list page"""
    # Load seasons from Filters.csv
    filters_df = pd.read_csv('data/Filters.csv')
    
    seasons_data = []
    for _, row in filters_df.iterrows():
        seasons_data.append({
            'filter_number': int(row['FilterNumber']),
            'season_name': row['FilterName']
        })
    
    # Sort by season name (newest first)
    def season_sort_key(season):
        name = season['season_name']
        # Extract year and season type
        parts = name.split()
        if len(parts) >= 2:
            season_type = parts[0]  # Winter, Summer, Fall
            year = parts[1]  # 2011, 2012, etc.
            
            # Season type priority: Winter = 1, Summer = 2, Fall = 3
            type_priority = {'Winter': 1, 'Summer': 2, 'Fall': 3}.get(season_type, 0)
            
            return f"{year}{type_priority:01d}"
        return '0000'
    
    seasons_data.sort(key=season_sort_key, reverse=True)
    
    return render_template('seasons.html', seasons=seasons_data)

@app.route('/season/<int:filter_number>')
def season_detail(filter_number):
    """Individual season detail page - shows standings for that season"""
    batting_df, people_df, teams_df = load_data()
    
    # Find the season
    filters_df = pd.read_csv('data/Filters.csv')
    season_info = filters_df[filters_df['FilterNumber'] == filter_number]
    if len(season_info) == 0:
        return "Season not found", 404
    
    season_info = season_info.iloc[0]
    season_name = season_info['FilterName']
    
    # Create mapping from season codes to FilterNumbers
    season_to_filter = {}
    for _, row in filters_df.iterrows():
        filter_num = row['FilterNumber']
        season_name_full = row['FilterName']
        
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
    
    # Find the season code for this filter number
    target_season_code = None
    for season_code, filter_num in season_to_filter.items():
        if filter_num == filter_number:
            target_season_code = season_code
            break
    
    if not target_season_code:
        return "Season mapping not found", 404
    
    # Load game data for standings
    game_df = pd.read_csv('data/GameStats.csv')
    
    # Filter teams by season
    teams_data = []
    
    for _, team in teams_df.iterrows():
        team_num = team['TeamNumber']
        team_name = team['LongTeamName']
        
        # Check if this team belongs to the selected season
        if ' ' in team_name:
            # Handle team names like "Angels S15 (D1/2)" - we need to extract "S15"
            parts = team_name.split()
            # Look for the season code (W11, S11, F11, etc.) in the parts
            team_season_code = None
            for part in parts:
                if len(part) == 3 and part[0] in ['W', 'S', 'F'] and part[1:].isdigit():
                    team_season_code = part
                    break
            
            if team_season_code != target_season_code:
                continue  # Skip teams from other seasons
        
        # Get team batting data
        team_batting = batting_df[batting_df['TeamNumber'] == team_num]
        
        # Get team game data for standings
        team_games = game_df[game_df['TeamNumber'] == team_num]
        
        # Calculate standings
        wins = 0
        losses = 0
        runs_for = 0
        runs_against = 0
        
        for _, game in team_games.iterrows():
            runs = game['Runs']
            opp_runs = game['OppRuns']
            
            runs_for += runs
            runs_against += opp_runs
            
            if runs > opp_runs:
                wins += 1
            else:
                losses += 1
        
        if len(team_batting) > 0:
            games_played = wins + losses
            win_pct = wins / games_played if games_played > 0 else 0
            run_diff = runs_for - runs_against
            rpg = runs_for / games_played if games_played > 0 else 0
            rpg_allowed = runs_against / games_played if games_played > 0 else 0
            
            # Calculate team batting stats
            team_pa = team_batting['PA'].sum()
            team_hits = team_batting['H'].sum()
            team_hr = team_batting['HR'].sum()
            team_bb = team_batting['BB'].sum()
            team_sf = team_batting['SF'].sum() if 'SF' in team_batting.columns else 0
            team_sh = team_batting['SH'].sum() if 'SH' in team_batting.columns else 0
            
            # Calculate doubles and triples
            team_doubles = team_batting['D'].sum() if 'D' in team_batting.columns else 0
            team_triples = team_batting['T'].sum() if 'T' in team_batting.columns else 0
            
            # Calculate at-bats and total bases
            team_ab = team_pa - team_bb - team_sh - team_sf
            team_singles = team_hits - team_doubles - team_triples - team_hr
            team_tb = team_singles + 2*team_doubles + 3*team_triples + 4*team_hr
            
            # Calculate averages
            team_ba = team_hits / team_ab if team_ab > 0 else 0
            team_obp = (team_hits + team_bb) / team_pa if team_pa > 0 else 0
            team_slg = team_tb / team_ab if team_ab > 0 else 0
            
            teams_data.append({
                'team_number': int(team_num),
                'team_name': team_name,
                'wins': wins,
                'losses': losses,
                'games_played': games_played,
                'win_pct': win_pct,
                'runs_for': runs_for,
                'runs_against': runs_against,
                'run_diff': run_diff,
                'rpg': rpg,
                'rpg_allowed': rpg_allowed,
                'ba': team_ba,
                'obp': team_obp,
                'slg': team_slg,
                'hr': team_hr
            })
    
    # Sort by winning percentage (descending), then by run differential as tiebreaker
    teams_data.sort(key=lambda x: (x['win_pct'], x['run_diff']), reverse=True)
    
    # Check if this season has divisions
    divisions = {}
    for team in teams_data:
        team_name = team['team_name']
        # Look for division in parentheses: "Team Name (Division) Season"
        if '(' in team_name and ')' in team_name:
            # Extract division name from parentheses
            start = team_name.find('(')
            end = team_name.find(')')
            if start < end:
                division = team_name[start+1:end]
                # Skip D1/2 notation - this is not a division, just player composition info
                if division != 'D1/2':
                    if division not in divisions:
                        divisions[division] = []
                    divisions[division].append(team)
    
    # If we found divisions, organize teams by division
    if divisions:
        # Calculate games back within each division
        for division_name, division_teams in divisions.items():
            # Sort division teams by winning percentage
            division_teams.sort(key=lambda x: (x['win_pct'], x['run_diff']), reverse=True)
            
            # Calculate games back within division
            if division_teams:
                first_place_wins = division_teams[0]['wins']
                first_place_losses = division_teams[0]['losses']
                
                for team in division_teams:
                    if team['wins'] == first_place_wins and team['losses'] == first_place_losses:
                        team['games_back'] = 0.0
                    else:
                        games_back = ((first_place_wins - team['wins']) + (team['losses'] - first_place_losses)) / 2
                        team['games_back'] = games_back
        
        return render_template('season_detail.html', 
                             season_name=season_name,
                             filter_number=filter_number,
                             divisions=divisions,
                             teams=None)
    else:
        # No divisions - calculate games back for all teams together
        if teams_data:
            first_place_wins = teams_data[0]['wins']
            first_place_losses = teams_data[0]['losses']
            
            for team in teams_data:
                if team['wins'] == first_place_wins and team['losses'] == first_place_losses:
                    team['games_back'] = 0.0
                else:
                    games_back = ((first_place_wins - team['wins']) + (team['losses'] - first_place_losses)) / 2
                    team['games_back'] = games_back
        
        return render_template('season_detail.html', 
                             season_name=season_name,
                             filter_number=filter_number,
                             divisions=None,
                             teams=teams_data)

@app.route('/team/<int:team_number>/<int:filter_number>')
def team_detail(team_number, filter_number):
    """Team detail page for a specific season"""
    batting_df, people_df, teams_df = load_data()
    
    # Find the team
    team = teams_df[teams_df['TeamNumber'] == team_number]
    if len(team) == 0:
        return "Team not found", 404
    
    team = team.iloc[0]
    
    # Find the season
    filters_df = pd.read_csv('data/Filters.csv')
    season_info = filters_df[filters_df['FilterNumber'] == filter_number]
    if len(season_info) == 0:
        return "Season not found", 404
    
    season_info = season_info.iloc[0]
    season_name = season_info['FilterName']
    
    # Get team batting data
    team_batting = batting_df[batting_df['TeamNumber'] == team_number]
    
    if len(team_batting) == 0:
        return "No data found for team", 404
    
    # Calculate team totals
    team_totals = {
        'pa': team_batting['PA'].sum(),
        'h': team_batting['H'].sum(),
        'hr': team_batting['HR'].sum(),
        'rbi': team_batting['RBI'].sum(),
        'unique_games': len(team_batting.groupby('GameNumber')),
        'u2_games': team_batting['U2'].sum()
    }
    team_totals['total_games'] = team_totals['unique_games'] + team_totals['u2_games']
    
    # Get player stats for this team
    players_data = []
    
    for player_num in team_batting['PlayerNumber'].unique():
        player_batting = team_batting[team_batting['PlayerNumber'] == player_num]
        
        # Find player name
        player_info = people_df[people_df['PersonNumber'] == player_num]
        if len(player_info) > 0:
            player_name = f"{player_info.iloc[0]['FirstName']} {player_info.iloc[0]['LastName']}"
        else:
            player_name = f"Player {player_num}"
        
        # Skip substitute players
        if player_name.endswith('Subs'):
            continue
        
        # Calculate full player stats for this team
        player_unique_games = len(player_batting.groupby('GameNumber'))
        
        # Get all the standard stats
        pa = player_batting['PA'].sum()
        r = player_batting['R'].sum()
        h = player_batting['H'].sum()
        d = player_batting['D'].sum() if 'D' in player_batting.columns else 0
        t = player_batting['T'].sum() if 'T' in player_batting.columns else 0
        hr = player_batting['HR'].sum()
        rbi = player_batting['RBI'].sum()
        bb = player_batting['BB'].sum()
        sh = player_batting['SH'].sum() if 'SH' in player_batting.columns else 0
        sf = player_batting['SF'].sum() if 'SF' in player_batting.columns else 0
        oe = player_batting['OE'].sum() if 'OE' in player_batting.columns else 0
        
        # Calculate derived stats
        singles = h - d - t - hr
        ab = pa - bb - sh - sf
        tb = singles + 2*d + 3*t + 4*hr
        
        # Calculate averages
        avg = h / ab if ab > 0 else 0
        obp = (h + bb) / pa if pa > 0 else 0
        slg = tb / ab if ab > 0 else 0
        
        players_data.append({
            'player_number': int(player_num),
            'name': player_name,
            'games_played': player_unique_games,
            'pa': pa,
            'ab': ab,
            'r': r,
            'h': h,
            '1b': singles,
            '2b': d,
            '3b': t,
            'hr': hr,
            'rbi': rbi,
            'bb': bb,
            'sf': sf,
            'oe': oe,
            'tb': tb,
            'avg': avg,
            'obp': obp,
            'slg': slg
        })
    
    # Sort by OBP (descending) by default
    players_data.sort(key=lambda x: x['obp'], reverse=True)
    
    return render_template('team_detail.html', 
                         team=team,
                         season_name=season_name,
                         filter_number=filter_number,
                         totals=team_totals, 
                         players=players_data)

@app.route('/team/<int:team_number>/<int:filter_number>/games')
def team_games(team_number, filter_number):
    """Team games page - shows all games for a team in a specific season"""
    batting_df, people_df, teams_df = load_data()
    game_df = pd.read_csv('data/GameStats.csv')
    
    # Find the team
    team = teams_df[teams_df['TeamNumber'] == team_number]
    if len(team) == 0:
        return "Team not found", 404
    
    team = team.iloc[0]
    
    # Find the season
    filters_df = pd.read_csv('data/Filters.csv')
    season_info = filters_df[filters_df['FilterNumber'] == filter_number]
    if len(season_info) == 0:
        return "Season not found", 404
    
    season_info = season_info.iloc[0]
    season_name = season_info['FilterName']
    
    # Get team games for this season
    team_games = game_df[game_df['TeamNumber'] == team_number]
    
    if len(team_games) == 0:
        return "No games found for team", 404
    
    # Process games data
    games_data = []
    for _, game in team_games.iterrows():
        # Parse game date
        game_date = game['GameDate']
        if pd.notna(game_date) and game_date != '':
            try:
                # Convert to datetime and format
                from datetime import datetime
                if isinstance(game_date, str):
                    # Handle different date formats
                    if '00:00:00' in game_date:
                        game_date = game_date.split(' ')[0]
                    parsed_date = datetime.strptime(game_date, '%m/%d/%y')
                    formatted_date = parsed_date.strftime('%m/%d/%Y')
                else:
                    formatted_date = game_date.strftime('%m/%d/%Y')
            except:
                formatted_date = str(game_date)
        else:
            formatted_date = 'Unknown'
        
        # Determine result
        runs = game['Runs']
        opp_runs = game['OppRuns']
        
        if runs > opp_runs:
            result = 'W'
            result_class = 'win'
        elif runs < opp_runs:
            result = 'L'
            result_class = 'loss'
        else:
            result = 'T'
            result_class = 'tie'
        
        # Get opponent team name
        opp_team_num = game['OpponentTeamNumber']
        opp_team = teams_df[teams_df['TeamNumber'] == opp_team_num]
        opp_team_name = opp_team.iloc[0]['LongTeamName'] if len(opp_team) > 0 else f"Team {opp_team_num}"
        
        # Determine home/away
        home_team = game['HomeTeam']
        if home_team == 1:
            game_type = 'Home'
        else:
            game_type = 'Away'
        
        games_data.append({
            'game_number': int(game['GameNumber']),
            'date': formatted_date,
            'opponent': opp_team_name,
            'game_type': game_type,
            'runs_for': int(runs),
            'runs_against': int(opp_runs),
            'result': result,
            'result_class': result_class,
            'run_diff': runs - opp_runs
        })
    
    # Sort by game number
    games_data.sort(key=lambda x: x['game_number'])
    
    # Calculate season totals
    total_games = len(games_data)
    wins = len([g for g in games_data if g['result'] == 'W'])
    losses = len([g for g in games_data if g['result'] == 'L'])
    ties = len([g for g in games_data if g['result'] == 'T'])
    runs_for = sum(g['runs_for'] for g in games_data)
    runs_against = sum(g['runs_against'] for g in games_data)
    
    season_totals = {
        'total_games': total_games,
        'wins': wins,
        'losses': losses,
        'ties': ties,
        'runs_for': runs_for,
        'runs_against': runs_against,
        'run_diff': runs_for - runs_against,
        'win_pct': wins / total_games if total_games > 0 else 0
    }
    
    return render_template('team_games.html',
                         team=team,
                         season_name=season_name,
                         filter_number=filter_number,
                         games=games_data,
                         totals=season_totals)

@app.route('/player/<int:player_id>/games')
def player_games(player_id):
    """Player games page - shows all individual game stats for a player"""
    batting_df, people_df, teams_df = load_data()
    game_df = pd.read_csv('data/GameStats.csv')
    
    # Find the player
    player = people_df[people_df['PersonNumber'] == player_id]
    if len(player) == 0:
        return "Player not found", 404
    
    player = player.iloc[0]
    player_name = f"{player['FirstName']} {player['LastName']}"
    
    # Skip players whose names end with "Subs" (team substitutes)
    if player_name.endswith('Subs'):
        return "Player not found", 404
    
    # Get player's game stats
    player_games = batting_df[batting_df['PlayerNumber'] == player_id]
    
    if len(player_games) == 0:
        return "No game stats found for player", 404
    
    # Process game data
    games_data = []
    for _, game in player_games.iterrows():
        # Get game info
        game_info = game_df[(game_df['TeamNumber'] == game['TeamNumber']) & 
                           (game_df['GameNumber'] == game['GameNumber'])]
        
        if len(game_info) == 0:
            continue
            
        game_info = game_info.iloc[0]
        
        # Parse game date
        game_date = game_info['GameDate']
        if pd.notna(game_date) and game_date != '':
            try:
                from datetime import datetime
                if isinstance(game_date, str):
                    if '00:00:00' in game_date:
                        game_date = game_date.split(' ')[0]
                    parsed_date = datetime.strptime(game_date, '%m/%d/%y')
                    formatted_date = parsed_date.strftime('%m/%d/%Y')
                    sort_date = parsed_date  # For proper sorting
                else:
                    formatted_date = game_date.strftime('%m/%d/%Y')
                    sort_date = game_date
            except:
                formatted_date = str(game_date)
                sort_date = datetime(1900, 1, 1)  # Default for sorting
        else:
            formatted_date = 'Unknown'
            sort_date = datetime(1900, 1, 1)  # Default for sorting
        
        # Get team name
        team_info = teams_df[teams_df['TeamNumber'] == game['TeamNumber']]
        team_name = team_info.iloc[0]['LongTeamName'] if len(team_info) > 0 else f"Team {game['TeamNumber']}"
        
        # Get opponent info
        opp_team_num = game_info['OpponentTeamNumber']
        opp_team = teams_df[teams_df['TeamNumber'] == opp_team_num]
        opp_team_name = opp_team.iloc[0]['LongTeamName'] if len(opp_team) > 0 else f"Team {opp_team_num}"
        
        # Get opposing starting pitcher (placeholder for now - will use pitching stats later)
        opp_sp = "TBD"  # TODO: Get from pitching stats
        
        # Easter egg: Get full opposing lineup (hidden)
        opp_starters = batting_df[(batting_df['TeamNumber'] == opp_team_num) & 
                                 (batting_df['GameNumber'] == game['GameNumber']) & 
                                 (batting_df['Starter'] == 1)]
        opp_sp_names = []
        for _, starter in opp_starters.iterrows():
            starter_player = people_df[people_df['PersonNumber'] == starter['PlayerNumber']]
            if len(starter_player) > 0:
                starter_name = f"{starter_player.iloc[0]['FirstName']} {starter_player.iloc[0]['LastName']}"
                opp_sp_names.append(starter_name)
        opp_lineup_easter_egg = ", ".join(opp_sp_names) if opp_sp_names else ""
        
        # Calculate at-bats and other derived stats
        pa = game['PA']
        bb = game['BB'] if pd.notna(game['BB']) else 0
        sh = game['SH'] if pd.notna(game['SH']) else 0
        sf = game['SF'] if pd.notna(game['SF']) else 0
        ab = pa - bb - sh - sf
        
        # Calculate hits breakdown
        h = game['H'] if pd.notna(game['H']) else 0
        d = game['D'] if pd.notna(game['D']) else 0
        t = game['T'] if pd.notna(game['T']) else 0
        hr = game['HR'] if pd.notna(game['HR']) else 0
        singles = h - d - t - hr
        
        # Calculate total bases
        tb = singles + 2*d + 3*t + 4*hr
        
        # Calculate averages
        avg = h / ab if ab > 0 else 0
        obp = (h + bb) / pa if pa > 0 else 0
        slg = tb / ab if ab > 0 else 0
        
        # Determine home/away
        home_team = game_info['HomeTeam']
        if home_team == 1:
            game_type = 'Home'
        else:
            game_type = 'Away'
        
        # Get game result
        runs = game_info['Runs']
        opp_runs = game_info['OppRuns']
        if runs > opp_runs:
            result = 'W'
            result_class = 'win'
        elif runs < opp_runs:
            result = 'L'
            result_class = 'loss'
        else:
            result = 'T'
            result_class = 'tie'
        
        games_data.append({
            'date': formatted_date,
            'sort_date': sort_date,
            'team': team_name,
            'opponent': opp_team_name,
            'opp_sp': opp_sp,
            'opp_lineup_easter_egg': opp_lineup_easter_egg,  # Hidden easter egg data
            'game_type': game_type,
            'result': result,
            'result_class': result_class,
            'score': f"{runs}-{opp_runs}",
            'pa': int(pa),
            'ab': int(ab),
            'r': int(game['R']) if pd.notna(game['R']) else 0,
            'h': int(h),
            '1b': int(singles),
            '2b': int(d),
            '3b': int(t),
            'hr': int(hr),
            'rbi': int(game['RBI']) if pd.notna(game['RBI']) else 0,
            'bb': int(bb),
            'sf': int(sf),
            'oe': int(game['OE']) if pd.notna(game['OE']) else 0,
            'tb': int(tb),
            'avg': avg,
            'obp': obp,
            'slg': slg
        })
    
    # Sort by date (most recent first)
    games_data.sort(key=lambda x: x['sort_date'], reverse=True)
    
    # Calculate career totals
    total_games = len(games_data)
    total_pa = sum(g['pa'] for g in games_data)
    total_ab = sum(g['ab'] for g in games_data)
    total_r = sum(g['r'] for g in games_data)
    total_h = sum(g['h'] for g in games_data)
    total_hr = sum(g['hr'] for g in games_data)
    total_rbi = sum(g['rbi'] for g in games_data)
    total_bb = sum(g['bb'] for g in games_data)
    total_tb = sum(g['tb'] for g in games_data)
    
    # Calculate W/L record (easter egg)
    wins = sum(1 for g in games_data if g['result'] == 'W')
    losses = sum(1 for g in games_data if g['result'] == 'L')
    ties = sum(1 for g in games_data if g['result'] == 'T')
    wl_record = f"{wins}-{losses}"
    if ties > 0:
        wl_record += f"-{ties}"
    
    # Calculate winning percentage
    total_decisions = wins + losses
    win_pct = wins / total_decisions if total_decisions > 0 else 0
    wl_record_with_pct = f"{wl_record} ({win_pct:.3f})".replace('0.', '.')
    
    career_avg = total_h / total_ab if total_ab > 0 else 0
    career_obp = (total_h + total_bb) / total_pa if total_pa > 0 else 0
    career_slg = total_tb / total_ab if total_ab > 0 else 0
    
    career_totals = {
        'total_games': total_games,
        'total_pa': total_pa,
        'total_ab': total_ab,
        'total_r': total_r,
        'total_h': total_h,
        'total_hr': total_hr,
        'total_rbi': total_rbi,
        'total_bb': total_bb,
        'total_tb': total_tb,
        'career_avg': career_avg,
        'career_obp': career_obp,
        'career_slg': career_slg,
        'wl_record': wl_record_with_pct  # Easter egg data with winning percentage
    }
    
    return render_template('player_games.html',
                         player=player,
                         player_name=player_name,
                         games=games_data,
                         totals=career_totals)

if __name__ == '__main__':
    print("Starting D1 Softball Stats App...")
    print("Visit http://localhost:5000 to view the site")
    app.run(debug=True, host='0.0.0.0', port=5000) 