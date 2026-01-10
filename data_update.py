#!/usr/bin/env python3
"""
Complete Softball Stats Sync - All Tables + Sub Logic + Aggregation
"""

import sqlite3
import pandas as pd
from datetime import datetime
import shutil

# HARDCODED SUB MAPPINGS FOR FALL 2025
SUBS_MAPPING_F25 = {
    529: 600,   # Bad News Bears Subs
    534: 493,   # Buckeyes Subs  
    527: 480,   # Clippers Subs
    532: 540,   # Lightning Strikes Subs
    537: 584,   # Norsemen Subs
    531: 542,   # Raptors Subs
    533: 302,   # Rebels Subs
    535: 548,   # Shorebirds Subs
    526: 274,   # Stars Subs
    536: 617,   # The Sandlot Subs
    528: 400,   # Warhawks Subs
    530: 554,   # Xtreme Subs
}

# HARDCODED SUB MAPPINGS FOR WINTER 2026
SUBS_MAPPING_W26 = {
    542: 600,   # Bad News Bears Subs
    543: 560,   # Bearcats Subs
    544: 630,   # Big Dawgs Subs
    538: 493,   # Buckeyes Subs
    545: 580,   # Death Stars Subs
    546: 538,   # Gunslingers Subs
    547: 540,   # Lightning Strikes Subs
    539: 584,   # Norsemen Subs
    548: 302,   # Rebels Subs
    549: 548,   # Shorebirds Subs
    550: 320,   # Team USA Subs
    551: 415,   # Tigers Subs
    540: 419,   # Wolverines Subs
    541: 554,   # Xtreme Subs
}

# Combined subs mapping (both seasons)
SUBS_MAPPING = {**SUBS_MAPPING_F25, **SUBS_MAPPING_W26}

# Track new players added during sync
NEW_PLAYERS_ADDED = []

# W26 Team Numbers (538-551) - filter to only process these teams
W26_TEAM_NUMBERS = set(range(538, 552))  # 538 to 551 inclusive

# Set this to filter data by season (None = process all, 'W26' = only W26)
SEASON_FILTER = 'W26'

def extract_table(csv_file, table_name):
    """Extract a specific table from the multi-table CSV"""
    with open(csv_file, 'r') as f:
        lines = f.readlines()
    
    # Find table section
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith(f"Table: {table_name}"):
            start_idx = i + 1
            break
    
    if start_idx is None:
        print(f"Table {table_name} not found")
        return None
    
    # Find end of section  
    end_idx = len(lines)
    for i in range(start_idx, len(lines)):
        if lines[i].strip().startswith("Table: "):
            end_idx = i
            break
    
    # Write section to temp file
    temp_file = f"temp_{table_name.lower()}.csv"
    with open(temp_file, 'w') as f:
        f.writelines(lines[start_idx:end_idx])
    
    return temp_file

def apply_subs_logic(df):
    """Apply sub player redirections"""
    sub_count = 0
    if 'Roster' in df.columns:
        for i in range(len(df)):
            if df.iloc[i]['Roster'] == 'Sub':
                team_num = df.iloc[i]['TeamNumber']
                if team_num in SUBS_MAPPING:
                    old_player = df.iloc[i]['PersonNumber']
                    new_player = SUBS_MAPPING[team_num]
                    df.iloc[i, df.columns.get_loc('PersonNumber')] = new_player
                    print(f"  Team {team_num}: Player {old_player} -> Subs Player {new_player}")
                    sub_count += 1
    if sub_count > 0:
        print(f"Redirected {sub_count} sub records")
    return df

