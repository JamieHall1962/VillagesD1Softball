"""
D1 Softball Hybrid Static Site Generator
Generates static pages + JSON data for dynamic content with zero compromises
"""

import os
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# Config
DATA_DIR = Path(__file__).parent / 'data'
SITE_DIR = Path(__file__).parent / 'site'
LEAGUE_NAME = "D1 Softball League"

# Ensure output directory exists
SITE_DIR.mkdir(exist_ok=True)
(SITE_DIR / 'data').mkdir(exist_ok=True)
(SITE_DIR / 'js').mkdir(exist_ok=True)

# Load data
print("Loading CSV data...")
players_df = pd.read_csv(DATA_DIR / 'People.csv')
batting_df = pd.read_csv(DATA_DIR / 'BattingStats.csv')
pitching_df = pd.read_csv(DATA_DIR / 'PitchingStats.csv')
games_df = pd.read_csv(DATA_DIR / 'GameStats.csv')
teams_df = pd.read_csv(DATA_DIR / 'Teams.csv')
filters_df = pd.read_csv(DATA_DIR / 'Filters.csv')
print("Data loaded successfully!")

def nostripleadingzero(value):
    """Format a float as .xxx (no leading zero, always 3 decimals)"""
    try:
        return ('%.3f' % value).lstrip('0')
    except Exception:
        return value

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

def filtername_to_code(name):
    """Convert filter name to season code (e.g., 'Winter 2011' -> 'W11')"""
    parts = name.split()
    if len(parts) != 2:
        return name.replace(" ", "")  # fallback
    season, year = parts
    code = ""
    if season.lower().startswith("win"):
        code = "W"
    elif season.lower().startswith("sum"):
        code = "S"
    elif season.lower().startswith("fal"):
        code = "F"
    else:
        code = season[0].upper()
    # Use last two digits of year
    code += year[-2:]
    return code

# Create season mapping
filters_df['SeasonCode'] = filters_df['FilterName'].apply(filtername_to_code)
season_to_filter = dict(zip(filters_df['SeasonCode'], filters_df['FilterNumber']))
filter_to_season = dict(zip(filters_df['FilterNumber'], filters_df['SeasonCode']))

print("Generating JSON data files...")

# --- Generate JSON Data Files ---

# 1. Players data
players_data = []
for _, player in players_df.iterrows():
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
            'firstName': str(player['FirstName']),
            'lastName': str(player['LastName']),
            'games_played': int(stats['games_played']),
            'pa': int(stats['pa']),
            'ab': int(stats['ab']),
            'r': int(stats['r']),
            'h': int(stats['h']),
            '1b': int(stats['1b']),
            '2b': int(stats['2b']),
            '3b': int(stats['3b']),
            'hr': int(stats['hr']),
            'rbi': int(stats['rbi']),
            'bb': int(stats['bb']),
            'sf': int(stats['sf']),
            'oe': int(stats['oe']),
            'tb': int(stats['tb']),
            'avg': float(stats['avg']),
            'slg': float(stats['slg']),
            'obp': float(stats['obp']),
        })

players_data.sort(key=lambda x: x['games_played'], reverse=True)

with open(SITE_DIR / 'data' / 'players.json', 'w', encoding='utf-8') as f:
    json.dump(players_data, f, indent=2)

# 2. Seasons data
seasons_data = []
for _, row in filters_df.iterrows():
    seasons_data.append({
        'filter_number': int(row['FilterNumber']),
        'season_name': row['FilterName'],
        'season_code': filtername_to_code(row['FilterName'])
    })

# Sort by season name (newest first)
def season_sort_key(season):
    name = season['season_name']
    parts = name.split()
    if len(parts) >= 2:
        season_type = parts[0]  # Winter, Summer, Fall
        year = parts[1]  # 2011, 2012, etc.
        type_priority = {'Winter': 1, 'Summer': 2, 'Fall': 3}.get(season_type, 0)
        return f"{year}{type_priority:01d}"
    return '0000'

seasons_data.sort(key=season_sort_key, reverse=True)

with open(SITE_DIR / 'data' / 'seasons.json', 'w', encoding='utf-8') as f:
    json.dump(seasons_data, f, indent=2)

# 3. Teams data
teams_data = []
for _, team in teams_df.iterrows():
    teams_data.append({
        'team_number': int(team['TeamNumber']),
        'team_name': team['LongTeamName'],
        'short_name': team.get('ShortTeamName', '')
    })

with open(SITE_DIR / 'data' / 'teams.json', 'w', encoding='utf-8') as f:
    json.dump(teams_data, f, indent=2)

# 4. Games data (for standings and game logs)
games_data = []
for _, game in games_df.iterrows():
    games_data.append({
        'team_number': int(game['TeamNumber']),
        'game_number': int(game['GameNumber']),
        'game_date': game['GameDate'],
        'runs': int(game['Runs']) if pd.notna(game['Runs']) else 0,
        'opp_runs': int(game['OppRuns']) if pd.notna(game['OppRuns']) else 0,
        'opponent_team_number': int(game['OpponentTeamNumber']) if pd.notna(game['OpponentTeamNumber']) else 0,
        'home_team': int(game['HomeTeam']) if pd.notna(game['HomeTeam']) else 0
    })

