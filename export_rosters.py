#!/usr/bin/env python3
"""
Export Team Rosters to Excel
Creates spreadsheet with all F25 teams, players, and IDs for live data entry
"""

import sqlite3
import pandas as pd
from datetime import datetime

class RosterExporter:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def get_f25_teams(self):
        """Get all F25 teams"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT TeamNumber, LongTeamName, Manager
            FROM Teams 
            WHERE LongTeamName LIKE '% F25'
            ORDER BY LongTeamName
        """)
        return cursor.fetchall()

    def get_team_players(self, team_number):
        """Get all players for a specific team - subs last"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.PersonNumber, p.FirstName, p.LastName, p.player_id
            FROM People p
            JOIN Roster r ON p.PersonNumber = r.PersonNumber
            WHERE r.TeamNumber = ?
            ORDER BY 
                CASE WHEN p.LastName = 'Subs' THEN 1 ELSE 0 END,
                p.LastName, p.FirstName
        """, (team_number,))
        return cursor.fetchall()

    def get_subs_person(self):
        """Get The Sandlot Subs person - NO LONGER NEEDED"""
        # This method is no longer used since subs are now in rosters
        pass

    def export_to_excel(self, filename="F25_Team_Rosters.xlsx"):
        """Export all team rosters to Excel"""
        
        # Get all F25 teams
        teams = self.get_f25_teams()
        print(f"Found {len(teams)} F25 teams")
        
        # Prepare data for Excel
        roster_data = []
        
        for team in teams:
            team_number = team['TeamNumber']
            team_name = team['LongTeamName']
            manager_name = team['Manager'] or ""
            
            print(f"Processing {team_name}...")
            
            # Get players for this team (now includes their individual sub)
            players = self.get_team_players(team_number)
            
            for player in players:
                player_name = f"{player['FirstName']} {player['LastName']}"
                
                roster_data.append({
                    'Team_Name': team_name,
                    'Team_ID': team_number,
                    'Player_Name': player_name,
                    'Player_ID': player['PersonNumber'],
                    'First_Name': player['FirstName'],
                    'Last_Name': player['LastName']
                })
        
        # Create DataFrame
        df = pd.DataFrame(roster_data)
        
        # Create Excel file with simplified sheets
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            
            # Main roster sheet - all teams including subs
            df.to_excel(writer, sheet_name='All_Teams', index=False)
            
            # Summary sheet
            summary_data = []
            for team in teams:
                team_name = team['LongTeamName']
                team_players = df[df['Team_Name'] == team_name]
                # Count players ending in "Subs" as subs
                subs_players = team_players[team_players['Last_Name'] == 'Subs']
                regular_players = team_players[team_players['Last_Name'] != 'Subs']
                
                summary_data.append({
                    'Team_Name': team_name,
                    'Team_ID': team['TeamNumber'],
                    'Manager': team['Manager'] or 'No Manager',
                    'Regular_Players': len(regular_players),
                    'Subs': len(subs_players),
                    'Total_Players': len(team_players)
                })
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Team_Summary', index=False)
        
        print(f"\nExcel file created: {filename}")
        print(f"Total teams: {len(teams)}")
        print(f"Total roster entries: {len(roster_data)}")
        print(f"Sheets created: All_Teams, Team_Summary")
        
        # Print summary
        print(f"\nTeam Summary:")
        for team in teams:
            team_name = team['LongTeamName']
            team_players = df[df['Team_Name'] == team_name]
            subs_players = team_players[team_players['Last_Name'] == 'Subs']
            regular_players = team_players[team_players['Last_Name'] != 'Subs']
            print(f"  {team_name}: {len(regular_players)} players + {len(subs_players)} sub")
        
        return filename

def main():
    """Main execution function"""
    
    db_path = "softball_stats.db"
    output_filename = f"F25_Team_Rosters_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    print("Fall 2025 Team Roster Export")
    print("=" * 40)
    
    try:
        with RosterExporter(db_path) as exporter:
            filename = exporter.export_to_excel(output_filename)
        
        print(f"\n✅ Success! Excel file created: {filename}")
        print("\nThe file contains:")
        print("  • All_Teams sheet: Complete roster with all IDs (including subs)")
        print("  • Team_Summary sheet: Overview of all teams")
        print("\nColumns include:")
        print("  • Team_Name, Team_ID")
        print("  • Player_Name, Player_ID") 
        print("  • First_Name, Last_Name")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()