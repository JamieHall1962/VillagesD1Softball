"""
Export script to create Excel file for Doug (data entry)
- Tab 1: W26 team rosters with player IDs
- Tab 2: All other players in database (for reference, to avoid duplicates)
"""

import sqlite3
import pandas as pd
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('softball_stats.db')
    conn.row_factory = sqlite3.Row
    return conn

def export_for_doug(season_code='W26'):
    """
    Export rosters and all players to Excel for Doug
    """
    conn = get_db_connection()
    
    # ===== TAB 1: W26 ROSTERS =====
    print(f"Getting {season_code} rosters...")
    
    # Get all teams for this season
    teams_query = '''
        SELECT TeamNumber, LongTeamName, Manager
        FROM Teams
        WHERE LongTeamName LIKE '%' || ? || '%'
        ORDER BY LongTeamName
    '''
    teams = conn.execute(teams_query, (season_code,)).fetchall()
    
    if not teams:
        print(f"No teams found for season {season_code}")
        conn.close()
        return
    
    print(f"Found {len(teams)} teams for {season_code}")
    
    # Get roster for each team
    roster_data = []
    for team in teams:
        team_number = team['TeamNumber']
        team_name = team['LongTeamName']
        manager = team['Manager'] or ''
        
        # Remove season code from team name for cleaner display
        import re
        clean_team_name = re.sub(r'\s+[A-Z]\d{2}$', '', team_name)
        
        # Get players on this team's roster (excluding subs)
        roster_query = '''
            SELECT 
                p.PersonNumber,
                p.FirstName,
                p.LastName
            FROM People p
            JOIN Roster r ON p.PersonNumber = r.PersonNumber
            WHERE r.TeamNumber = ?
                AND p.LastName != 'Subs'
                AND p.FirstName NOT LIKE '%Sub%'
                AND p.LastName NOT LIKE '%Sub%'
            ORDER BY p.LastName, p.FirstName
        '''
        players = conn.execute(roster_query, (team_number,)).fetchall()
        
        for player in players:
            full_name = f"{player['FirstName']} {player['LastName']}"
            is_manager = 'YES' if full_name.strip() == manager.strip() else ''
            
            roster_data.append({
                'Team': clean_team_name,
                'PlayerID': player['PersonNumber'],
                'FirstName': player['FirstName'],
                'LastName': player['LastName'],
                'Manager': is_manager
            })
    
    roster_df = pd.DataFrame(roster_data)
    print(f"Total roster entries: {len(roster_df)}")
    
    # ===== TAB 2: ALL OTHER PLAYERS =====
    print("Getting all other players...")
    
    # Get PersonNumbers of players already on W26 rosters
    w26_players_query = '''
        SELECT DISTINCT r.PersonNumber
        FROM Roster r
        JOIN Teams t ON r.TeamNumber = t.TeamNumber
        WHERE t.LongTeamName LIKE '%' || ? || '%'
    '''
    w26_player_ids = [row['PersonNumber'] for row in conn.execute(w26_players_query, (season_code,)).fetchall()]
    
    # Get all other players (excluding subs)
    if w26_player_ids:
        placeholders = ','.join(['?' for _ in w26_player_ids])
        all_players_query = f'''
            SELECT 
                p.PersonNumber as PlayerID,
                p.FirstName,
                p.LastName
            FROM People p
            WHERE p.PersonNumber NOT IN ({placeholders})
                AND p.LastName != 'Subs'
                AND p.FirstName NOT LIKE '%Sub%'
                AND p.LastName NOT LIKE '%Sub%'
                AND LOWER(p.FirstName) NOT LIKE '%substitute%'
                AND LOWER(p.LastName) NOT LIKE '%substitute%'
            ORDER BY p.LastName, p.FirstName
        '''
        other_players = conn.execute(all_players_query, w26_player_ids).fetchall()
    else:
        all_players_query = '''
            SELECT 
                p.PersonNumber as PlayerID,
                p.FirstName,
                p.LastName
            FROM People p
            WHERE p.LastName != 'Subs'
                AND p.FirstName NOT LIKE '%Sub%'
                AND p.LastName NOT LIKE '%Sub%'
                AND LOWER(p.FirstName) NOT LIKE '%substitute%'
                AND LOWER(p.LastName) NOT LIKE '%substitute%'
            ORDER BY p.LastName, p.FirstName
        '''
        other_players = conn.execute(all_players_query).fetchall()
    
    other_players_data = []
    for player in other_players:
        other_players_data.append({
            'PlayerID': player['PlayerID'],
            'FirstName': player['FirstName'],
            'LastName': player['LastName']
        })
    
    other_players_df = pd.DataFrame(other_players_data)
    print(f"Total other players: {len(other_players_df)}")
    
    conn.close()
    
    # ===== EXPORT TO EXCEL =====
    output_filename = f'Doug_{season_code}_Rosters_{datetime.now().strftime("%Y%m%d")}.xlsx'
    
    with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
        roster_df.to_excel(writer, sheet_name=f'{season_code} Rosters', index=False)
        other_players_df.to_excel(writer, sheet_name='All Other Players', index=False)
    
    print(f"\nExport complete: {output_filename}")
    print(f"   - {season_code} Rosters: {len(roster_df)} players on {len(teams)} teams")
    print(f"   - All Other Players: {len(other_players_df)} players")
    
    return output_filename

if __name__ == '__main__':
    export_for_doug('W26')

