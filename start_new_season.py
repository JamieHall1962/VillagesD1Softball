#!/usr/bin/env python3
"""
Softball Database New Season Setup Script
Creates new season, teams, rosters, adds subs, and exports Excel file
"""

import sqlite3
import csv
import re
import pandas as pd
from difflib import SequenceMatcher
from datetime import datetime

class NewSeasonManager:
    def __init__(self, db_path, csv_path):
        self.db_path = db_path
        self.csv_path = csv_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        
        # Track decisions for reporting
        self.exact_matches = []
        self.fuzzy_matches = []
        self.new_players = []
        self.new_subs = []
        self.teams_created = []
        self.season_info = {}
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
    
    def get_next_filter_number(self):
        """Get the next FilterNumber for seasons"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(CAST(FilterNumber AS INTEGER)) FROM Seasons WHERE FilterNumber GLOB '[0-9]*'")
        result = cursor.fetchone()
        return (result[0] or 0) + 1
    
    def create_season(self, season_name, short_name, year):
        """Create new season record"""
        filter_number = self.get_next_filter_number()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO Seasons (FilterNumber, season_name, short_name, Champion)
            VALUES (?, ?, ?, NULL)
        """, (str(filter_number), season_name, short_name))
        
        self.season_info = {
            'FilterNumber': filter_number,
            'season_name': season_name,
            'short_name': short_name,
            'year': year
        }
        
        print(f"Created season: {season_name} (FilterNumber: {filter_number})")
        return filter_number
    
    def create_team(self, team_name, short_name, manager_name=None):
        """Create new team record"""
        # Convert team name to proper case, but preserve acronyms like USA
        team_name_proper = team_name.title()
        # Fix common acronyms that .title() breaks
        team_name_proper = team_name_proper.replace('Usa', 'USA')
        full_team_name = f"{team_name_proper} {short_name}"
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO Teams (LongTeamName, Manager)
            VALUES (?, ?)
        """, (full_team_name, manager_name))
        
        team_number = cursor.lastrowid
        self.teams_created.append({
            'TeamNumber': team_number,
            'LongTeamName': full_team_name,
            'original_name': team_name,
            'Manager': manager_name
        })
        
        manager_text = f" (Manager: {manager_name})" if manager_name else ""
        print(f"Created team: {full_team_name}{manager_text} (TeamNumber: {team_number})")
        return team_number
    
    def get_existing_people(self):
        """Get all existing people for matching"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT PersonNumber, FirstName, LastName FROM People")
        return {row['PersonNumber']: {'FirstName': row['FirstName'], 'LastName': row['LastName']} 
                for row in cursor.fetchall()}
    
    def normalize_name(self, name):
        """Normalize name for matching (handle common variations)"""
        name = name.strip().upper()
        
        # Bidirectional nickname mappings - more comprehensive
        name_mappings = {
            # Mike/Michael group
            'MIKE': 'MICHAEL', 'MICHAEL': 'MICHAEL',
            # Bob/Robert group  
            'BOB': 'ROBERT', 'ROBERT': 'ROBERT',
            # Bill/William group
            'BILL': 'WILLIAM', 'BILLY': 'WILLIAM', 'WILLIAM': 'WILLIAM',
            # Jim/James group
            'JIM': 'JAMES', 'JAMES': 'JAMES', 'JIMMY': 'JAMES',
            # Tom/Thomas group
            'TOM': 'THOMAS', 'THOMAS': 'THOMAS', 'TOMMY': 'THOMAS',
            # Rick/Richard group
            'RICK': 'RICHARD', 'RICHARD': 'RICHARD', 'DICK': 'RICHARD',
            # Dave/David group
            'DAVE': 'DAVID', 'DAVID': 'DAVID', 'DAVEY': 'DAVID',
            # Steve/Steven group
            'STEVE': 'STEVEN', 'STEVEN': 'STEVEN', 'STEVIE': 'STEVEN',
            # Tony/Anthony group
            'TONY': 'ANTHONY', 'ANTHONY': 'ANTHONY',
            # Matt/Matthew group
            'MATT': 'MATTHEW', 'MATTHEW': 'MATTHEW',
            # Dan/Daniel group
            'DAN': 'DANIEL', 'DANIEL': 'DANIEL', 'DANNY': 'DANIEL',
            # Joe/Joseph group
            'JOE': 'JOSEPH', 'JOSEPH': 'JOSEPH', 'JOEY': 'JOSEPH',
            # Chris/Christopher group
            'CHRIS': 'CHRISTOPHER', 'CHRISTOPHER': 'CHRISTOPHER',
            # Don/Donald group
            'DON': 'DONALD', 'DONALD': 'DONALD', 'DONNY': 'DONALD',
            # Ron/Ronald group  
            'RON': 'RONALD', 'RONALD': 'RONALD', 'RONNIE': 'RONALD',
            # Pat/Patrick group
            'PAT': 'PATRICK', 'PATRICK': 'PATRICK', 'PATTY': 'PATRICK',
            # Terry/Terrance group
            'TERRY': 'TERRANCE', 'TERRANCE': 'TERRANCE', 'TERENCE': 'TERRANCE',
            # Greg/Gregory group
            'GREG': 'GREGORY', 'GREGORY': 'GREGORY',
            # Jeff/Jeffrey group
            'JEFF': 'JEFFREY', 'JEFFREY': 'JEFFREY',
            # Jan group (keep as is for compound names)
            'JAN': 'JAN'
        }
        
        return name_mappings.get(name, name)
    
    def find_person_match(self, first_name, last_name, existing_people):
        """Find matching person - exact first, then fuzzy"""
        first_norm = self.normalize_name(first_name)
        last_norm = self.normalize_name(last_name)
        
        # Try exact match first (with normalization)
        for person_id, person in existing_people.items():
            existing_first = self.normalize_name(person['FirstName'])
            existing_last = self.normalize_name(person['LastName'])
            
            if existing_first == first_norm and existing_last == last_norm:
                return person_id, 'exact'
        
        # Try compound name matching (e.g., "JAN MICHAEL" matches "Jan")
        first_parts = first_name.upper().split()
        for person_id, person in existing_people.items():
            existing_first = self.normalize_name(person['FirstName'])
            existing_last = self.normalize_name(person['LastName'])
            
            # Check if any part of compound first name matches
            if existing_last == last_norm:
                for part in first_parts:
                    if self.normalize_name(part) == existing_first:
                        return person_id, 'exact'
                
                # Also check reverse - if existing name is compound
                existing_first_parts = person['FirstName'].upper().split()
                for existing_part in existing_first_parts:
                    if self.normalize_name(existing_part) == first_norm:
                        return person_id, 'exact'
        
        # Try fuzzy matching
        best_match = None
        best_score = 0.85  # Threshold for fuzzy matching
        
        for person_id, person in existing_people.items():
            existing_first = self.normalize_name(person['FirstName'])
            existing_last = self.normalize_name(person['LastName'])
            
            # Score based on both names
            first_score = SequenceMatcher(None, first_norm, existing_first).ratio()
            last_score = SequenceMatcher(None, last_norm, existing_last).ratio()
            combined_score = (first_score + last_score) / 2
            
            if combined_score > best_score:
                best_match = person_id
                best_score = combined_score
        
        if best_match:
            return best_match, 'fuzzy'
        
        return None, 'new'
    
    def create_person(self, first_name, last_name):
        """Create new person record"""
        cursor = self.conn.cursor()
        
        # Get next player_id
        cursor.execute("SELECT MAX(player_id) FROM People")
        result = cursor.fetchone()
        next_player_id = (result[0] or 0) + 1
        
        cursor.execute("""
            INSERT INTO People (FirstName, LastName, player_id)
            VALUES (?, ?, ?)
        """, (first_name.title(), last_name.title(), next_player_id))
        
        person_number = cursor.lastrowid
        print(f"Created new person: {first_name} {last_name} (PersonNumber: {person_number})")
        return person_number
    
    def create_roster_entry(self, team_number, person_number):
        """Create roster entry linking team and person"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO Roster (TeamNumber, PersonNumber)
            VALUES (?, ?)
        """, (team_number, person_number))
    
    def parse_csv_data(self):
        """Parse the draft CSV data - handles format with PID column"""
        import csv
        
        teams_data = {}
        
        with open(self.csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            
            print(f"CSV columns found: {reader.fieldnames}")
            
            # Expect columns: TEAM, PLAYER, IS_MANAGER, PID
            expected_cols = ['TEAM', 'PLAYER', 'IS_MANAGER', 'PID']
            if reader.fieldnames != expected_cols:
                raise ValueError(f"Expected columns: {expected_cols}, got: {reader.fieldnames}")
            
            # Read and process all data
            for row in reader:
                team = row['TEAM'].strip()
                player = row['PLAYER'].strip()
                is_manager_str = row['IS_MANAGER'].strip().lower() if row['IS_MANAGER'] else ''
                is_manager = is_manager_str in ['yes', 'y', 'true', '1']
                pid_str = row['PID'].strip() if row['PID'] else ''
                pid = int(pid_str) if pid_str else None
                
                # Initialize team if not seen before
                if team not in teams_data:
                    teams_data[team] = {'players': [], 'manager': None}
                
                # Parse player name - handle "LASTNAME, FIRSTNAME" format
                if ',' in player:
                    last, first = player.split(',', 1)
                    first_name = first.strip()
                    last_name = last.strip()
                    
                    if first_name and last_name:
                        player_info = {
                            'draft_position': len(teams_data[team]['players']) + 1,
                            'first_name': first_name,
                            'last_name': last_name,
                            'is_manager': is_manager,
                            'pid': pid  # PersonNumber - None if new player
                        }
                        
                        teams_data[team]['players'].append(player_info)
                        
                        # Set manager if this player is marked as manager
                        if is_manager:
                            manager_name = f"{first_name.title()} {last_name.title()}"
                            teams_data[team]['manager'] = manager_name
        
        # Count returning vs new players
        returning = sum(1 for t in teams_data.values() for p in t['players'] if p['pid'])
        new = sum(1 for t in teams_data.values() for p in t['players'] if not p['pid'])
        total = returning + new
        
        print(f"Parsed {len(teams_data)} teams with {total} players ({returning} returning, {new} new)")
        return teams_data
    
    def find_team_subs(self, short_name):
        """Find existing sub players for teams"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT PersonNumber, FirstName, LastName
            FROM People 
            WHERE LastName = 'Subs'
            ORDER BY FirstName
        """)
        return {row['FirstName']: row['PersonNumber'] for row in cursor.fetchall()}
    
    def get_base_team_name(self, full_team_name, short_name):
        """Extract base team name by removing season code and division"""
        import re
        # Remove season code (e.g., " W26")
        base_name = full_team_name.replace(f' {short_name}', '')
        # Remove division in parentheses (e.g., "(Palmese)" or "(Ballers)")
        base_name = re.sub(r'\s*\([^)]+\)\s*', '', base_name).strip()
        return base_name
    
    def add_subs_to_rosters(self, short_name):
        """Add sub players to team rosters - creates missing subs if needed"""
        print(f"\nAdding subs to team rosters...")
        
        # Get all teams for this season
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT TeamNumber, LongTeamName
            FROM Teams 
            WHERE LongTeamName LIKE ?
            ORDER BY LongTeamName
        """, (f'% {short_name}',))
        
        teams = cursor.fetchall()
        subs_dict = self.find_team_subs(short_name)
        
        subs_added = 0
        subs_created = 0
        missing_subs = []
        
        # First pass: identify missing subs
        for team in teams:
            team_name = team['LongTeamName']
            base_name = self.get_base_team_name(team_name, short_name)
            
            if base_name not in subs_dict:
                missing_subs.append(base_name)
        
        # Create missing subs if any
        if missing_subs:
            print(f"  Found {len(missing_subs)} teams needing new subs:")
            for team_name in missing_subs:
                print(f"    {team_name} Subs")
            
            # Get next player_id
            cursor.execute("SELECT MAX(player_id) FROM People")
            result = cursor.fetchone()
            next_player_id = (result[0] or 0) + 1
            
            # Create missing subs
            for i, team_name in enumerate(missing_subs):
                cursor.execute("""
                    INSERT INTO People (FirstName, LastName, player_id)
                    VALUES (?, 'Subs', ?)
                """, (team_name, next_player_id + i))
                
                new_person_number = cursor.lastrowid
                subs_dict[team_name] = new_person_number
                subs_created += 1
                
                # Track for reporting
                self.new_subs.append({
                    'team_name': team_name,
                    'person_number': new_person_number,
                    'player_id': next_player_id + i
                })
                
                print(f"    Created: {team_name} Subs (PersonNumber: {new_person_number})")
        
        # Second pass: add all subs to rosters
        for team in teams:
            team_number = team['TeamNumber']
            team_name = team['LongTeamName']
            base_name = self.get_base_team_name(team_name, short_name)
            
            if base_name in subs_dict:
                sub_person_number = subs_dict[base_name]
                
                # Add to roster
                cursor.execute("""
                    INSERT INTO Roster (TeamNumber, PersonNumber)
                    VALUES (?, ?)
                """, (team_number, sub_person_number))
                
                status = "CREATED" if base_name in missing_subs else "EXISTING"
                print(f"  Added {base_name} Subs to {team_name} ({status})")
                subs_added += 1
            else:
                print(f"  ERROR: Still no sub found for {base_name}")
        
        if subs_created > 0:
            print(f"\n[OK] Created {subs_created} new sub players")
        print(f"[OK] Added {subs_added} subs to rosters")
        
        return {'added': subs_added, 'created': subs_created}
    
    def get_season_teams(self, short_name):
        """Get all teams for this season"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT TeamNumber, LongTeamName, Manager
            FROM Teams 
            WHERE LongTeamName LIKE ?
            ORDER BY LongTeamName
        """, (f'% {short_name}',))
        return cursor.fetchall()
    
    def get_team_players_for_export(self, team_number):
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
    
    def export_to_excel(self, short_name, filename=None):
        """Export all team rosters to Excel"""
        if filename is None:
            filename = f"{short_name}_Team_Rosters_{datetime.now().strftime('%Y%m%d')}.xlsx"
        
        print(f"\nExporting rosters to Excel...")
        
        # Get all teams for this season
        teams = self.get_season_teams(short_name)
        print(f"Found {len(teams)} teams")
        
        # Prepare data for Excel
        roster_data = []
        
        for team in teams:
            team_number = team['TeamNumber']
            team_name = team['LongTeamName']
            manager_name = team['Manager'] or ""
            
            # Get players for this team (now includes their individual sub)
            players = self.get_team_players_for_export(team_number)
            
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
        
        # Create Excel file
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            
            # Main roster sheet
            df.to_excel(writer, sheet_name='All_Teams', index=False)
            
            # Summary sheet
            summary_data = []
            for team in teams:
                team_name = team['LongTeamName']
                team_players = df[df['Team_Name'] == team_name]
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
        
        print(f"Excel file created: {filename}")
        print(f"Total roster entries: {len(roster_data)}")
        
        # Print summary
        print(f"\nTeam Summary:")
        for team in teams:
            team_name = team['LongTeamName']
            team_players = df[df['Team_Name'] == team_name]
            subs_players = team_players[team_players['Last_Name'] == 'Subs']
            regular_players = team_players[team_players['Last_Name'] != 'Subs']
            print(f"  {team_name}: {len(regular_players)} players + {len(subs_players)} sub")
        
        return filename
    
    def process_season(self, season_name="Fall 2025", short_name="F25", year=2025):
        """Main processing function"""
        print(f"Starting new season setup: {season_name}")
        print("=" * 50)
        
        # Create season
        filter_number = self.create_season(season_name, short_name, year)
        
        # Parse CSV data
        print("\nParsing draft data...")
        teams_data = self.parse_csv_data()
        
        # Get existing people for matching
        existing_people = self.get_existing_people()
        print(f"Found {len(existing_people)} existing people in database")
        
        # Process each team
        for team_name, team_data in teams_data.items():
            print(f"\nProcessing team: {team_name}")
            print("-" * 30)
            
            # Create team with manager
            manager_name = team_data.get('manager')
            team_number = self.create_team(team_name, short_name, manager_name)
            
            # Process each player
            for player_info in team_data['players']:
                first_name = player_info['first_name']
                last_name = player_info['last_name']
                draft_pos = player_info['draft_position']
                is_manager = player_info.get('is_manager', False)
                pid = player_info.get('pid')  # PersonNumber from CSV
                
                manager_flag = " (MANAGER)" if is_manager else ""
                
                if pid:
                    # Returning player - use PID directly
                    person_id = pid
                    db_name = f"{existing_people[pid]['FirstName']} {existing_people[pid]['LastName']}" if pid in existing_people else "UNKNOWN"
                    
                    self.exact_matches.append({
                        'team': team_name,
                        'draft_pos': draft_pos,
                        'name': f"{first_name} {last_name}",
                        'person_id': person_id,
                        'existing_name': db_name,
                        'is_manager': is_manager
                    })
                    print(f"  {draft_pos}. {first_name} {last_name}{manager_flag} -> PID {person_id} ({db_name})")
                
                else:
                    # New player - create record
                    person_id = self.create_person(first_name, last_name)
                    self.new_players.append({
                        'team': team_name,
                        'draft_pos': draft_pos,
                        'name': f"{first_name} {last_name}",
                        'person_id': person_id,
                        'is_manager': is_manager
                    })
                    print(f"  {draft_pos}. {first_name} {last_name}{manager_flag} -> NEW PLAYER (PersonNumber: {person_id})")
                
                # Create roster entry
                self.create_roster_entry(team_number, person_id)
        
        # Add subs to all team rosters
        print("DEBUG: About to call add_subs_to_rosters()")
        subs_result = self.add_subs_to_rosters(short_name)
        print(f"DEBUG: Subs result: {subs_result}")
        
        # Commit all changes
        self.conn.commit()
        
        # Export to Excel
        excel_filename = self.export_to_excel(short_name)
        
        # Generate final report
        self.generate_report(excel_filename, subs_result)
    
    def generate_report(self, excel_filename=None, subs_result=None):
        """Generate summary report"""
        print("\n" + "=" * 60)
        print("NEW SEASON SETUP COMPLETE")
        print("=" * 60)
        
        print(f"\nSeason Created:")
        print(f"  Name: {self.season_info['season_name']}")
        print(f"  Short: {self.season_info['short_name']}")
        print(f"  FilterNumber: {self.season_info['FilterNumber']}")
        
        print(f"\nTeams Created: {len(self.teams_created)}")
        for team in self.teams_created:
            manager_text = f" (Manager: {team['Manager']})" if team['Manager'] else " (No Manager)"
            print(f"  {team['LongTeamName']}{manager_text} (TeamNumber: {team['TeamNumber']})")
        
        if subs_result:
            print(f"\nSubs Management:")
            if subs_result['created'] > 0:
                print(f"  New subs created: {subs_result['created']}")
            print(f"  Subs added to rosters: {subs_result['added']}")
        
        print(f"\nPlayer Summary:")
        print(f"  Returning players: {len(self.exact_matches)}")
        print(f"  New players: {len(self.new_players)}")
        print(f"  New subs: {len(self.new_subs)}")
        
        if self.new_subs:
            print(f"\nNEW SUBS CREATED:")
            for sub in self.new_subs:
                print(f"  {sub['team_name']} Subs (PersonNumber: {sub['person_number']})")
        
        if self.new_players:
            print(f"\nNEW PLAYERS CREATED:")
            for player in self.new_players:
                manager_flag = " (MANAGER)" if player.get('is_manager') else ""
                print(f"  {player['team']}: {player['name']}{manager_flag} (PersonNumber: {player['person_id']})")
        
        total_roster_entries = len(self.exact_matches) + len(self.new_players)
        if subs_result:
            total_roster_entries += subs_result['added']
        
        print(f"\nTotal roster entries created: {total_roster_entries}")
        
        if excel_filename:
            print(f"\nExcel roster file created: {excel_filename}")
        
        print(f"\n[OK] SETUP COMPLETE - Ready for {self.season_info['season_name']} season!")


def main():
    """Main execution function"""
    
    # ============================================================
    # CONFIGURE THESE FOR EACH NEW SEASON
    # ============================================================
    db_path = "softball_stats.db"
    csv_path = "draft_w26.csv"          # Draft CSV file with PID column
    season_name = "Winter 2026"          # Full season name
    short_name = "W26"                   # Short code (used in team names)
    year = 2026                          # Year
    # ============================================================
    
    print(f"NEW SEASON SETUP")
    print(f"=" * 50)
    print(f"Database: {db_path}")
    print(f"Draft CSV: {csv_path}")
    print(f"Season: {season_name} ({short_name})")
    print(f"=" * 50)
    
    try:
        with NewSeasonManager(db_path, csv_path) as manager:
            manager.process_season(season_name, short_name, year)
        
        print(f"\nSuccess! Database updated and Excel file created.")
        print(f"Excel roster file is ready for live data entry.")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
        print(f"Make sure both '{db_path}' and '{csv_path}' are in the same folder as this script.")
        print(f"Also ensure pandas is installed: pip install pandas openpyxl")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()