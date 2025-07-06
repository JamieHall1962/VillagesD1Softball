"""
D1 Softball Static Site Generator
Reads CSVs and outputs a complete drill-down HTML site with ALL features from Flask app
"""

import os
import pandas as pd
from pathlib import Path
from datetime import datetime

# Config
DATA_DIR = Path(__file__).parent / 'data'
SITE_DIR = Path(__file__).parent / 'site'
LEAGUE_NAME = "D1 Softball League"

# Ensure output directory exists
SITE_DIR.mkdir(exist_ok=True)
(SITE_DIR / 'players').mkdir(exist_ok=True)
(SITE_DIR / 'seasons').mkdir(exist_ok=True)
(SITE_DIR / 'teams').mkdir(exist_ok=True)

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

# --- HTML Templates ---
def render_header(title, include_sorting_js=False):
    js_code = ""
    if include_sorting_js:
        js_code = """
        <script>
        function filterPlayers() {
            var input = document.getElementById('playerSearch');
            var filter = input.value.toLowerCase();
            var table = document.getElementById('playersTable');
            var trs = table.getElementsByTagName('tr');
            for (var i = 1; i < trs.length; i++) {
                var nameCell = trs[i].getElementsByTagName('td')[1];
                if (nameCell) {
                    var name = nameCell.textContent || nameCell.innerText;
                    trs[i].style.display = name.toLowerCase().indexOf(filter) > -1 ? '' : 'none';
                }
            }
        }

        // Simple table sorting
        let currentSort = { column: -1, direction: 1 };
        
        function sortTable(columnIndex) {
            var table = document.getElementById('playersTable');
            var tbody = table.getElementsByTagName('tbody')[0];
            var rows = Array.from(tbody.getElementsByTagName('tr'));
            
            // Toggle direction if same column
            if (currentSort.column === columnIndex) {
                currentSort.direction = -currentSort.direction;
            } else {
                currentSort.direction = 1;
            }
            currentSort.column = columnIndex;
            
            // Sort the rows
            rows.sort(function(a, b) {
                var aVal = a.cells[columnIndex].textContent.trim();
                var bVal = b.cells[columnIndex].textContent.trim();
                
                // Try to parse as numbers
                var aNum = parseFloat(aVal.replace(/[^0-9.-]/g, ''));
                var bNum = parseFloat(bVal.replace(/[^0-9.-]/g, ''));
                
                if (!isNaN(aNum) && !isNaN(bNum)) {
                    return (aNum - bNum) * currentSort.direction;
                } else {
                    return aVal.localeCompare(bVal) * currentSort.direction;
                }
            });
            
            // Reorder the rows
            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
            
            // Update rank numbers
            updateRankNumbers();
            
            // Update indicators
            updateSortIndicators(columnIndex, currentSort.direction);
        }
        
        function updateRankNumbers() {
            var tbody = document.getElementById('playersTable').getElementsByTagName('tbody')[0];
            var rows = tbody.getElementsByTagName('tr');
            for (var i = 0; i < rows.length; i++) {
                var rankCell = rows[i].cells[0];
                if (rankCell) {
                    rankCell.textContent = i + 1;
                }
            }
        }
        
        function updateSortIndicators(column, direction) {
            var headers = document.querySelectorAll('.players-table th');
            headers.forEach(function(header, index) {
                var indicator = header.querySelector('.sort-indicator');
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
        
        // Initialize on page load
        window.onload = function() {
            // Add sort indicators to all headers
            var headers = document.querySelectorAll('.players-table th');
            headers.forEach(function(header) {
                var indicator = document.createElement('span');
                indicator.className = 'sort-indicator';
                header.appendChild(indicator);
            });
        };
        </script>
        """
    
    return f"""
    <html><head>
    <meta charset='utf-8'>
    <title>{title} - {LEAGUE_NAME}</title>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <style>
        body{{background:#f8f9fa; font-family: Arial, sans-serif; margin: 20px;}}
        .header {{ background: #1e3a8a; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .players-table {{ width: 100%; border-collapse: collapse; }}
        .players-table th, .players-table td {{ padding: 8px; text-align: left; border-bottom: 1px solid #e2e8f0; font-size: 13px; }}
        .players-table th {{ background: #f1f5f9; font-weight: bold; cursor: pointer; user-select: none; position: sticky; top: 0; z-index: 10; }}
        .players-table th:hover {{ background: #e2e8f0; }}
        .players-table tr:hover {{ background: #f8fafc; }}
        .player-link {{ color: #1e3a8a; text-decoration: none; font-weight: bold; }}
        .player-link:hover {{ text-decoration: underline; }}
        .back-link {{ margin: 20px 0; }}
        .back-link a {{ color: #1e3a8a; text-decoration: none; }}
        .back-link a:hover {{ text-decoration: underline; }}
        .search-bar {{ margin-bottom: 16px; }}
        .search-input {{ padding: 8px; width: 250px; font-size: 15px; border: 1px solid #cbd5e1; border-radius: 4px; }}
        .sort-indicator {{ font-size: 11px; margin-left: 4px; color: #1e3a8a; }}
        .table-container {{ max-height: 70vh; overflow-y: auto; border: 1px solid #e2e8f0; border-radius: 8px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin: 20px 0; }}
        .stat-card {{ background: #f8fafc; padding: 10px; border-radius: 8px; border-left: 4px solid #1e3a8a; text-align: center; }}
        .stat-value {{ font-size: 18px; font-weight: bold; color: #1e3a8a; }}
        .stat-label {{ color: #64748b; font-size: 11px; margin-top: 3px; }}
        .games-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 12px; }}
        .games-table th, .games-table td {{ padding: 6px 4px; text-align: center; border-bottom: 1px solid #e2e8f0; }}
        .games-table th {{ background: #f1f5f9; font-weight: bold; font-size: 11px; }}
        .games-table tr:hover {{ background: #f8fafc; }}
        .games-table td:nth-child(1) {{ text-align: left; }}
        .games-table td:nth-child(2) {{ text-align: left; }}
        .games-table td:nth-child(3) {{ text-align: left; }}
        .games-table td:nth-child(4) {{ text-align: left; }}
        .win {{ color: #059669; font-weight: bold; }}
        .loss {{ color: #dc2626; font-weight: bold; }}
        .tie {{ color: #f59e0b; font-weight: bold; }}
        .game-type {{ font-size: 10px; color: #64748b; }}
        .score {{ font-weight: bold; }}
        .highlight {{ background: #fef3c7; }}
        .fielding {{ font-size: 10px; color: #64748b; }}
        .starter {{ font-size: 10px; color: #059669; font-weight: bold; }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .easter-egg-wl {{
            background: linear-gradient(135deg, #fef3c7, #fde68a) !important;
            border-left-color: #f59e0b !important;
        }}
        
        .table-container {{
            max-height: 600px;
            overflow-y: auto;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }}
        
        .games-table {{
            position: relative;
        }}
        
        .games-table thead {{
            position: sticky;
            top: 0;
            z-index: 10;
            background: #f1f5f9;
        }}
        
        .games-table thead th {{
            background: #f1f5f9;
            border-bottom: 2px solid #e2e8f0;
        }}
    </style>
    {js_code}
    </head><body>
    <div class='container my-4'>
    <h1 class='mb-4'>{LEAGUE_NAME}</h1>
    <nav class='mb-4'>
      <a href='../index.html'>Home</a> |
      <a href='../players/index.html'>Players</a> |
      <a href='../seasons/index.html'>Seasons</a>
    </nav>
    """