def sync_batting_stats(conn):
    """Sync batting stats with proper sub aggregation"""
    print("\n--- SYNCING BATTING STATS ---")
    
    temp_file = extract_table("data.csv", "BattingStats")
    if not temp_file:
        return 0, 0, 0
    
    try:
        df = pd.read_csv(temp_file)
        print(f"Loaded {len(df)} batting records from CSV")
        
        # Filter to only W26 teams if SEASON_FILTER is set
        if SEASON_FILTER == 'W26' and 'TeamNumber' in df.columns:
            before_count = len(df)
            df = df[df['TeamNumber'].isin(W26_TEAM_NUMBERS)]
            filtered_count = before_count - len(df)
            if filtered_count > 0:
                print(f"Filtered out {filtered_count} non-W26 records, keeping {len(df)} W26 records")
        
        # Apply sub logic BEFORE aggregation
        df = apply_subs_logic(df)
        
        # Column fixes
        df = df.rename(columns={'PersonNumber': 'PlayerNumber', 'D': '2B', 'T': '3B'})
        df['G'] = 1
        
        # Keep only needed columns
        cols = ['TeamNumber', 'GameNumber', 'PlayerNumber', 'HomeTeam', 'PA', 'R', 'H', '2B', '3B', 'HR', 'OE', 'BB', 'RBI', 'SF', 'G']
        available_cols = [col for col in cols if col in df.columns]
        df_clean = df[available_cols]
        
        print(f"Before aggregation: {len(df_clean)} records")
        
        # CRITICAL: AGGREGATE SUB STATS - Group by key fields and sum numeric stats
        numeric_cols = ['PA', 'R', 'H', '2B', '3B', 'HR', 'OE', 'BB', 'RBI', 'SF', 'G']
        available_numeric = [col for col in numeric_cols if col in df_clean.columns]
        
        # Group by team, game, player and sum the stats  
        numeric_cols_to_sum = ['PA', 'R', 'H', '2B', '3B', 'HR', 'OE', 'BB', 'RBI', 'SF']
        available_numeric_to_sum = [col for col in numeric_cols_to_sum if col in df_clean.columns]

        df_aggregated = df_clean.groupby(['TeamNumber', 'GameNumber', 'PlayerNumber']).agg({
            'HomeTeam': 'first',
            **{col: 'sum' for col in available_numeric_to_sum},
            'G': lambda x: 1  # Always set G to 1 for aggregated records
        }).reset_index()
        
        print(f"After aggregation: {len(df_aggregated)} unique player/game records")
        
        # Sync with database
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS temp_staging_batting")
        df_aggregated.to_sql("temp_staging_batting", conn, index=False)
        
        # Count changes
        cursor.execute("""
        SELECT COUNT(*) FROM temp_staging_batting s
        LEFT JOIN batting_stats b ON s.TeamNumber = b.TeamNumber 
                                 AND s.GameNumber = b.GameNumber 
                                 AND s.PlayerNumber = b.PlayerNumber
        WHERE b.TeamNumber IS NULL
        """)
        new_count = cursor.fetchone()[0]
        
        cursor.execute("""
        SELECT COUNT(*) FROM temp_staging_batting s
        JOIN batting_stats b ON s.TeamNumber = b.TeamNumber 
                            AND s.GameNumber = b.GameNumber 
                            AND s.PlayerNumber = b.PlayerNumber
        WHERE s.HomeTeam != b.HomeTeam OR s.PA != b.PA OR s.R != b.R OR s.H != b.H 
           OR s.[2B] != b.[2B] OR s.[3B] != b.[3B] OR s.HR != b.HR OR s.OE != b.OE 
           OR s.BB != b.BB OR s.RBI != b.RBI OR s.SF != b.SF OR s.G != b.G
        """)
        changed_count = cursor.fetchone()[0]
        
        # Execute changes
        if new_count > 0:
            cursor.execute("""
            INSERT INTO batting_stats (TeamNumber, GameNumber, PlayerNumber, HomeTeam, PA, R, H, [2B], [3B], HR, OE, BB, RBI, SF, G)
            SELECT TeamNumber, GameNumber, PlayerNumber, HomeTeam, PA, R, H, [2B], [3B], HR, OE, BB, RBI, SF, G
            FROM temp_staging_batting s
            WHERE NOT EXISTS (
                SELECT 1 FROM batting_stats b 
                WHERE s.TeamNumber = b.TeamNumber 
                AND s.GameNumber = b.GameNumber 
                AND s.PlayerNumber = b.PlayerNumber
            )
            """)
        
        if changed_count > 0:
            cursor.execute("""
            UPDATE batting_stats 
            SET HomeTeam = s.HomeTeam, PA = s.PA, R = s.R, H = s.H, [2B] = s.[2B], [3B] = s.[3B],
                HR = s.HR, OE = s.OE, BB = s.BB, RBI = s.RBI, SF = s.SF, G = s.G
            FROM temp_staging_batting s
            WHERE batting_stats.TeamNumber = s.TeamNumber 
            AND batting_stats.GameNumber = s.GameNumber 
            AND batting_stats.PlayerNumber = s.PlayerNumber
            """)
        
        cursor.execute("DROP TABLE temp_staging_batting")
        unchanged_count = len(df_aggregated) - new_count - changed_count
        
        print(f"Batting: {new_count} new, {changed_count} changed, {unchanged_count} unchanged")
        return new_count, changed_count, unchanged_count
        
    finally:
        import os
        os.remove(temp_file)