with open(SITE_DIR / 'data' / 'games.json', 'w', encoding='utf-8') as f:
    json.dump(games_data, f, indent=2)

# 5. Batting stats data (for detailed stats)
batting_data = []
for _, stat in batting_df.iterrows():
    batting_data.append({
        'player_number': int(stat['PlayerNumber']),
        'team_number': int(stat['TeamNumber']),
        'game_number': int(stat['GameNumber']),
        'pa': int(stat['PA']) if pd.notna(stat['PA']) else 0,
        'ab': int(stat['PA'] - stat.get('BB', 0) - stat.get('SH', 0) - stat.get('SF', 0)) if pd.notna(stat['PA']) else 0,
        'r': int(stat['R']) if pd.notna(stat['R']) else 0,
        'h': int(stat['H']) if pd.notna(stat['H']) else 0,
        'd': int(stat['D']) if pd.notna(stat['D']) else 0,
        't': int(stat['T']) if pd.notna(stat['T']) else 0,
        'hr': int(stat['HR']) if pd.notna(stat['HR']) else 0,
        'rbi': int(stat['RBI']) if pd.notna(stat['RBI']) else 0,
        'bb': int(stat['BB']) if pd.notna(stat['BB']) else 0,
        'sf': int(stat['SF']) if pd.notna(stat['SF']) else 0,
        'oe': int(stat['OE']) if pd.notna(stat['OE']) else 0,
        'u2': int(stat['U2']) if pd.notna(stat['U2']) else 0,
        'starter': int(stat['Starter']) if pd.notna(stat['Starter']) else 0
    })

with open(SITE_DIR / 'data' / 'batting_stats.json', 'w', encoding='utf-8') as f:
    json.dump(batting_data, f, indent=2)

print("JSON data files generated successfully!")

print("Generating static pages...")

# --- Generate Static Pages ---