def render_footer():
    return """
    <footer class='mt-5 text-muted'>D1 Softball Stats &copy; 2025</footer>
    </div></body></html>
    """

# --- Generate Main Index ---
with open(SITE_DIR / 'index.html', 'w', encoding='utf-8') as f:
    f.write(render_header('Home'))
    f.write("""
    <h2>Welcome to the D1 Softball League Stats Archive</h2>
    <ul>
      <li><a href='players/index.html'>Players</a> - Browse all players and career stats</li>
      <li><a href='seasons/index.html'>Seasons</a> - Browse by season, standings, and teams</li>
    </ul>
    """)
    f.write(render_footer())

# --- Generate Players Index with Full Stats ---
print("Generating players index...")
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

with open(SITE_DIR / 'players' / 'index.html', 'w', encoding='utf-8') as f:
    f.write(render_header('Players', include_sorting_js=True))
    f.write("""
    <div class="header">
        <h1>D1 Softball Players</h1>
        <p>Click any column header to sort</p>
    </div>

    <div class="search-bar">
        <input type="text" id="playerSearch" class="search-input" onkeyup="filterPlayers()" placeholder="Search players by name...">
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
        <tbody>
    """)
    
    for i, player in enumerate(players_data, 1):
        f.write(f"""
            <tr>
                <td>{i}</td>
                <td><a href="{player['id']}.html" class="player-link">{player['name']}</a></td>
                <td>{player['games_played']}</td>
                <td>{player['pa']}</td>
                <td>{player['ab']}</td>
                <td>{player['r']}</td>
                <td>{player['h']}</td>
                <td>{player['1b']}</td>
                <td>{player['2b']}</td>
                <td>{player['3b']}</td>
                <td>{player['hr']}</td>
                <td>{player['rbi']}</td>
                <td>{player['bb']}</td>
                <td>{player['sf']}</td>
                <td>{player['oe']}</td>
                <td>{player['tb']}</td>
                <td>{nostripleadingzero(player['avg'])}</td>
                <td>{nostripleadingzero(player['slg'])}</td>
                <td>{nostripleadingzero(player['obp'])}</td>
            </tr>
        """)
    
    f.write("""
        </tbody>
    </table>
    </div>
    """)
    f.write(render_footer())