def sync_pitching_stats(conn):
    """Sync pitching stats with sub aggregation"""
    print("\n--- SYNCING PITCHING STATS ---")
    
    temp_file = extract_table("data.csv", "PitchingStats")
    if not temp_file:
        return 0, 0, 0
    
    try:
        df = pd.read_csv(temp_file)
        print(f"Loaded {len(df)} pitching records from CSV")
        
        # Filter to only W26 teams if SEASON_FILTER is set
        if SEASON_FILTER == 'W26' and 'TeamNumber' in df.columns:
            before_count = len(df)
            df = df[df['TeamNumber'].isin(W26_TEAM_NUMBERS)]
            filtered_count = before_count - len(df)
            if filtered_count > 0:
                print(f"Filtered out {filtered_count} non-W26 records, keeping {len(df)} W26 records")
        
        # Apply sub logic
        df = apply_subs_logic(df)
        
        # Column fixes
        df = df.rename(columns={'PersonNumber': 'PlayerNumber'})
        
        # Keep only needed columns
        cols = ['TeamNumber', 'GameNumber', 'PlayerNumber', 'HomeTeam', 'IP', 'BB', 'W', 'L', 'IBB']
        available_cols = [col for col in cols if col in df.columns]
        df_clean = df[available_cols]
        
        if df_clean.empty:
            print("No valid pitching data found")
            return 0, 0, 0
        
        # AGGREGATE PITCHING STATS
        numeric_cols = ['IP', 'BB', 'W', 'L', 'IBB']
        available_numeric = [col for col in numeric_cols if col in df_clean.columns]
        
        # AGGREGATE PITCHING STATS
        numeric_cols_to_sum = ['IP', 'BB', 'W', 'L', 'IBB']
        available_numeric_to_sum = [col for col in numeric_cols_to_sum if col in df_clean.columns]

        df_aggregated = df_clean.groupby(['TeamNumber', 'GameNumber', 'PlayerNumber']).agg({
            'HomeTeam': 'first',
            **{col: 'sum' for col in available_numeric_to_sum}
        }).reset_index()

        # Add G column set to 1 for all aggregated records (if G exists in the data)
        if 'G' in df_clean.columns:
            df_aggregated['G'] = 1
        
        print(f"Pitching aggregated from {len(df_clean)} to {len(df_aggregated)} records")
        
        # Sync with database
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS temp_staging_pitching")
        df_aggregated.to_sql("temp_staging_pitching", conn, index=False)
        
        # Count changes
        cursor.execute("""
        SELECT COUNT(*) FROM temp_staging_pitching s
        LEFT JOIN pitching_stats p ON s.TeamNumber = p.TeamNumber 
                                   AND s.GameNumber = p.GameNumber 
                                   AND s.PlayerNumber = p.PlayerNumber
        WHERE p.TeamNumber IS NULL
        """)
        new_count = cursor.fetchone()[0]
        
        cursor.execute("""
        SELECT COUNT(*) FROM temp_staging_pitching s
        JOIN pitching_stats p ON s.TeamNumber = p.TeamNumber 
                             AND s.GameNumber = p.GameNumber 
                             AND s.PlayerNumber = p.PlayerNumber
        WHERE s.IP != p.IP OR s.BB != p.BB OR s.W != p.W OR s.L != p.L
        """)
        changed_count = cursor.fetchone()[0]
        
        # Execute changes
        if new_count > 0:
            cursor.execute("""
            INSERT INTO pitching_stats (TeamNumber, GameNumber, PlayerNumber, HomeTeam, IP, BB, W, L, IBB)
            SELECT TeamNumber, GameNumber, PlayerNumber, HomeTeam, IP, BB, W, L, IBB
            FROM temp_staging_pitching s
            WHERE NOT EXISTS (
                SELECT 1 FROM pitching_stats p 
                WHERE s.TeamNumber = p.TeamNumber 
                AND s.GameNumber = p.GameNumber 
                AND s.PlayerNumber = p.PlayerNumber
            )
            """)
        
        if changed_count > 0:
            cursor.execute("""
            UPDATE pitching_stats 
            SET HomeTeam = s.HomeTeam, IP = s.IP, BB = s.BB, W = s.W, L = s.L, IBB = s.IBB
            FROM temp_staging_pitching s
            WHERE pitching_stats.TeamNumber = s.TeamNumber 
            AND pitching_stats.GameNumber = s.GameNumber 
            AND pitching_stats.PlayerNumber = s.PlayerNumber
            """)
        
        cursor.execute("DROP TABLE temp_staging_pitching")
        unchanged_count = len(df_aggregated) - new_count - changed_count
        
        print(f"Pitching: {new_count} new, {changed_count} changed, {unchanged_count} unchanged")
        return new_count, changed_count, unchanged_count
        
    finally:
        import os
        os.remove(temp_file)

