#!/usr/bin/env python3
"""
Complete Softball Stats Sync - All Tables + Preprocessing + Sub Logic + Aggregation

Preprocessing layer handles:
  1. PID remapping (CSV PIDs → DB PIDs) for mid-season player additions
  2. Pitching sub detection (overrides incorrect Roster flags using actual roster data)
  3. Error reporting for data quality issues
"""

import sqlite3
import pandas as pd
from datetime import datetime
import shutil
import os

# ============================================================
# CONFIGURATION - Update these each season
# ============================================================

# W26 Team Numbers (538-551)
W26_TEAM_NUMBERS = set(range(538, 552))

# Season filter: 'W26' = only process W26 teams, None = process all
SEASON_FILTER = 'W26'

# PID REMAPPING: CSV PersonNumber → DB PersonNumber
# The data entry system diverged from our DB numbering at PID 628.
# This maps CSV PIDs to their correct DB PIDs.
# Special case: PID 630 is "Big Dawgs Subs" in our DB, but the CSV
# uses 630 for Mike Riley when he subs for other teams.
PID_REMAP = {
    631: 628,   # "Hillis Matt" (reversed name) → Matt Hillis
    632: 628,   # "Hillis Matt" (reversed name, duplicate) → Matt Hillis
    633: 631,   # Tom Birchfield (CSV numbering) → DB numbering
    634: 632,   # Brett Baumbach (CSV numbering) → DB numbering
    635: 633,   # Jeff Lipitz (CSV numbering) → DB numbering
    636: 628,   # "Matt Hillis" (yet another CSV PID) → Matt Hillis
    637: 634,   # Alan Humes (CSV numbering) → DB numbering
    638: 635,   # Pete Hache (CSV numbering) → DB numbering
}

# PID 630 special case: In our DB, 630 = "Big Dawgs Subs".
# When the CSV has PID 630 on a non-Big Dawgs team, it's actually
# Mike Riley (DB PID 620) subbing. On Big Dawgs (544), leave as 630.
PID_630_REAL_PLAYER = 620   # Mike Riley
PID_630_HOME_TEAM = 544     # Big Dawgs

# HARDCODED SUB MAPPINGS - Team Number → Team's Subs PID
SUBS_MAPPING_W26 = {
    538: 493,   # Buckeyes Subs
    539: 584,   # Norsemen Subs
    540: 419,   # Wolverines Subs
    541: 554,   # Xtreme Subs
    542: 600,   # Bad News Bears Subs
    543: 560,   # Bearcats Subs
    544: 630,   # Big Dawgs Subs
    545: 580,   # Death Stars Subs
    546: 538,   # Gunslingers Subs
    547: 540,   # Lightning Strikes Subs
    548: 302,   # Rebels Subs
    549: 548,   # Shorebirds Subs
    550: 320,   # Team USA Subs
    551: 415,   # Tigers Subs
}

# Opponent team name → TeamNumber mapping for game_stats
TEAM_MAPPING_W26 = {
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
    'Xtreme': 541,
}


# ============================================================
# PREPROCESSING
# ============================================================

def build_roster_lookup(conn):
    """Build roster lookup from DB: {team_number: set of player PIDs}
    Excludes Subs placeholder entries."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.TeamNumber, r.PersonNumber
        FROM Roster r
        JOIN People p ON r.PersonNumber = p.PersonNumber
        WHERE r.TeamNumber BETWEEN 538 AND 551 AND p.LastName != 'Subs'
    """)
    roster = {}
    for team, pid in cursor.fetchall():
        if team not in roster:
            roster[team] = set()
        roster[team].add(pid)
    return roster


def get_team_name_lookup(conn):
    """Build team number → short name lookup"""
    cursor = conn.cursor()
    cursor.execute("SELECT TeamNumber, LongTeamName FROM Teams WHERE TeamNumber BETWEEN 538 AND 551")
    return {row[0]: row[1].split('(')[0].strip() for row in cursor.fetchall()}


def get_player_name_lookup(conn):
    """Build PID → name lookup"""
    cursor = conn.cursor()
    cursor.execute("SELECT PersonNumber, FirstName, LastName FROM People")
    return {row[0]: f"{row[1]} {row[2]}" for row in cursor.fetchall()}