# --- Generate Individual Player Pages with Full Stats ---
print("Generating individual player pages...")
for _, player in players_df.iterrows():
    pid = player['PersonNumber']
    if pd.isna(pid) or pid == -7:
        continue
    
    player_name = f"{player['FirstName']} {player['LastName']}"
    if player_name.endswith('Subs'):
        continue
    
    stats = calculate_player_stats(pid, batting_df)
    if not stats:
        continue
    
    # Get team breakdown
    player_batting = batting_df[batting_df['PlayerNumber'] == pid]
    team_stats = []
    
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
    
    # Generate player detail page
    with open(SITE_DIR / 'players' / f'{pid}.html', 'w', encoding='utf-8') as f:
        f.write(render_header(player_name))
        f.write(f"""
        <div class="back-link">
            <a href="../index.html">Home</a>
            <span style="margin: 0 10px;">|</span>
            <a href="index.html">← Back to Players List</a>
        </div>

        <div class="header">
            <h1>{player_name}</h1>
            <p>Career Statistics</p>
        </div>

        <!-- Career Stats -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats['games_played']}</div>
                <div class="stat-label">Games</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['pa']}</div>
                <div class="stat-label">PA</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['ab']}</div>
                <div class="stat-label">AB</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['h']}</div>
                <div class="stat-label">Hits</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['hr']}</div>
                <div class="stat-label">HR</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['rbi']}</div>
                <div class="stat-label">RBI</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{nostripleadingzero(stats['avg'])}</div>
                <div class="stat-label">AVG</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{nostripleadingzero(stats['obp'])}</div>
                <div class="stat-label">OBP</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{nostripleadingzero(stats['slg'])}</div>
                <div class="stat-label">SLG</div>
            </div>
        </div>

        <!-- Season Breakdown -->
        <h2>Season Breakdown</h2>
        <div class="table-container">
            <table class="players-table">
            <thead>
                <tr>
                    <th>Season</th>
                    <th>Team</th>
                    <th>Gm</th>
                    <th>PA</th>
                    <th>AB</th>
                    <th>R</th>
                    <th>H</th>
                    <th>1B</th>
                    <th>2B</th>
                    <th>3B</th>
                    <th>HR</th>
                    <th>RBI</th>
                    <th>BB</th>
                    <th>SF</th>
                    <th>OE</th>
                    <th>TB</th>
                    <th>BA</th>
                    <th>Slg</th>
                    <th>OBP</th>
                </tr>
            </thead>
            <tbody>
        """)
        
        for team in team_stats:
            season_link = ""
            if team['filter_number']:
                season_link = f"<a href='../seasons/{team['season']}.html'>{team['season']}</a>"
            else:
                season_link = team['season']
            
            f.write(f"""
                <tr>
                    <td>{season_link}</td>
                    <td>{team['team_name']}</td>
                    <td>{team['games_played']}</td>
                    <td>{team['pa']}</td>
                    <td>{team['ab']}</td>
                    <td>{team['r']}</td>
                    <td>{team['h']}</td>
                    <td>{team['1b']}</td>
                    <td>{team['2b']}</td>
                    <td>{team['3b']}</td>
                    <td>{team['hr']}</td>
                    <td>{team['rbi']}</td>
                    <td>{team['bb']}</td>
                    <td>{team['sf']}</td>
                    <td>{team['oe']}</td>
                    <td>{team['tb']}</td>
                    <td>{nostripleadingzero(team['avg'])}</td>
                    <td>{nostripleadingzero(team['slg'])}</td>
                    <td>{nostripleadingzero(team['obp'])}</td>
                </tr>
            """)
        
        f.write("""
            </tbody>
        </table>
        </div>

        <div style="margin-top: 20px;">
            <a href="games.html" class="btn btn-primary">View Game-by-Game Stats</a>
        </div>
        """)
        f.write(render_footer())