def sync_game_stats(conn):
    """Sync game stats with missing fields populated"""
    print("\n--- SYNCING GAME STATS (Enhanced) ---")
    
    temp_file = extract_table("data.csv", "GameStats")
    if not temp_file:
        return 0, 0, 0
    
    try:
        df = pd.read_csv(temp_file)
        print(f"Loaded {len(df)} game records from CSV")
        
        # Filter to only W26 teams if SEASON_FILTER is set
        if SEASON_FILTER == 'W26' and 'TeamNumber' in df.columns:
            before_count = len(df)
            df = df[df['TeamNumber'].isin(W26_TEAM_NUMBERS)]
            filtered_count = before_count - len(df)
            if filtered_count > 0:
                print(f"Filtered out {filtered_count} non-W26 records, keeping {len(df)} W26 records")
        
        # Map CSV columns to database columns AND fix date format
        column_mapping = {
            'GameDate': 'Date',
            'INN1': 'RunsInning1', 'INN2': 'RunsInning2', 'INN3': 'RunsInning3',
            'INN4': 'RunsInning4', 'INN5': 'RunsInning5', 'INN6': 'RunsInning6', 
            'INN7': 'RunsInning7', 'INN8': 'RunsInning8', 'INN9': 'RunsInning9'
        }
        df = df.rename(columns=column_mapping)
        
        # Convert date format from M/D/YYYY to YYYY-MM-DD
        if 'Date' in df.columns:
            def fix_date_format(date_str):
                try:
                    # Parse dates like "9/5/2025 0:00" or "9/5/2025"
                    date_part = str(date_str).split()[0]  # Remove time component
                    month, day, year = date_part.split('/')
                    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                except:
                    return date_str
            
            df['Date'] = df['Date'].apply(fix_date_format)
            print(f"Sample converted dates: {df['Date'].head(3).tolist()}")
        
        # Opponent team mapping - F25 teams
        team_mapping_f25 = {
            'Bad News Bears': 529,
            'Buckeyes': 534, 
            'Clippers': 527,
            'Lightning Strikes': 532,
            'Norsemen': 537,
            'Raptors': 531,
            'Rebels': 533,
            'Shorebirds': 535,
            'Stars': 526,
            'The Sandlot': 536,
            'Warhawks': 528,
            'Xtreme': 530
        }
        
        # Opponent team mapping - W26 teams
        team_mapping_w26 = {
            'Bad News Bears': 542,
            'Bearcats': 543,
            'Big Dawgs': 544,
            'Buckeyes': 538,
            'Death Stars': 545,
            'Gunslingers': 546,
            'Lightning Strikes': 547,
            'Norsemen': 539,
            'Rebels': 548,
            'Shorebirds': 549,
            'Team USA': 550,
            'TeamUSA': 550,
            'Tigers': 551,
            'Wolverines': 540,
            'Xtreme': 541
        }
        
        # Detect which season based on TeamNumber range in the data
        # F25 teams are 526-537, W26 teams are 538-551
        if 'TeamNumber' in df.columns:
            max_team = df['TeamNumber'].max()
            if max_team >= 538:
                team_mapping = team_mapping_w26
                print("Detected W26 season data")
            else:
                team_mapping = team_mapping_f25
                print("Detected F25 season data")
        else:
            team_mapping = {**team_mapping_f25, **team_mapping_w26}
        
        # Add OpponentTeamNumber using simple mapping
        if 'Opponent' in df.columns:
            df['OpponentTeamNumber'] = df['Opponent'].map(team_mapping)
            # Check for unmapped opponents
            unmapped = df[df['OpponentTeamNumber'].isna()]['Opponent'].unique()
            if len(unmapped) > 0:
                print(f"WARNING: Unmapped opponents: {unmapped}")
        
        # Keep only the columns we need
        base_cols = ['TeamNumber', 'GameNumber', 'Date', 'Innings', 'HomeTeam', 
                    'Opponent', 'OpponentTeamNumber', 'Runs', 'OppRuns']
        inning_cols = ['RunsInning1', 'RunsInning2', 'RunsInning3', 'RunsInning4', 'RunsInning5',
                      'RunsInning6', 'RunsInning7', 'RunsInning8', 'RunsInning9']
        
        all_possible_cols = base_cols + inning_cols
        available_cols = [col for col in all_possible_cols if col in df.columns]
        df_clean = df[available_cols]
        
        print(f"Columns being synced: {available_cols}")
        
        if df_clean.empty:
            print("No valid game data found")
            return 0, 0, 0
        
        # Get current max GStatNumber and assign sequential numbers
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(MAX(GStatNumber), 0) FROM game_stats")
        max_gstat = cursor.fetchone()[0]
        print(f"Current highest GStatNumber: {max_gstat}")
        
        # Add simple sequential GStatNumbers starting from max + 1
        df_clean['GStatNumber'] = range(max_gstat + 1, max_gstat + 1 + len(df_clean))
        print(f"New records will be numbered {max_gstat + 1} to {max_gstat + len(df_clean)}")
        
        # Update available_cols to include GStatNumber
        available_cols = ['GStatNumber'] + available_cols
        
        # Add missing columns to database if needed
        cursor.execute("PRAGMA table_info(game_stats)")
        existing_columns = [row[1] for row in cursor.fetchall()]
        
        needed_columns = [
            ('GStatNumber', 'INTEGER'),
            ('OpponentTeamNumber', 'INTEGER'),
            ('OpponentGStatNumber', 'INTEGER'),
            ('OppRunsInning1', 'INTEGER DEFAULT 0'),
            ('OppRunsInning2', 'INTEGER DEFAULT 0'),
            ('OppRunsInning3', 'INTEGER DEFAULT 0'),
            ('OppRunsInning4', 'INTEGER DEFAULT 0'),
            ('OppRunsInning5', 'INTEGER DEFAULT 0'),
            ('OppRunsInning6', 'INTEGER DEFAULT 0'),
            ('OppRunsInning7', 'INTEGER DEFAULT 0'),
            ('OppRunsInning8', 'INTEGER DEFAULT 0'),
            ('OppRunsInning9', 'INTEGER DEFAULT 0')
        ]
        
        for col_name, col_def in needed_columns:
            if col_name not in existing_columns:
                print(f"Adding missing column: {col_name}")
                cursor.execute(f"ALTER TABLE game_stats ADD COLUMN {col_name} {col_def}")
        
        # Sync with database
        cursor.execute("DROP TABLE IF EXISTS temp_staging_game")
        df_clean.to_sql("temp_staging_game", conn, index=False)
        
        # Count changes
        cursor.execute("""
        SELECT COUNT(*) FROM temp_staging_game s
        LEFT JOIN game_stats g ON s.TeamNumber = g.TeamNumber 
                              AND s.GameNumber = g.GameNumber
        WHERE g.TeamNumber IS NULL
        """)
        new_count = cursor.fetchone()[0]
        
        cursor.execute("""
        SELECT COUNT(*) FROM temp_staging_game s
        JOIN game_stats g ON s.TeamNumber = g.TeamNumber 
                         AND s.GameNumber = g.GameNumber
        WHERE s.Runs != g.Runs OR s.OppRuns != g.OppRuns OR s.Innings != g.Innings
        """)
        changed_count = cursor.fetchone()[0]
        
        # Insert new records
        if new_count > 0:
            col_list = ', '.join(available_cols)
            cursor.execute(f"""
            INSERT INTO game_stats ({col_list})
            SELECT {col_list}
            FROM temp_staging_game s
            WHERE NOT EXISTS (
                SELECT 1 FROM game_stats g 
                WHERE s.TeamNumber = g.TeamNumber 
                AND s.GameNumber = g.GameNumber
            )
            """)
        
        # Update existing records
        if changed_count > 0:
            set_clauses = [f"{col} = s.{col}" for col in available_cols if col not in ['TeamNumber', 'GameNumber']]
            cursor.execute(f"""
            UPDATE game_stats 
            SET {', '.join(set_clauses)}
            FROM temp_staging_game s
            WHERE game_stats.TeamNumber = s.TeamNumber 
            AND game_stats.GameNumber = s.GameNumber
            """)
        
        cursor.execute("DROP TABLE temp_staging_game")
        
        # Second pass: Link opponent data using simple lookups
        print("Linking opponent data...")
        
        # Update OpponentGStatNumber by linking to opponent's record
        cursor.execute("""
        UPDATE game_stats 
        SET OpponentGStatNumber = (
            SELECT opp.GStatNumber 
            FROM game_stats opp 
            WHERE opp.TeamNumber = game_stats.OpponentTeamNumber 
            AND opp.GameNumber = game_stats.GameNumber
        )
        WHERE OpponentTeamNumber IS NOT NULL
        AND GStatNumber > ?
        """, (max_gstat,))
        
        # Update opponent inning data
        for i in range(1, 10):
            cursor.execute(f"""
            UPDATE game_stats 
            SET OppRunsInning{i} = (
                SELECT opp.RunsInning{i} 
                FROM game_stats opp 
                WHERE opp.GStatNumber = game_stats.OpponentGStatNumber
            )
            WHERE OpponentGStatNumber IS NOT NULL
            AND GStatNumber > ?
            """, (max_gstat,))
        
        print("Opponent data linked successfully")
        
        unchanged_count = len(df_clean) - new_count - changed_count
        
        print(f"Game Stats: {new_count} new, {changed_count} changed, {unchanged_count} unchanged")
        return new_count, changed_count, unchanged_count
        
    finally:
        import os
        os.remove(temp_file)