def remap_pids(df, report_lines):
    """Remap CSV PersonNumbers to DB PersonNumbers.
    Modifies df in place. Logs all remaps to report_lines."""
    remap_count = 0

    for i in range(len(df)):
        pid = df.iloc[i]['PersonNumber']
        team = df.iloc[i]['TeamNumber']

        # Special case: PID 630
        if pid == 630 and team != PID_630_HOME_TEAM:
            df.iloc[i, df.columns.get_loc('PersonNumber')] = PID_630_REAL_PLAYER
            report_lines.append(
                f"  PID REMAP: 630 → {PID_630_REAL_PLAYER} (Mike Riley sub) "
                f"Team {team} Game {df.iloc[i]['GameNumber']}"
            )
            remap_count += 1
            continue

        # Standard remaps
        if pid in PID_REMAP:
            new_pid = PID_REMAP[pid]
            df.iloc[i, df.columns.get_loc('PersonNumber')] = new_pid
            report_lines.append(
                f"  PID REMAP: {pid} → {new_pid} "
                f"Team {team} Game {df.iloc[i]['GameNumber']}"
            )
            remap_count += 1

    if remap_count > 0:
        report_lines.insert(0, f"PID Remaps applied: {remap_count}")
    return df


def fix_pitching_subs(df, roster, report_lines):
    """For pitching stats, check actual roster membership.
    If a pitcher is not on the team's roster, force Roster='Sub'
    regardless of what the CSV says. This catches data entry errors
    where sub pitchers are incorrectly marked as 'Roster'."""
    fix_count = 0

    if 'Roster' not in df.columns:
        return df

    for i in range(len(df)):
        pid = int(df.iloc[i]['PersonNumber'])
        team = int(df.iloc[i]['TeamNumber'])
        roster_flag = df.iloc[i]['Roster']

        # Skip if already marked Sub
        if roster_flag == 'Sub':
            continue

        # Check if player is actually on this team's roster
        team_roster = roster.get(team, set())
        if pid not in team_roster:
            df.iloc[i, df.columns.get_loc('Roster')] = 'Sub'
            report_lines.append(
                f"  PITCHING SUB FIX: PID {pid} marked Roster→Sub "
                f"for Team {team} Game {df.iloc[i]['GameNumber']} "
                f"(not on roster)"
            )
            fix_count += 1

    if fix_count > 0:
        report_lines.insert(0, f"Pitching Sub fixes applied: {fix_count}")
    return df


def validate_data(df, table_name, roster, team_names, player_names, report_lines):
    """Run validation checks and add warnings to report."""
    warnings = []

    if table_name == 'PitchingStats' and 'Roster' in df.columns:
        # Check for multiple rostered pitchers per team/game (after sub fix)
        grouped = df[df['Roster'] == 'Roster'].groupby(['TeamNumber', 'GameNumber'])
        for (team, game), group in grouped:
            # This is fine - some teams have multiple pitchers per game
            pass

        # Check for duplicate entries (same player, same team, same game)
        dupes = df.groupby(['TeamNumber', 'GameNumber', 'PersonNumber']).size()
        dupes = dupes[dupes > 1]
        for (team, game, pid), count in dupes.items():
            name = player_names.get(int(pid), f'PID {pid}')
            tname = team_names.get(int(team), f'Team {team}')
            warnings.append(
                f"  WARNING: Duplicate pitching entry - {name} on {tname} "
                f"Game {game} ({count} entries)"
            )

    if table_name == 'BattingStats':
        # Check for duplicate entries
        dupes = df.groupby(['TeamNumber', 'GameNumber', 'PersonNumber']).size()
        dupes = dupes[dupes > 1]
        for (team, game, pid), count in dupes.items():
            name = player_names.get(int(pid), f'PID {pid}')
            tname = team_names.get(int(team), f'Team {team}')
            warnings.append(
                f"  WARNING: Duplicate batting entry - {name} on {tname} "
                f"Game {game} ({count} entries, will be aggregated)"
            )

    if warnings:
        report_lines.append(f"\n--- {table_name} Validation Warnings ---")
        report_lines.extend(warnings)