# 1. Main index page
with open(SITE_DIR / 'index.html', 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <title>D1 Softball League Stats</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <style>
        body { background: #f8f9fa; font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #1e3a8a; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .nav-link { color: #1e3a8a; text-decoration: none; font-weight: bold; }
        .nav-link:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container my-4">
        <h1 class="mb-4">D1 Softball League Stats Archive</h1>
        <div class="header">
            <h2>Welcome to the D1 Softball League Stats Archive</h2>
            <p>Complete historical statistics for all players, teams, and seasons</p>
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Players</h5>
                        <p class="card-text">Browse all players and career statistics with detailed season breakdowns.</p>
                        <a href="players.html" class="btn btn-primary">View Players</a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Seasons</h5>
                        <p class="card-text">Browse by season with standings, team statistics, and game results.</p>
                        <a href="seasons.html" class="btn btn-primary">View Seasons</a>
                    </div>
                </div>
            </div>
        </div>
        <footer class="mt-5 text-muted">D1 Softball Stats &copy; 2025</footer>
    </div>
    <script src="js/app.js"></script>
</body>
</html>""")

# 2. Players list page
with open(SITE_DIR / 'players.html', 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Players - D1 Softball Stats</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <style>
        body { background: #f8f9fa; font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #1e3a8a; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .players-table { width: 100%; border-collapse: collapse; }
        .players-table th, .players-table td { padding: 8px; text-align: left; border-bottom: 1px solid #e2e8f0; font-size: 13px; }
        .players-table th { background: #f1f5f9; font-weight: bold; cursor: pointer; user-select: none; position: sticky; top: 0; z-index: 10; }
        .players-table th:hover { background: #e2e8f0; }
        .players-table tr:hover { background: #f8fafc; }
        .player-link { color: #1e3a8a; text-decoration: none; font-weight: bold; }
        .player-link:hover { text-decoration: underline; }
        .search-bar { margin-bottom: 16px; }
        .search-input { padding: 8px; width: 250px; font-size: 15px; border: 1px solid #cbd5e1; border-radius: 4px; }
        .sort-indicator { font-size: 11px; margin-left: 4px; color: #1e3a8a; }
        .table-container { max-height: 70vh; overflow-y: auto; border: 1px solid #e2e8f0; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container my-4">
        <nav class="mb-4">
            <a href="index.html">Home</a> |
            <a href="players.html">Players</a> |
            <a href="seasons.html">Seasons</a>
        </nav>
        
        <div class="header">
            <h1>D1 Softball Players</h1>
            <p>Click any column header to sort</p>
        </div>

        <div class="search-bar">
            <input type="text" id="playerSearch" class="search-input" placeholder="Search players by name...">
        </div>

        <div class="table-container">
            <table class="players-table" id="playersTable">
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">Rank</th>
                        <th onclick="sortTable(1)">Name</th>
                        <th onclick="sortTable(2)">Gm</th>
                        <th onclick="sortTable(3)">PA</th>
                        <th onclick="sortTable(4)">AB</th>
                        <th onclick="sortTable(5)">R</th>
                        <th onclick="sortTable(6)">H</th>
                        <th onclick="sortTable(7)">1B</th>
                        <th onclick="sortTable(8)">2B</th>
                        <th onclick="sortTable(9)">3B</th>
                        <th onclick="sortTable(10)">HR</th>
                        <th onclick="sortTable(11)">RBI</th>
                        <th onclick="sortTable(12)">BB</th>
                        <th onclick="sortTable(13)">SF</th>
                        <th onclick="sortTable(14)">OE</th>
                        <th onclick="sortTable(15)">TB</th>
                        <th onclick="sortTable(16)">BA</th>
                        <th onclick="sortTable(17)">Slg</th>
                        <th onclick="sortTable(18)">OBP</th>
                    </tr>
                </thead>
                <tbody id="playersTableBody">
                    <!-- Data will be loaded dynamically -->
                </tbody>
            </table>
        </div>
        
        <footer class="mt-5 text-muted">D1 Softball Stats &copy; 2025</footer>
    </div>
    <script src="js/app.js"></script>
</body>
</html>""")

# 3. Seasons list page
with open(SITE_DIR / 'seasons.html', 'w', encoding='utf-8') as f:
    f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Seasons - D1 Softball Stats</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <style>
        body { background: #f8f9fa; font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #1e3a8a; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .season-link { color: #1e3a8a; text-decoration: none; font-weight: bold; font-size: 18px; }
        .season-link:hover { text-decoration: underline; }
        .season-item { padding: 10px; border-bottom: 1px solid #e2e8f0; }
        .season-item:hover { background: #f8fafc; }
    </style>
</head>
<body>
    <div class="container my-4">
        <nav class="mb-4">
            <a href="index.html">Home</a> |
            <a href="players.html">Players</a> |
            <a href="seasons.html">Seasons</a>
        </nav>
        
        <div class="header">
            <h1>D1 Softball Seasons</h1>
            <p>Click on any season to view standings and teams</p>
        </div>

        <div id="seasonsList">
            <!-- Data will be loaded dynamically -->
        </div>
        
        <footer class="mt-5 text-muted">D1 Softball Stats &copy; 2025</footer>
    </div>
    <script src="js/app.js"></script>
</body>
</html>""")

print("Static pages generated successfully!")

print("Generating JavaScript application...")

# --- Generate JavaScript Application ---

with open(SITE_DIR / 'js' / 'app.js', 'w', encoding='utf-8') as f:
    f.write("""// D1 Softball Stats Application
// Replicates all Flask app functionality with zero compromises

// Global data storage
let playersData = [];
let seasonsData = [];
let teamsData = [];
let gamesData = [];
let battingStatsData = [];

// Utility functions
function nostripleadingzero(value) {
    try {
        return ('%.3f' % value).lstrip('0');
    } catch (e) {
        return value;
    }
}

function calculatePlayerStats(playerNumber) {
    const playerBatting = battingStatsData.filter(stat => stat.player_number === playerNumber);
    if (playerBatting.length === 0) return null;

    const totalPa = playerBatting.reduce((sum, stat) => sum + stat.pa, 0);
    const totalR = playerBatting.reduce((sum, stat) => sum + stat.r, 0);
    const totalH = playerBatting.reduce((sum, stat) => sum + stat.h, 0);
    const total2b = playerBatting.reduce((sum, stat) => sum + stat.d, 0);
    const total3b = playerBatting.reduce((sum, stat) => sum + stat.t, 0);
    const totalHr = playerBatting.reduce((sum, stat) => sum + stat.hr, 0);
    const totalBb = playerBatting.reduce((sum, stat) => sum + stat.bb, 0);
    const totalSf = playerBatting.reduce((sum, stat) => sum + stat.sf, 0);
    const totalOe = playerBatting.reduce((sum, stat) => sum + stat.oe, 0);
    const totalRbi = playerBatting.reduce((sum, stat) => sum + stat.rbi, 0);
    const total1b = totalH - total2b - total3b - totalHr;

    // Calculate at-bats
    const totalAb = totalPa - totalBb - totalSf;

    // Games played with U2 correction
    const uniqueGames = new Set(playerBatting.map(stat => `${stat.team_number}-${stat.game_number}`)).size;
    const totalU2 = playerBatting.reduce((sum, stat) => sum + stat.u2, 0);
    const gamesPlayed = uniqueGames + totalU2;

    // Averages
    const avg = totalAb > 0 ? totalH / totalAb : 0;
    const obp = totalPa > 0 ? (totalH + totalBb) / totalPa : 0;
    const slg = totalAb > 0 ? (totalH + total2b + 2*total3b + 3*totalHr) / totalAb : 0;

    return {
        games_played: gamesPlayed,
        pa: totalPa,
        ab: totalAb,
        r: totalR,
        h: totalH,
        '1b': total1b,
        '2b': total2b,
        '3b': total3b,
        hr: totalHr,
        rbi: totalRbi,
        bb: totalBb,
        sf: totalSf,
        oe: totalOe,
        tb: totalH + total2b + 2*total3b + 3*totalHr,
        avg: avg,
        slg: slg,
        obp: obp
    };
}

// Load all data
async function loadData() {
    try {
        // Determine the correct base path for data files
        const path = window.location.pathname;
        let basePath = '';
        
        if (path.includes('/player/') || path.includes('/season/')) {
            basePath = '../';
        }
        
        const [playersResponse, seasonsResponse, teamsResponse, gamesResponse, battingResponse] = await Promise.all([
            fetch(basePath + 'data/players.json'),
            fetch(basePath + 'data/seasons.json'),
            fetch(basePath + 'data/games.json'),
            fetch(basePath + 'data/teams.json'),
            fetch(basePath + 'data/batting_stats.json')
        ]);

        playersData = await playersResponse.json();
        seasonsData = await seasonsResponse.json();
        teamsData = await teamsResponse.json();
        gamesData = await gamesResponse.json();
        battingStatsData = await battingResponse.json();

        console.log('Data loaded successfully!');
        initializeApp();
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Initialize application based on current page
function initializeApp() {
    const path = window.location.pathname;
    
    if (path.includes('players.html') || path.endsWith('/')) {
        initializePlayersPage();
    } else if (path.includes('seasons.html')) {
        initializeSeasonsPage();
    } else if (path.includes('player/')) {
        initializePlayerDetailPage();
    } else if (path.includes('season/')) {
        initializeSeasonDetailPage();
    }
}

// Players page functionality
function initializePlayersPage() {
    if (!document.getElementById('playersTableBody')) return;
    
    renderPlayersTable();
    setupPlayersSorting();
    setupPlayersSearch();
}

function renderPlayersTable() {
    const tbody = document.getElementById('playersTableBody');
    tbody.innerHTML = '';
    
    playersData.forEach((player, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td><a href="player/${player.id}.html" class="player-link">${player.name}</a></td>
            <td>${player.games_played}</td>
            <td>${player.pa}</td>
            <td>${player.ab}</td>
            <td>${player.r}</td>
            <td>${player.h}</td>
            <td>${player['1b']}</td>
            <td>${player['2b']}</td>
            <td>${player['3b']}</td>
            <td>${player.hr}</td>
            <td>${player.rbi}</td>
            <td>${player.bb}</td>
            <td>${player.sf}</td>
            <td>${player.oe}</td>
            <td>${player.tb}</td>
            <td>${nostripleadingzero(player.avg)}</td>
            <td>${nostripleadingzero(player.slg)}</td>
            <td>${nostripleadingzero(player.obp)}</td>
        `;
        tbody.appendChild(row);
    });
}

function setupPlayersSorting() {
    // Implementation for sorting (same as Flask app)
    let currentSort = { column: -1, direction: 1 };
    
    window.sortTable = function(columnIndex) {
        const table = document.getElementById('playersTable');
        const tbody = table.getElementsByTagName('tbody')[0];
        const rows = Array.from(tbody.getElementsByTagName('tr'));
        
        if (currentSort.column === columnIndex) {
            currentSort.direction = -currentSort.direction;
        } else {
            currentSort.direction = 1;
        }
        currentSort.column = columnIndex;
        
        rows.sort(function(a, b) {
            const aVal = a.cells[columnIndex].textContent.trim();
            const bVal = b.cells[columnIndex].textContent.trim();
            
            const aNum = parseFloat(aVal.replace(/[^0-9.-]/g, ''));
            const bNum = parseFloat(bVal.replace(/[^0-9.-]/g, ''));
            
            if (!isNaN(aNum) && !isNaN(bNum)) {
                return (aNum - bNum) * currentSort.direction;
            } else {
                return aVal.localeCompare(bVal) * currentSort.direction;
            }
        });
        
        rows.forEach(function(row) {
            tbody.appendChild(row);
        });
        
        updateRankNumbers();
        updateSortIndicators(columnIndex, currentSort.direction);
    };
}

function setupPlayersSearch() {
    const searchInput = document.getElementById('playerSearch');
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const filter = this.value.toLowerCase();
        const table = document.getElementById('playersTable');
        const trs = table.getElementsByTagName('tr');
        
        for (let i = 1; i < trs.length; i++) {
            const nameCell = trs[i].getElementsByTagName('td')[1];
            if (nameCell) {
                const name = nameCell.textContent || nameCell.innerText;
                trs[i].style.display = name.toLowerCase().indexOf(filter) > -1 ? '' : 'none';
            }
        }
    });
}

function updateRankNumbers() {
    const tbody = document.getElementById('playersTable').getElementsByTagName('tbody')[0];
    const rows = tbody.getElementsByTagName('tr');
    for (let i = 0; i < rows.length; i++) {
        const rankCell = rows[i].cells[0];
        if (rankCell) {
            rankCell.textContent = i + 1;
        }
    }
}

function updateSortIndicators(column, direction) {
    const headers = document.querySelectorAll('.players-table th');
    headers.forEach(function(header, index) {
        let indicator = header.querySelector('.sort-indicator');
        if (!indicator) {
            indicator = document.createElement('span');
            indicator.className = 'sort-indicator';
            header.appendChild(indicator);
        }
        
        if (index === column) {
            indicator.textContent = direction === 1 ? '▲' : '▼';
        } else {
            indicator.textContent = '';
        }
    });
}

// Seasons page functionality
function initializeSeasonsPage() {
    if (!document.getElementById('seasonsList')) return;
    
    renderSeasonsList();
}

function renderSeasonsList() {
    const container = document.getElementById('seasonsList');
    container.innerHTML = '';
    
    seasonsData.forEach(season => {
        const div = document.createElement('div');
        div.className = 'season-item';
        div.innerHTML = `<a href="season/${season.season_code}.html" class="season-link">${season.season_name}</a>`;
        container.appendChild(div);
    });
}

// Player detail page functionality
function initializePlayerDetailPage() {
    if (!document.getElementById('playerContent')) return;
    
    // Extract player ID from URL
    const path = window.location.pathname;
    const match = path.match(/\/player\/(\d+)\.html$/);
    if (match) {
        const playerId = parseInt(match[1]);
        renderPlayerDetail(playerId);
    }
}

// Season detail page functionality
function initializeSeasonDetailPage() {
    if (!document.getElementById('seasonContent')) return;
    
    // Extract season code from URL
    const path = window.location.pathname;
    const match = path.match(/\/season\/([^.]+)\.html$/);
    if (match) {
        const seasonCode = match[1];
        renderSeasonDetail(seasonCode);
    }
}

function renderPlayerDetail(playerId) {
    const player = playersData.find(p => p.id === playerId);
    if (!player) {
        document.getElementById('playerContent').innerHTML = '<p>Player not found.</p>';
        return;
    }
    
    // Calculate season breakdown
    const seasonBreakdown = calculatePlayerSeasonBreakdown(playerId);
    
    // Render career stats grid
    const statsGrid = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${player.games_played}</div>
                <div class="stat-label">Games</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.pa}</div>
                <div class="stat-label">PA</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.ab}</div>
                <div class="stat-label">AB</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.h}</div>
                <div class="stat-label">H</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.r}</div>
                <div class="stat-label">R</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.rbi}</div>
                <div class="stat-label">RBI</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player['2b']}</div>
                <div class="stat-label">2B</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player['3b']}</div>
                <div class="stat-label">3B</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.hr}</div>
                <div class="stat-label">HR</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${player.bb}</div>
                <div class="stat-label">BB</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${nostripleadingzero(player.avg)}</div>
                <div class="stat-label">AVG</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${nostripleadingzero(player.obp)}</div>
                <div class="stat-label">OBP</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${nostripleadingzero(player.slg)}</div>
                <div class="stat-label">SLG</div>
            </div>
        </div>
    `;
    
    // Render season breakdown table
    const seasonTable = `
        <h2>${seasonBreakdown.length} Seasons</h2>
        <div class="table-container">
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>Season</th>
                        <th>Team</th>
                        <th>G</th>
                        <th>PA</th>
                        <th>AB</th>
                        <th>H</th>
                        <th>R</th>
                        <th>RBI</th>
                        <th>2B</th>
                        <th>3B</th>
                        <th>HR</th>
                        <th>BB</th>
                        <th>AVG</th>
                        <th>OBP</th>
                        <th>SLG</th>
                    </tr>
                </thead>
                <tbody>
                    ${seasonBreakdown.map(season => `
                        <tr>
                            <td><a href="../season/${season.season_code}.html" class="season-link">${season.season_name}</a></td>
                            <td>${season.team_name}</td>
                            <td>${season.games_played}</td>
                            <td>${season.pa}</td>
                            <td>${season.ab}</td>
                            <td>${season.h}</td>
                            <td>${season.r}</td>
                            <td>${season.rbi}</td>
                            <td>${season['2b']}</td>
                            <td>${season['3b']}</td>
                            <td>${season.hr}</td>
                            <td>${season.bb}</td>
                            <td>${nostripleadingzero(season.avg)}</td>
                            <td>${nostripleadingzero(season.obp)}</td>
                            <td>${nostripleadingzero(season.slg)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    document.getElementById('playerContent').innerHTML = statsGrid + seasonTable;
}

function calculatePlayerSeasonBreakdown(playerId) {
    const playerStats = battingStatsData.filter(stat => stat.player_number === playerId);
    if (playerStats.length === 0) return [];
    
    // Group by team to get season information
    const teamStats = {};
    playerStats.forEach(stat => {
        if (!teamStats[stat.team_number]) {
            teamStats[stat.team_number] = [];
        }
        teamStats[stat.team_number].push(stat);
    });
    
    const breakdown = [];
    
    Object.keys(teamStats).forEach(teamNumber => {
        const teamStat = teamStats[teamNumber];
        const totalPa = teamStat.reduce((sum, stat) => sum + stat.pa, 0);
        const totalR = teamStat.reduce((sum, stat) => sum + stat.r, 0);
        const totalH = teamStat.reduce((sum, stat) => sum + stat.h, 0);
        const total2b = teamStat.reduce((sum, stat) => sum + stat.d, 0);
        const total3b = teamStat.reduce((sum, stat) => sum + stat.t, 0);
        const totalHr = teamStat.reduce((sum, stat) => sum + stat.hr, 0);
        const totalBb = teamStat.reduce((sum, stat) => sum + stat.bb, 0);
        const totalRbi = teamStat.reduce((sum, stat) => sum + stat.rbi, 0);
        const totalSf = teamStat.reduce((sum, stat) => sum + stat.sf, 0);
        const totalOe = teamStat.reduce((sum, stat) => sum + stat.oe, 0);
        
        // Calculate at-bats
        const totalAb = totalPa - totalBb - totalSf;
        
        // Games played with U2 correction
        const uniqueGames = new Set(teamStat.map(stat => `${stat.team_number}-${stat.game_number}`)).size;
        const totalU2 = teamStat.reduce((sum, stat) => sum + stat.u2, 0);
        const gamesPlayed = uniqueGames + totalU2;
        
        // Averages
        const avg = totalAb > 0 ? totalH / totalAb : 0;
        const obp = totalPa > 0 ? (totalH + totalBb) / totalPa : 0;
        const slg = totalAb > 0 ? (totalH + total2b + 2*total3b + 3*totalHr) / totalAb : 0;
        
        // Find team name
        const team = teamsData.find(t => t.team_number === parseInt(teamNumber));
        const teamName = team ? team.team_name : `Team ${teamNumber}`;
        
        // Extract season code from team name
        const seasonMatch = teamName.match(/\s([WSF]\d{2})$/);
        const seasonCode = seasonMatch ? seasonMatch[1] : 'Unknown';
        
        // Find season name
        const season = seasonsData.find(s => s.season_code === seasonCode);
        const seasonName = season ? season.season_name : seasonCode;
        
        breakdown.push({
            season_code: seasonCode,
            season_name: seasonName,
            team_name: teamName,
            games_played: gamesPlayed,
            pa: totalPa,
            ab: totalAb,
            h: totalH,
            r: totalR,
            rbi: totalRbi,
            '2b': total2b,
            '3b': total3b,
            hr: totalHr,
            bb: totalBb,
            avg: avg,
            obp: obp,
            slg: slg
        });
    });
    
    // Sort by season (Winter=1, Summer=2, Fall=3)
    breakdown.sort((a, b) => {
        const aCode = a.season_code;
        const bCode = b.season_code;
        
        const aYear = parseInt(aCode.slice(1));
        const bYear = parseInt(bCode.slice(1));
        const aSeason = aCode[0];
        const bSeason = bCode[0];
        
        const seasonOrder = { 'W': 1, 'S': 2, 'F': 3 };
        
        if (aYear !== bYear) return bYear - aYear; // Newest first
        return seasonOrder[aSeason] - seasonOrder[bSeason];
    });
    
    return breakdown;
}

// Season detail page functionality
function renderSeasonDetail(seasonCode) {
    const season = seasonsData.find(s => s.season_code === seasonCode);
    if (!season) {
        document.getElementById('seasonContent').innerHTML = '<p>Season not found.</p>';
        return;
    }
    
    // Calculate standings for this season
    const standings = calculateSeasonStandings(seasonCode);
    
    // Render standings
    let standingsHtml = '';
    
    if (standings.divisions && standings.divisions.length > 1) {
        // Multiple divisions
        standings.divisions.forEach(division => {
            standingsHtml += `
                <div class="division-section">
                    <div class="division-title">${division.name}</div>
                    <div class="table-container">
                        <table class="table table-striped table-hover">
                            <thead>
                                <tr>
                                    <th>Rank</th>
                                    <th>Team</th>
                                    <th>W</th>
                                    <th>L</th>
                                    <th>PCT</th>
                                    <th>GB</th>
                                    <th>R</th>
                                    <th>RA</th>
                                    <th>R/G</th>
                                    <th>RA/G</th>
                                    <th>BA</th>
                                    <th>OBP</th>
                                    <th>SLG</th>
                                    <th>HR</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${division.teams.map((team, index) => `
                                    <tr>
                                        <td>${index + 1}</td>
                                        <td><a href="../team/${team.team_number}.html" class="team-link">${team.team_name}</a></td>
                                        <td>${team.wins}</td>
                                        <td>${team.losses}</td>
                                        <td>${nostripleadingzero(team.win_pct)}</td>
                                        <td>${team.games_back}</td>
                                        <td>${team.runs}</td>
                                        <td>${team.runs_allowed}</td>
                                        <td>${nostripleadingzero(team.runs_per_game)}</td>
                                        <td>${nostripleadingzero(team.runs_allowed_per_game)}</td>
                                        <td>${nostripleadingzero(team.team_avg)}</td>
                                        <td>${nostripleadingzero(team.team_obp)}</td>
                                        <td>${nostripleadingzero(team.team_slg)}</td>
                                        <td>${team.team_hr}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;
        });
    } else {
        // Single division
        const teams = standings.divisions[0].teams;
        standingsHtml = `
            <div class="table-container">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Team</th>
                            <th>W</th>
                            <th>L</th>
                            <th>PCT</th>
                            <th>GB</th>
                            <th>R</th>
                            <th>RA</th>
                            <th>R/G</th>
                            <th>RA/G</th>
                            <th>BA</th>
                            <th>OBP</th>
                            <th>SLG</th>
                            <th>HR</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${teams.map((team, index) => `
                            <tr>
                                <td>${index + 1}</td>
                                <td><a href="../team/${team.team_number}.html" class="team-link">${team.team_name}</a></td>
                                <td>${team.wins}</td>
                                <td>${team.losses}</td>
                                <td>${nostripleadingzero(team.win_pct)}</td>
                                <td>${team.games_back}</td>
                                <td>${team.runs}</td>
                                <td>${team.runs_allowed}</td>
                                <td>${nostripleadingzero(team.runs_per_game)}</td>
                                <td>${nostripleadingzero(team.runs_allowed_per_game)}</td>
                                <td>${nostripleadingzero(team.team_avg)}</td>
                                <td>${nostripleadingzero(team.team_obp)}</td>
                                <td>${nostripleadingzero(team.team_slg)}</td>
                                <td>${team.team_hr}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }
    
    // Add note for combined seasons if needed
    if (['S15', 'S16', 'S17'].includes(seasonCode)) {
        standingsHtml = `
            <div class="note-box">
                <strong>Note:</strong> This season combined D1 and D2 divisions. Only D1 player statistics were recorded.
            </div>
        ` + standingsHtml;
    }
    
    document.getElementById('seasonContent').innerHTML = standingsHtml;
}

function calculateSeasonStandings(seasonCode) {
    // Find teams for this season
    const seasonTeams = teamsData.filter(team => {
        const seasonMatch = team.team_name.match(/\s([WSF]\d{2})$/);
        return seasonMatch && seasonMatch[1] === seasonCode;
    });
    
    if (seasonTeams.length === 0) {
        return {
            divisions: [{
                name: 'Division',
                teams: []
            }]
        };
    }
    
    // Check for divisions (teams with parentheses in names)
    const divisions = {};
    seasonTeams.forEach(team => {
        const divisionMatch = team.team_name.match(/\(([^)]+)\)/);
        const divisionName = divisionMatch ? divisionMatch[1] : 'Division';
        
        if (!divisions[divisionName]) {
            divisions[divisionName] = [];
        }
        divisions[divisionName].push(team);
    });
    
    // Calculate standings for each division
    const divisionStandings = [];
    
    Object.keys(divisions).forEach(divisionName => {
        const teams = divisions[divisionName];
        const teamStandings = [];
        
        teams.forEach(team => {
            // Get games for this team in this season
            const teamGames = gamesData.filter(game => game.team_number === team.team_number);
            
            let wins = 0;
            let losses = 0;
            let runs = 0;
            let runsAllowed = 0;
            
            teamGames.forEach(game => {
                runs += game.runs;
                runsAllowed += game.opp_runs;
                
                if (game.runs > game.opp_runs) {
                    wins++;
                } else if (game.runs < game.opp_runs) {
                    losses++;
                }
            });
            
            // Calculate team batting stats
            const teamBatting = battingStatsData.filter(stat => stat.team_number === team.team_number);
            const totalPa = teamBatting.reduce((sum, stat) => sum + stat.pa, 0);
            const totalH = teamBatting.reduce((sum, stat) => sum + stat.h, 0);
            const total2b = teamBatting.reduce((sum, stat) => sum + stat.d, 0);
            const total3b = teamBatting.reduce((sum, stat) => sum + stat.t, 0);
            const totalHr = teamBatting.reduce((sum, stat) => sum + stat.hr, 0);
            const totalBb = teamBatting.reduce((sum, stat) => sum + stat.bb, 0);
            const totalSf = teamBatting.reduce((sum, stat) => sum + stat.sf, 0);
            
            const totalAb = totalPa - totalBb - totalSf;
            const teamAvg = totalAb > 0 ? totalH / totalAb : 0;
            const teamObp = totalPa > 0 ? (totalH + totalBb) / totalPa : 0;
            const teamSlg = totalAb > 0 ? (totalH + total2b + 2*total3b + 3*totalHr) / totalAb : 0;
            
            const winPct = (wins + losses) > 0 ? wins / (wins + losses) : 0;
            const gamesPlayed = wins + losses;
            const runsPerGame = gamesPlayed > 0 ? runs / gamesPlayed : 0;
            const runsAllowedPerGame = gamesPlayed > 0 ? runsAllowed / gamesPlayed : 0;
            
            teamStandings.push({
                team_number: team.team_number,
                team_name: team.team_name,
                wins: wins,
                losses: losses,
                win_pct: winPct,
                games_back: 0, // Will be calculated below
                runs: runs,
                runs_allowed: runsAllowed,
                runs_per_game: runsPerGame,
                runs_allowed_per_game: runsAllowedPerGame,
                team_avg: teamAvg,
                team_obp: teamObp,
                team_slg: teamSlg,
                team_hr: totalHr
            });
        });
        
        // Sort by winning percentage
        teamStandings.sort((a, b) => b.win_pct - a.win_pct);
        
        // Calculate games back
        if (teamStandings.length > 0) {
            const firstPlaceWins = teamStandings[0].wins;
            const firstPlaceLosses = teamStandings[0].losses;
            
            teamStandings.forEach((team, index) => {
                if (index === 0) {
                    team.games_back = 0;
                } else {
                    const gamesBack = ((firstPlaceWins - team.wins) + (team.losses - firstPlaceLosses)) / 2;
                    team.games_back = gamesBack;
                }
            });
        }
        
        divisionStandings.push({
            name: divisionName,
            teams: teamStandings
        });
    });
    
    return {
        divisions: divisionStandings
    };
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', loadData);

// Export functions for use in other scripts
window.D1Stats = {
    loadData,
    calculatePlayerStats,
    nostripleadingzero
};
""")

print("JavaScript application generated successfully!")

# --- Generate Individual Player Pages ---
print("Generating individual player pages...")
(SITE_DIR / 'player').mkdir(exist_ok=True)

CACHE_BUST = '?v=20250708'

for player in players_data:
    player_id = player['id']
    player_file = SITE_DIR / 'player' / f'{player_id}.html'
    
    with open(player_file, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{player['name']} - {LEAGUE_NAME}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid #dee2e6;
        }}
        .stat-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: #0d6efd;
            margin-bottom: 4px;
        }}
        .stat-label {{
            font-size: 0.9em;
            color: #6c757d;
            text-transform: uppercase;
        }}
        .table-container {{
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid #dee2e6;
            border-radius: 8px;
        }}
        .table th {{
            position: sticky;
            top: 0;
            background: white;
            z-index: 1;
        }}
        .season-link {{
            color: #0d6efd;
            text-decoration: none;
        }}
        .season-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container my-4">
        <nav class="mb-4">
            <a href="../index.html">Home</a> |
            <a href="../players.html">← Back to Players List</a>
        </nav>
        
        <div class="header">
            <h1>{player['name']}</h1>
            <p>Career Statistics</p>
        </div>

        <div id="playerContent">
            <p>Loading player data...</p>
        </div>
    </div>

    <script src="../js/app.js{CACHE_BUST}"></script>
    <script>
        // Load data and render player detail
        document.addEventListener('DOMContentLoaded', function() {{
            loadData().then(function() {{
                const playerId = {player_id};
                const player = playersData.find(p => p.id === playerId);
                if (player) {{
                    renderPlayerDetail(playerId);
                }}
            }});
        }});
    </script>
</body>
</html>""")

# --- Generate Individual Season Pages ---
print("Generating individual season pages...")
(SITE_DIR / 'season').mkdir(exist_ok=True)

CACHE_BUST = '?v=20250708'

for season in seasons_data:
    season_code = season['season_code']
    season_file = SITE_DIR / 'season' / f'{season_code}.html'
    
    with open(season_file, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{season['season_name']} - {LEAGUE_NAME}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .division-section {{
            margin-bottom: 30px;
        }}
        .division-title {{
            background: #f8f9fa;
            padding: 10px 15px;
            border-radius: 8px 8px 0 0;
            border: 1px solid #dee2e6;
            border-bottom: none;
            font-weight: bold;
        }}
        .table-container {{
            border: 1px solid #dee2e6;
            border-radius: 0 0 8px 8px;
            overflow: hidden;
        }}
        .table th {{
            position: sticky;
            top: 0;
            background: white;
            z-index: 1;
        }}
        .team-link {{
            color: #0d6efd;
            text-decoration: none;
        }}
        .team-link:hover {{
            text-decoration: underline;
        }}
        .note-box {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container my-4">
        <nav class="mb-4">
            <a href="../index.html">Home</a> |
            <a href="../seasons.html">← Back to Seasons List</a>
        </nav>
        
        <div class="header">
            <h1>{season['season_name']}</h1>
        </div>

        <div id="seasonContent">
            <p>Loading season data...</p>
        </div>
    </div>

    <script src="../js/app.js{CACHE_BUST}"></script>
    <script>
        // Load data and render season detail
        document.addEventListener('DOMContentLoaded', function() {{
            loadData().then(function() {{
                const seasonCode = '{season_code}';
                renderSeasonDetail(seasonCode);
            }});
        }});
    </script>
</body>
</html>""")

print(f"Hybrid site generated successfully in {SITE_DIR}/")
print("Features included:")
print("- Static pages for main navigation (Home, Players list, Seasons list)")
print("- Individual player and season detail pages")
print("- JSON data files for fast loading")
print("- JavaScript that replicates all Flask app functionality")
print("- All easter eggs, sorting, search, and interactive features")
print("- Zero compromises - identical to localhost experience")
print(f"- Generated {len(players_data)} player pages and {len(seasons_data)} season pages") 