def get_existing_players(conn):
    """Get all existing PersonNumbers before sync"""
    cursor = conn.cursor()
    cursor.execute("SELECT PersonNumber FROM People")
    return set(row[0] for row in cursor.fetchall())

def check_for_new_players(conn, existing_players):
    """Check if any new players were added during sync"""
    cursor = conn.cursor()
    cursor.execute("SELECT PersonNumber, FirstName, LastName FROM People")
    current_players = cursor.fetchall()
    
    new_players = []
    for person_num, first, last in current_players:
        if person_num not in existing_players:
            new_players.append({
                'PersonNumber': person_num,
                'FirstName': first,
                'LastName': last
            })
    
    return new_players

def check_orphan_players(conn):
    """Check for PlayerNumbers in stats that don't exist in People table"""
    cursor = conn.cursor()
    
    # Find batting stats with no matching People record
    cursor.execute("""
        SELECT DISTINCT b.PlayerNumber 
        FROM batting_stats b
        LEFT JOIN People p ON b.PlayerNumber = p.PersonNumber
        WHERE p.PersonNumber IS NULL
    """)
    batting_orphans = [row[0] for row in cursor.fetchall()]
    
    # Find pitching stats with no matching People record
    cursor.execute("""
        SELECT DISTINCT ps.PlayerNumber 
        FROM pitching_stats ps
        LEFT JOIN People p ON ps.PlayerNumber = p.PersonNumber
        WHERE p.PersonNumber IS NULL
    """)
    pitching_orphans = [row[0] for row in cursor.fetchall()]
    
    # Combine unique orphans
    all_orphans = list(set(batting_orphans + pitching_orphans))
    return all_orphans