def print_preprocess_report(report_lines):
    """Print the preprocessing report."""
    if report_lines:
        print("\n" + "=" * 50)
        print("PREPROCESSING REPORT")
        print("=" * 50)
        for line in report_lines:
            print(line)
        print("=" * 50)
    else:
        print("\nPreprocessing: No issues found")


# ============================================================
# CSV EXTRACTION
# ============================================================

def extract_table(csv_file, table_name):
    """Extract a specific table from the multi-table CSV"""
    with open(csv_file, 'r') as f:
        lines = f.readlines()

    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith(f"Table: {table_name}"):
            start_idx = i + 1
            break

    if start_idx is None:
        print(f"Table {table_name} not found")
        return None

    end_idx = len(lines)
    for i in range(start_idx, len(lines)):
        if lines[i].strip().startswith("Table: "):
            end_idx = i
            break

    temp_file = f"temp_{table_name.lower()}.csv"
    with open(temp_file, 'w') as f:
        f.writelines(lines[start_idx:end_idx])

    return temp_file


# ============================================================
# SUB LOGIC (existing - redirects Sub players to team Subs PID)
# ============================================================

def apply_subs_logic(df):
    """Apply sub player redirections - replaces individual sub PIDs
    with the team's Subs placeholder PID."""
    sub_count = 0
    if 'Roster' in df.columns:
        for i in range(len(df)):
            if df.iloc[i]['Roster'] == 'Sub':
                team_num = df.iloc[i]['TeamNumber']
                if team_num in SUBS_MAPPING_W26:
                    old_player = df.iloc[i]['PersonNumber']
                    new_player = SUBS_MAPPING_W26[team_num]
                    df.iloc[i, df.columns.get_loc('PersonNumber')] = new_player
                    sub_count += 1
    if sub_count > 0:
        print(f"  Redirected {sub_count} sub records to team Subs PIDs")
    return df


# ============================================================
# SYNC FUNCTIONS
# ============================================================