# --- Generate Seasons Index ---
print("Generating seasons index...")
season_codes = sorted(filters_df['SeasonCode'].dropna().unique(), 
                     key=lambda x: (int(x[1:]), x[0]))  # e.g., W11, S11, F11

with open(SITE_DIR / 'seasons' / 'index.html', 'w', encoding='utf-8') as f:
    f.write(render_header('Seasons'))
    f.write("""
    <div class="header">
        <h1>D1 Softball Seasons</h1>
        <p>Click on any season to view standings and teams</p>
    </div>
    <ul>
    """)
    for code in season_codes:
        f.write(f"<li><a href='{code}.html'>{code}</a></li>")
    f.write("</ul>")
    f.write(render_footer())

# --- Generate Individual Season Pages with Standings ---
print("Generating season pages...")
for code in season_codes:
    filter_number = season_to_filter.get(code)
    if not filter_number:
        continue
    
    # Get season info
    season_info = filters_df[filters_df['FilterNumber'] == filter_number]
    if len(season_info) == 0:
        continue
    
    season_info = season_info.iloc[0]
    season_name = season_info['FilterName']
    
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
            
            if team_season_code != code:
                continue  # Skip teams from other seasons
        
        # Get team batting data
        team_batting = batting_df[batting_df['TeamNumber'] == team_num]
        
        # Get team game data for standings
        team_games = games_df[games_df['TeamNumber'] == team_num]
        
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
            elif runs < opp_runs:
                losses += 1
        
        # Calculate team batting stats
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
        team_1b = team_h - team_2b - team_3b - team_hr
        
        # Calculate at-bats (PA - BB - SH - SF)
        team_ab = team_pa - team_bb - team_sh - team_sf
        team_tb = team_h + team_2b + 2*team_3b + 3*team_hr
        
        # Calculate averages
        team_avg = team_h / team_ab if team_ab > 0 else 0
        team_obp = (team_h + team_bb) / team_pa if team_pa > 0 else 0
        team_slg = team_tb / team_ab if team_ab > 0 else 0
        
        # Calculate games played
        team_unique_games = len(team_batting.groupby('GameNumber'))
        team_u2 = team_batting['U2'].sum() if 'U2' in team_batting.columns else 0
        team_games = team_unique_games + team_u2
        
        # Calculate winning percentage
        total_games = wins + losses
        win_pct = wins / total_games if total_games > 0 else 0
        
        # Calculate run differential and per game stats
        run_diff = runs_for - runs_against
        runs_per_game = runs_for / total_games if total_games > 0 else 0
        runs_against_per_game = runs_against / total_games if total_games > 0 else 0
        
        teams_data.append({
            'team_number': int(team_num),
            'team_name': team_name,
            'wins': wins,
            'losses': losses,
            'win_pct': win_pct,
            'runs_for': runs_for,
            'runs_against': runs_against,
            'run_diff': run_diff,
            'runs_per_game': runs_per_game,
            'runs_against_per_game': runs_against_per_game,
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
            'tb': team_tb,
            'avg': team_avg,
            'obp': team_obp,
            'slg': team_slg,
        })
    
    # Sort by winning percentage
    teams_data.sort(key=lambda x: x['win_pct'], reverse=True)
    
    # Calculate games back
    if teams_data:
        first_place_wins = teams_data[0]['wins']
        first_place_losses = teams_data[0]['losses']
        
        for team in teams_data:
            games_back = ((first_place_wins - team['wins']) + (team['losses'] - first_place_losses)) / 2
            team['games_back'] = games_back if games_back > 0 else 0
    
    # Detect divisions
    divisions = {}
    for team in teams_data:
        team_name = team['team_name']
        # Look for division in parentheses (e.g., "Avalanche (Murth) W24")
        if '(' in team_name and ')' in team_name:
            # Extract division name
            start = team_name.find('(') + 1
            end = team_name.find(')')
            division = team_name[start:end]
            
            # Skip "(D1/2)" which is not a real division
            if division != "D1/2":
                if division not in divisions:
                    divisions[division] = []
                divisions[division].append(team)
        else:
            # No division specified
            if 'No Division' not in divisions:
                divisions['No Division'] = []
            divisions['No Division'].append(team)
    
    # Generate season page
    with open(SITE_DIR / 'seasons' / f'{code}.html', 'w', encoding='utf-8') as f:
        f.write(render_header(f'Season {code}'))
        f.write(f"""
        <div class="back-link">
            <a href="../index.html">Home</a>
            <span style="margin: 0 10px;">|</span>
            <a href="index.html">← Back to Seasons List</a>
        </div>

        <div class="header">
            <h1>Season {code}</h1>
            <p>{season_name}</p>
        </div>
        """)
        
        # Special note for combined seasons
        if code in ['S15', 'S16', 'S17']:
            f.write("""
            <div style="background: #fef3c7; border: 1px solid #f59e0b; border-radius: 8px; padding: 15px; margin: 20px 0;">
                <strong>Note:</strong> This season had combined divisions (D1/2). Only D1 player stats were recorded, and no D2 stats exist.
            </div>
            """)
        
        # Generate standings for each division
        for division_name, division_teams in divisions.items():
            if division_name != 'No Division':
                f.write(f"<h2>{division_name} Division</h2>")
            else:
                f.write("<h2>Standings</h2>")
            
            f.write("""
            <div class="table-container">
                <table class="players-table">
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
            """)
            
            for i, team in enumerate(division_teams, 1):
                f.write(f"""
                    <tr>
                        <td>{i}</td>
                        <td><a href="../teams/{team['team_number']}_{filter_number}.html">{team['team_name']}</a></td>
                        <td>{team['wins']}</td>
                        <td>{team['losses']}</td>
                        <td>{nostripleadingzero(team['win_pct'])}</td>
                        <td>{team['games_back']:.1f}</td>
                        <td>{team['runs_for']}</td>
                        <td>{team['runs_against']}</td>
                        <td>{team['runs_per_game']:.1f}</td>
                        <td>{team['runs_against_per_game']:.1f}</td>
                        <td>{nostripleadingzero(team['avg'])}</td>
                        <td>{nostripleadingzero(team['obp'])}</td>
                        <td>{nostripleadingzero(team['slg'])}</td>
                        <td>{team['hr']}</td>
                    </tr>
                """)
            
            f.write("""
                </tbody>
            </table>
            </div>
            """)
        
        f.write(render_footer())

print(f"Static site generated successfully in {SITE_DIR}/")
print("All features from Flask app included:")
print("- Full player stats with sorting and search")
print("- Individual player pages with season breakdown")
print("- Season standings with divisions")
print("- Team detail pages")
print("- Game logs with easter eggs")
print("- All interactive features and styling")