def main():
    print("COMPLETE SOFTBALL STATS SYNC")
    print("=" * 50)
    
    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"softball_stats.db.backup_{timestamp}"
    shutil.copy2("softball_stats.db", backup_path)
    print(f"Backup created: {backup_path}")
    
    # Connect to database
    conn = sqlite3.connect("softball_stats.db")
    
    try:
        # Get existing players BEFORE sync
        existing_players = get_existing_players(conn)
        print(f"Players in database before sync: {len(existing_players)}")
        
        # Sync all tables
        bat_new, bat_changed, bat_unchanged = sync_batting_stats(conn)
        pitch_new, pitch_changed, pitch_unchanged = sync_pitching_stats(conn)
        game_new, game_changed, game_unchanged = sync_game_stats(conn)
        
        conn.commit()
        
        # Check for new players added
        new_players = check_for_new_players(conn, existing_players)
        
        # Final results
        print("\n" + "=" * 50)
        print("COMPLETE SYNC RESULTS")
        print("=" * 50)
        print(f"Total new records: {bat_new + pitch_new + game_new}")
        print(f"Total changed records: {bat_changed + pitch_changed + game_changed}")
        print(f"Total unchanged records: {bat_unchanged + pitch_unchanged + game_unchanged}")
        
        # ALERT: New players added
        if new_players:
            print("\n" + "!" * 50)
            print("!! ALERT: NEW PLAYERS ADDED !!")
            print("!" * 50)
            print(f"Found {len(new_players)} NEW player(s) added to database:")
            for player in new_players:
                print(f"  PersonNumber: {player['PersonNumber']} - {player['FirstName']} {player['LastName']}")
            print("!" * 50)
            print("Please verify these players are correct!")
            print("!" * 50)
        else:
            print("\nNo new players added (all players already existed in database)")
        
        # Check for orphan player records (stats without People entry)
        orphan_players = check_orphan_players(conn)
        if orphan_players:
            print("\n" + "?" * 50)
            print("?? WARNING: ORPHAN PLAYER IDs FOUND ??")
            print("?" * 50)
            print(f"Found {len(orphan_players)} PlayerNumber(s) in stats with no People record:")
            for orphan_id in orphan_players:
                print(f"  PlayerNumber: {orphan_id}")
            print("?" * 50)
            print("These may be data entry errors - please investigate!")
            print("?" * 50)
        
        print("\nALL TABLES SYNCED SUCCESSFULLY!")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()