def sync_batting_stats(conn, roster, team_names, player_names):
    """Sync batting stats with preprocessing + sub aggregation"""
    print("\n--- SYNCING BATTING STATS ---")

    temp_file = extract_table("data.csv", "BattingStats")
    if not temp_file:
        return 0, 0, 0

    try:
        df = pd.read_csv(temp_file)
        print(f"Loaded {len(df)} batting records from CSV")

        # Filter to W26 only
        if SEASON_FILTER == 'W26' and 'TeamNumber' in df.columns:
            before_count = len(df)
            df = df[df['TeamNumber'].isin(W26_TEAM_NUMBERS)]
            filtered_count = before_count - len(df)
            if filtered_count > 0:
                print(f"Filtered out {filtered_count} non-W26 records, keeping {len(df)} W26 records")

        # PREPROCESSING: Remap PIDs
        report = []
        df = remap_pids(df, report)

        # PREPROCESSING: Validate
        validate_data(df, 'BattingStats', roster, team_names, player_names, report)

        if report:
            print("  Batting preprocessing:")
            for line in report:
                print(f"    {line}")

        # Apply sub logic (redirect Sub entries to team Subs PID)
        df = apply_subs_logic(df)

        # Column fixes
        df = df.rename(columns={'PersonNumber': 'PlayerNumber', 'D': '2B', 'T': '3B'})
        df['G'] = 1

        # Keep only needed columns
        cols = ['TeamNumber', 'GameNumber', 'PlayerNumber', 'HomeTeam', 'PA', 'R', 'H',
                '2B', '3B', 'HR', 'OE', 'BB', 'RBI', 'SF', 'G']
        available_cols = [col for col in cols if col in df.columns]
        df_clean = df[available_cols]

        print(f"  Before aggregation: {len(df_clean)} records")

        # Aggregate sub stats
        numeric_cols_to_sum = ['PA', 'R', 'H', '2B', '3B', 'HR', 'OE', 'BB', 'RBI', 'SF']
        available_numeric_to_sum = [col for col in numeric_cols_to_sum if col in df_clean.columns]

        df_aggregated = df_clean.groupby(['TeamNumber', 'GameNumber', 'PlayerNumber']).agg({
            'HomeTeam': 'first',
            **{col: 'sum' for col in available_numeric_to_sum},
            'G': lambda x: 1
        }).reset_index()

        print(f"  After aggregation: {len(df_aggregated)} unique player/game records")

        # Sync with database
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS temp_staging_batting")
        df_aggregated.to_sql("temp_staging_batting", conn, index=False)

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

        if new_count > 0:
            cursor.execute("""
            INSERT INTO batting_stats (TeamNumber, GameNumber, PlayerNumber, HomeTeam, PA, R, H,
                                       [2B], [3B], HR, OE, BB, RBI, SF, G)
            SELECT TeamNumber, GameNumber, PlayerNumber, HomeTeam, PA, R, H,
                   [2B], [3B], HR, OE, BB, RBI, SF, G
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

        print(f"  Batting: {new_count} new, {changed_count} changed, {unchanged_count} unchanged")
        return new_count, changed_count, unchanged_count

    finally:
        os.remove(temp_file)


def sync_pitching_stats(conn, roster, team_names, player_names):
    """Sync pitching stats with preprocessing + sub aggregation"""
    print("\n--- SYNCING PITCHING STATS ---")

    temp_file = extract_table("data.csv", "PitchingStats")
    if not temp_file:
        return 0, 0, 0

    try:
        df = pd.read_csv(temp_file)
        print(f"Loaded {len(df)} pitching records from CSV")

        # Filter to W26 only
        if SEASON_FILTER == 'W26' and 'TeamNumber' in df.columns:
            before_count = len(df)
            df = df[df['TeamNumber'].isin(W26_TEAM_NUMBERS)]
            filtered_count = before_count - len(df)
            if filtered_count > 0:
                print(f"Filtered out {filtered_count} non-W26 records, keeping {len(df)} W26 records")

        # PREPROCESSING: Remap PIDs
        report = []
        df = remap_pids(df, report)

        # PREPROCESSING: Fix pitching sub flags using actual roster data
        fix_pitching_subs(df, roster, report)

        # PREPROCESSING: Validate
        validate_data(df, 'PitchingStats', roster, team_names, player_names, report)

        if report:
            print("  Pitching preprocessing:")
            for line in report:
                print(f"    {line}")

        # Apply sub logic (redirect Sub entries to team Subs PID)
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

        # Aggregate pitching stats
        numeric_cols_to_sum = ['IP', 'BB', 'W', 'L', 'IBB']
        available_numeric_to_sum = [col for col in numeric_cols_to_sum if col in df_clean.columns]

        df_aggregated = df_clean.groupby(['TeamNumber', 'GameNumber', 'PlayerNumber']).agg({
            'HomeTeam': 'first',
            **{col: 'sum' for col in available_numeric_to_sum}
        }).reset_index()

        print(f"  Pitching aggregated from {len(df_clean)} to {len(df_aggregated)} records")

        # Sync with database
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS temp_staging_pitching")
        df_aggregated.to_sql("temp_staging_pitching", conn, index=False)

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

        print(f"  Pitching: {new_count} new, {changed_count} changed, {unchanged_count} unchanged")
        return new_count, changed_count, unchanged_count

    finally:
        os.remove(temp_file)


def sync_game_stats(conn):
    """Sync game stats with missing fields populated"""
    print("\n--- SYNCING GAME STATS ---")

    temp_file = extract_table("data.csv", "GameStats")
    if not temp_file:
        return 0, 0, 0

    try:
        df = pd.read_csv(temp_file)
        print(f"Loaded {len(df)} game records from CSV")

        # Filter to W26 only
        if SEASON_FILTER == 'W26' and 'TeamNumber' in df.columns:
            before_count = len(df)
            df = df[df['TeamNumber'].isin(W26_TEAM_NUMBERS)]
            filtered_count = before_count - len(df)
            if filtered_count > 0:
                print(f"Filtered out {filtered_count} non-W26 records, keeping {len(df)} W26 records")

        # Map CSV columns to database columns
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
                    date_part = str(date_str).split()[0]
                    month, day, year = date_part.split('/')
                    return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                except:
                    return date_str

            df['Date'] = df['Date'].apply(fix_date_format)
            print(f"  Sample converted dates: {df['Date'].head(3).tolist()}")

        # Add OpponentTeamNumber
        if 'Opponent' in df.columns:
            df['OpponentTeamNumber'] = df['Opponent'].map(TEAM_MAPPING_W26)
            unmapped = df[df['OpponentTeamNumber'].isna()]['Opponent'].unique()
            if len(unmapped) > 0:
                print(f"  WARNING: Unmapped opponents: {unmapped}")

        # Keep only the columns we need
        base_cols = ['TeamNumber', 'GameNumber', 'Date', 'Innings', 'HomeTeam',
                     'Opponent', 'OpponentTeamNumber', 'Runs', 'OppRuns']
        inning_cols = ['RunsInning1', 'RunsInning2', 'RunsInning3', 'RunsInning4',
                       'RunsInning5', 'RunsInning6', 'RunsInning7', 'RunsInning8',
                       'RunsInning9']

        all_possible_cols = base_cols + inning_cols
        available_cols = [col for col in all_possible_cols if col in df.columns]
        df_clean = df[available_cols]

        if df_clean.empty:
            print("No valid game data found")
            return 0, 0, 0

        # Get current max GStatNumber
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(MAX(GStatNumber), 0) FROM game_stats")
        max_gstat = cursor.fetchone()[0]

        # Add sequential GStatNumbers
        df_clean = df_clean.copy()
        df_clean['GStatNumber'] = range(max_gstat + 1, max_gstat + 1 + len(df_clean))
        available_cols = ['GStatNumber'] + available_cols

        # Add missing columns to database if needed
        cursor.execute("PRAGMA table_info(game_stats)")
        existing_columns = [row[1] for row in cursor.fetchall()]

        needed_columns = [
            ('GStatNumber', 'INTEGER'),
            ('OpponentTeamNumber', 'INTEGER'),
            ('OpponentGStatNumber', 'INTEGER'),
        ] + [(f'OppRunsInning{i}', 'INTEGER DEFAULT 0') for i in range(1, 10)]

        for col_name, col_def in needed_columns:
            if col_name not in existing_columns:
                print(f"  Adding missing column: {col_name}")
                cursor.execute(f"ALTER TABLE game_stats ADD COLUMN {col_name} {col_def}")

        # Sync with database
        cursor.execute("DROP TABLE IF EXISTS temp_staging_game")
        df_clean.to_sql("temp_staging_game", conn, index=False)

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

        if changed_count > 0:
            set_clauses = [f"{col} = s.{col}" for col in available_cols
                           if col not in ['TeamNumber', 'GameNumber']]
            cursor.execute(f"""
            UPDATE game_stats
            SET {', '.join(set_clauses)}
            FROM temp_staging_game s
            WHERE game_stats.TeamNumber = s.TeamNumber
            AND game_stats.GameNumber = s.GameNumber
            """)

        cursor.execute("DROP TABLE temp_staging_game")

        # Link opponent data
        print("  Linking opponent data...")
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

        print("  Opponent data linked successfully")

        unchanged_count = len(df_clean) - new_count - changed_count

        print(f"  Game Stats: {new_count} new, {changed_count} changed, {unchanged_count} unchanged")
        return new_count, changed_count, unchanged_count

    finally:
        os.remove(temp_file)


# ============================================================
# POST-SYNC VALIDATION
# ============================================================

def post_sync_validation(conn):
    """Run validation checks after sync to catch any remaining issues."""
    print("\n--- POST-SYNC VALIDATION ---")
    issues = []

    cursor = conn.cursor()

    # Orphan PIDs in batting
    cursor.execute("""
        SELECT DISTINCT b.PlayerNumber
        FROM batting_stats b
        LEFT JOIN People p ON b.PlayerNumber = p.PersonNumber
        WHERE b.TeamNumber BETWEEN 538 AND 551 AND p.PersonNumber IS NULL
    """)
    orphans = [row[0] for row in cursor.fetchall()]
    if orphans:
        issues.append(f"ORPHAN PIDs in batting (no People record): {orphans}")

    # Orphan PIDs in pitching
    cursor.execute("""
        SELECT DISTINCT ps.PlayerNumber
        FROM pitching_stats ps
        LEFT JOIN People p ON ps.PlayerNumber = p.PersonNumber
        WHERE ps.TeamNumber BETWEEN 538 AND 551 AND p.PersonNumber IS NULL
    """)
    orphans = [row[0] for row in cursor.fetchall()]
    if orphans:
        issues.append(f"ORPHAN PIDs in pitching (no People record): {orphans}")

    # Multiple wins same team/game
    cursor.execute("""
        SELECT TeamNumber, GameNumber, COUNT(*)
        FROM pitching_stats
        WHERE TeamNumber BETWEEN 538 AND 551 AND W = 1
        GROUP BY TeamNumber, GameNumber HAVING COUNT(*) > 1
    """)
    dupes = cursor.fetchall()
    if dupes:
        for team, game, count in dupes:
            issues.append(f"MULTIPLE WINS: Team {team} Game {game} ({count} pitchers with W)")

    # Multiple losses same team/game
    cursor.execute("""
        SELECT TeamNumber, GameNumber, COUNT(*)
        FROM pitching_stats
        WHERE TeamNumber BETWEEN 538 AND 551 AND L = 1
        GROUP BY TeamNumber, GameNumber HAVING COUNT(*) > 1
    """)
    dupes = cursor.fetchall()
    if dupes:
        for team, game, count in dupes:
            issues.append(f"MULTIPLE LOSSES: Team {team} Game {game} ({count} pitchers with L)")

    # IP vs innings mismatch
    cursor.execute("""
        SELECT ps.TeamNumber, ps.GameNumber, SUM(ps.IP), gs.Innings
        FROM pitching_stats ps
        JOIN game_stats gs ON ps.TeamNumber = gs.TeamNumber AND ps.GameNumber = gs.GameNumber
        WHERE ps.TeamNumber BETWEEN 538 AND 551
        GROUP BY ps.TeamNumber, ps.GameNumber
        HAVING ABS(SUM(ps.IP) - gs.Innings) > 1.5
    """)
    mismatches = cursor.fetchall()
    if mismatches:
        for team, game, total_ip, innings in mismatches:
            issues.append(f"IP MISMATCH: Team {team} Game {game}: Total IP={total_ip}, Innings={innings}")

    # Duplicate batting entries (same player/team/game)
    cursor.execute("""
        SELECT PlayerNumber, TeamNumber, GameNumber, COUNT(*)
        FROM batting_stats
        WHERE TeamNumber BETWEEN 538 AND 551
        GROUP BY PlayerNumber, TeamNumber, GameNumber
        HAVING COUNT(*) > 1
    """)
    dupes = cursor.fetchall()
    if dupes:
        for pid, team, game, count in dupes:
            issues.append(f"DUPLICATE BATTING: PID {pid} Team {team} Game {game} ({count} rows)")

    if issues:
        print("  !! ISSUES FOUND !!")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("  All validation checks passed ✓")

    return issues


# ============================================================
# MAIN
# ============================================================

def main():
    print("COMPLETE SOFTBALL STATS SYNC")
    print("=" * 50)

    # Create backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"softball_stats.db.backup_{timestamp}"
    shutil.copy2("softball_stats.db", backup_path)
    print(f"Backup created: {backup_path}")

    conn = sqlite3.connect("softball_stats.db")

    try:
        # Build lookup tables from DB
        roster = build_roster_lookup(conn)
        team_names = get_team_name_lookup(conn)
        player_names = get_player_name_lookup(conn)
        print(f"Loaded roster data for {len(roster)} teams")

        # Sync all tables
        bat_new, bat_changed, bat_unchanged = sync_batting_stats(conn, roster, team_names, player_names)
        pitch_new, pitch_changed, pitch_unchanged = sync_pitching_stats(conn, roster, team_names, player_names)
        game_new, game_changed, game_unchanged = sync_game_stats(conn)

        conn.commit()

        # Post-sync validation
        issues = post_sync_validation(conn)

        # Final results
        print("\n" + "=" * 50)
        print("SYNC RESULTS")
        print("=" * 50)
        print(f"  New records:       {bat_new + pitch_new + game_new}")
        print(f"  Changed records:   {bat_changed + pitch_changed + game_changed}")
        print(f"  Unchanged records: {bat_unchanged + pitch_unchanged + game_unchanged}")

        if issues:
            print(f"\n  !! {len(issues)} validation issue(s) found - review above !!")
        else:
            print(f"\n  All clean ✓")

        print("\nSYNC COMPLETE")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
