#!/usr/bin/env python3
print("*** RUNNING VERSION 28 - VOLUNTEER-ONLY FIX ***")
"""
D1 Softball Registration Processor
Transforms ugly Zoho CSV export into organized Excel workbook with player matching

Version 28 Changes (CRITICAL FIX - NON-PLAYER VOLUNTEERS):
- FIXED: Non-player volunteers (VolunteerOnly field) now excluded from:
  * Full-Time Players sheet
  * New Players sheet
  * SUB-ONLY Players sheet
  * PDF registration list
- Non-player volunteers still appear correctly on Non-Player Volunteers sheet
- Non-player volunteers still appear correctly on volunteer role sheets (Managers, Umpires, Scorekeepers)

Version 27 Changes (PERSISTENT DECISIONS FILE):
- NEW: fuzzy_decisions.csv - persistent file that accumulates ALL decisions over time
- NEW: manual_matches.csv - manual match overrides (highest priority)
- All sheets sorted alphabetically by LastName (except Raw Cleaned)
- Detects and removes duplicate registrations (keeps newest by Added Time)
- Fuzzy Match decisions now TRULY persist across runs:
  * YES = Auto-apply match (won't show again)
  * NO = Reject match, treat as new player (won't show again)
  * BLANK = Keep the match (won't show again)
- Decisions saved to fuzzy_decisions.csv so they persist even when no Fuzzy Matches sheet exists
"""

import pandas as pd
import sqlite3
from fuzzywuzzy import fuzz
from datetime import datetime
import re
from fpdf import FPDF

# ===== CONFIGURATION =====
ZOHO_CSV_PATH = "zoho.csv"  # Input file
OUTPUT_EXCEL_PATH = "w26reg.xlsx"  # Output file
DATABASE_PATH = "softball_stats.db"
FUZZY_MATCH_THRESHOLD = 75  # Lowered from 85 to catch more variations

# ===== COLUMN MAPPING =====
# Map Zoho column names to clean, standardized names
COLUMN_MAPPING = {
    'Name': 'FullName',
    'Email': 'Email',
    'Phone': 'Phone',
    'Villages Address': 'Address',
    'Village': 'Village',
    'Villages ID': 'VillagesID',
    'Date of Birth': 'DOB',
    'Age at Start of Season': 'Age',
    'Preferred Position(s)': 'Position1',
    '2nd Preferred Position(s)': 'Position2',
    'Do you need a runner?': 'NeedsRunner',
    'Emergency Contact (ICE)': 'EmergencyName',
    'Emergency Contact (ICE) Phone': 'EmergencyPhone',
    'Player availability to include dates missed for travel tournaments, vacations, etc., known injuries, any limitations, etc. (BE SPECIFIC)': 'Availability',
    'In which season did you last play?': 'LastSeason',
    'In what division did you last play?': 'LastDivision',
    'Approximate date you were evaluated': 'EvalDate',
    'In what division were you evaluated?': 'EvalDivision',
    'I want to be SUB-ONLY': 'SubOnly',
    'Will you be in The Villages for the start of the season?': 'AvailableStart',
    'If not, when will you be back?': 'ReturnDate',
    'Volunteer Only (Manager, Umpire, Scorekeeper, Announcer)': 'VolunteerOnly',
    'I wish to volunteer as a(n):': 'PlayerVolunteer',
    'Please select the option you prefer if you go undrafted.': 'UndraftedPreference'
}

def load_manual_overrides(manual_csv_path="manual_matches.csv"):
    """Load manual match overrides from CSV file"""
    manual_matches = {}
    try:
        df = pd.read_csv(manual_csv_path)
        for idx, row in df.iterrows():
            key = f"{row['CSVFirstName']}|{row['CSVLastName']}".lower()
            manual_matches[key] = int(row['PersonNumber'])
            note = row.get('Notes', '')
            print(f"  Manual override: {row['CSVFirstName']} {row['CSVLastName']} -> PersonNumber {row['PersonNumber']}" + (f" ({note})" if note else ""))
        print(f"  Loaded {len(manual_matches)} manual match overrides")
    except FileNotFoundError:
        print(f"  No manual_matches.csv found (create one to override fuzzy matching)")
    except Exception as e:
        print(f"  Error loading manual matches: {e}")
    return manual_matches

def load_excluded_players(exclusion_csv_path="excluded_players.csv"):
    """Load list of players to exclude from draft"""
    excluded = {}
    try:
        df = pd.read_csv(exclusion_csv_path)
        for idx, row in df.iterrows():
            person_num = int(row['PersonNumber'])
            reason = row.get('Reason', 'Excluded')
            excluded[person_num] = reason
            print(f"  Excluded: PersonNumber {person_num} - {reason}")
        print(f"  Loaded {len(excluded)} excluded players")
    except FileNotFoundError:
        print(f"  No excluded_players.csv found (none excluded)")
    except Exception as e:
        print(f"  Error loading excluded players: {e}")
    return excluded

def load_persistent_decisions(csv_path="fuzzy_decisions.csv"):
    """Load persistent fuzzy match decisions from CSV file"""
    confirmed = {}
    rejected = set()
    previously_seen = {}
    
    try:
        df = pd.read_csv(csv_path)
        for idx, row in df.iterrows():
            key = f"{row['CSVFirstName']}|{row['CSVLastName']}".lower()
            decision = str(row['Decision']).strip().upper()
            
            if decision in ['YES', 'Y', '1', 'TRUE', 'CONFIRMED']:
                confirmed[key] = int(row['PersonNumber'])
                print(f"  Persistent YES: {row['CSVFirstName']} {row['CSVLastName']} -> PersonNumber {row['PersonNumber']}")
            elif decision in ['NO', 'N', '0', 'FALSE', 'REJECTED']:
                rejected.add(key)
                print(f"  Persistent NO: {row['CSVFirstName']} {row['CSVLastName']}")
            elif decision == 'SEEN':
                previously_seen[key] = int(row['PersonNumber'])
                print(f"  Persistent SEEN: {row['CSVFirstName']} {row['CSVLastName']} -> PersonNumber {row['PersonNumber']}")
        
        print(f"  Loaded {len(confirmed)} confirmed + {len(rejected)} rejected + {len(previously_seen)} seen from persistent file")
    except FileNotFoundError:
        print(f"  No persistent decisions file found (will create on first run)")
    except Exception as e:
        print(f"  Error loading persistent decisions: {e}")
    
    return confirmed, rejected, previously_seen

def save_persistent_decisions(confirmed, rejected, previously_seen, csv_path="fuzzy_decisions.csv"):
    """Save all fuzzy match decisions to persistent CSV file"""
    records = []
    
    # Add confirmed matches
    for key, person_num in confirmed.items():
        parts = key.split('|')
        records.append({
            'CSVFirstName': parts[0],
            'CSVLastName': parts[1],
            'PersonNumber': person_num,
            'Decision': 'CONFIRMED',
            'DateDecided': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # Add rejected matches
    for key in rejected:
        parts = key.split('|')
        records.append({
            'CSVFirstName': parts[0],
            'CSVLastName': parts[1],
            'PersonNumber': '',
            'Decision': 'REJECTED',
            'DateDecided': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # Add previously seen matches
    for key, person_num in previously_seen.items():
        parts = key.split('|')
        records.append({
            'CSVFirstName': parts[0],
            'CSVLastName': parts[1],
            'PersonNumber': person_num,
            'Decision': 'SEEN',
            'DateDecided': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    if records:
        df = pd.DataFrame(records)
        df.to_csv(csv_path, index=False)
        print(f"\n  Saved {len(records)} total decisions to {csv_path}")
    else:
        print(f"\n  No decisions to save")

def load_confirmed_matches(excel_path):
    """Load fuzzy match decisions from Excel file (for this run only)"""
    confirmed = {}
    rejected = set()
    previously_seen = {}
    
    try:
        # Try to read Fuzzy Matches sheet from current Excel file
        df = pd.read_excel(excel_path, sheet_name='Fuzzy Matches')
        print(f"  DEBUG: Found Fuzzy Matches sheet with {len(df)} rows")
        if 'Confirmed' in df.columns:
            # Accept multiple confirmation formats: YES, Y, 1, True (case insensitive)
            def is_confirmed(val):
                if pd.isna(val):
                    return False
                val_str = str(val).strip().upper()
                return val_str in ['YES', 'Y', '1', 'TRUE', '1.0']
            
            # Accept multiple rejection formats: NO, N, 0, False (case insensitive)
            def is_rejected(val):
                if pd.isna(val):
                    return False
                val_str = str(val).strip().upper()
                return val_str in ['NO', 'N', '0', 'FALSE', '0.0']
            
            # Load confirmed matches (marked YES)
            confirmed_df = df[df['Confirmed'].apply(is_confirmed)]
            for idx, row in confirmed_df.iterrows():
                key = f"{row['FirstName']}|{row['LastName']}".lower()
                confirmed[key] = int(row['PersonNumber'])
                print(f"  Confirmed YES: {row['FirstName']} {row['LastName']} (key: '{key}') -> PersonNumber {row['PersonNumber']}")
            
            # Load rejected matches (marked NO)
            rejected_df = df[df['Confirmed'].apply(is_rejected)]
            for idx, row in rejected_df.iterrows():
                key = f"{row['FirstName']}|{row['LastName']}".lower()
                rejected.add(key)
                print(f"  Rejected NO: {row['FirstName']} {row['LastName']} (key: '{key}') (will treat as new player)")
            
            # Load previously seen but unconfirmed (BLANK entries) - keep the fuzzy match
            blank_df = df[~df['Confirmed'].apply(is_confirmed) & ~df['Confirmed'].apply(is_rejected)]
            for idx, row in blank_df.iterrows():
                key = f"{row['FirstName']}|{row['LastName']}".lower()
                previously_seen[key] = int(row['PersonNumber'])
                print(f"  Previously seen (blank): {row['FirstName']} {row['LastName']} (key: '{key}') -> PersonNumber {row['PersonNumber']} (will keep match)")
            
            print(f"  Loaded {len(confirmed)} confirmed matches (will auto-apply)")
            print(f"  Loaded {len(rejected)} rejected matches (will treat as new)")
            print(f"  Loaded {len(previously_seen)} previously seen matches (will keep fuzzy match)")
        else:
            print(f"  WARNING: Confirmed column not found in Fuzzy Matches sheet")
    except Exception as e:
        print(f"  No previous matches found (this is normal for first run): {e}")
    return confirmed, rejected, previously_seen

def parse_name(full_name):
    """Parse 'FirstName, LastName' format from Zoho CSV"""
    if pd.isna(full_name) or not full_name:
        return None, None
    
    # Handle "FirstName, LastName" format (NOT LastName, FirstName!)
    if ',' in full_name:
        parts = full_name.split(',', 1)
        # IMPORTANT: Before comma is FIRST name, after comma is LAST name
        first_name = parts[0].strip()  # Before comma
        last_name = parts[1].strip()   # After comma
    else:
        # Fallback: assume "FirstName LastName" if no comma
        parts = full_name.strip().split()
        if len(parts) >= 2:
            first_name = parts[0]
            last_name = ' '.join(parts[1:])
        else:
            first_name = parts[0] if parts else ''
            last_name = ''
    
    return first_name, last_name

def remove_duplicates(df):
    """Remove duplicate registrations, keeping the most recent one"""
    print("\nChecking for duplicate registrations...")
    
    # Parse names first to check for duplicates
    df[['FirstName', 'LastName']] = df['FullName'].apply(
        lambda x: pd.Series(parse_name(x))
    )
    
    # Check if Added Time column exists (from Zoho CSV)
    time_column = None
    for col in df.columns:
        if 'added time' in col.lower() or 'time' in col.lower():
            time_column = col
            break
    
    initial_count = len(df)
    
    if time_column and time_column in df.columns:
        # Convert Added Time to datetime for proper sorting
        df[time_column] = pd.to_datetime(df[time_column], errors='coerce')
        
        # Sort by Added Time (newest first) so we keep the most recent
        df = df.sort_values(time_column, ascending=False)
    else:
        print("  WARNING: No timestamp column found, keeping last occurrence in file")
    
    # Create a key for duplicate detection (case-insensitive name matching)
    df['_DuplicateKey'] = df['FirstName'].str.lower() + '|' + df['LastName'].str.lower()
    
    # Identify duplicates
    duplicates = df[df.duplicated(subset=['_DuplicateKey'], keep='first')]
    
    if len(duplicates) > 0:
        print(f"  Found {len(duplicates)} duplicate registration(s):")
        for idx, row in duplicates.iterrows():
            time_str = row[time_column].strftime('%Y-%m-%d %H:%M:%S') if time_column and pd.notna(row[time_column]) else 'Unknown time'
            print(f"    - {row['FirstName']} {row['LastName']} (registered: {time_str}) - REMOVING")
        
        # Keep only first occurrence (which is newest due to sorting)
        df = df.drop_duplicates(subset=['_DuplicateKey'], keep='first')
        
        # Drop the temporary duplicate key column
        df = df.drop(columns=['_DuplicateKey'])
        
        final_count = len(df)
        print(f"  Removed {initial_count - final_count} duplicate(s), keeping {final_count} unique registrations")
    else:
        print(f"  No duplicates found - all {initial_count} registrations are unique")
        df = df.drop(columns=['_DuplicateKey'])
    
    # Reset index after removing duplicates
    df = df.reset_index(drop=True)
    
    return df

def load_database_players(db_path):
    """Load existing players from database"""
    conn = sqlite3.connect(db_path)
    query = "SELECT PersonNumber, FirstName, LastName FROM People WHERE LastName != 'Subs'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    print(f"Loaded {len(df)} existing players from database")
    return df

def exact_match(first_name, last_name, db_players):
    """Find exact name match in database"""
    matches = db_players[
        (db_players['FirstName'].str.lower() == first_name.lower()) &
        (db_players['LastName'].str.lower() == last_name.lower())
    ]
    if len(matches) > 0:
        return matches.iloc[0]['PersonNumber'], 'Exact', 100
    return None, None, 0

def fuzzy_match(first_name, last_name, db_players, threshold=75):
    """Find fuzzy name matches in database"""
    best_match = None
    best_score = 0
    best_db_first = None
    best_db_last = None
    
    full_name = f"{first_name} {last_name}".lower()
    
    for idx, row in db_players.iterrows():
        db_full_name = f"{row['FirstName']} {row['LastName']}".lower()
        
        # Calculate similarity score
        score = fuzz.ratio(full_name, db_full_name)
        
        if score > best_score and score >= threshold:
            best_score = score
            best_match = row['PersonNumber']
            best_db_first = row['FirstName']
            best_db_last = row['LastName']
    
    if best_match:
        return best_match, best_db_first, best_db_last, 'Fuzzy', best_score
    return None, None, None, None, 0

def process_registrations(csv_path, db_path):
    """Main processing function"""
    print("=" * 60)
    print("D1 SOFTBALL REGISTRATION PROCESSOR")
    print("=" * 60)
    
    # Load Zoho CSV
    print(f"\nLoading Zoho export: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} registrations")
    
    # Rename columns to clean names
    df = df.rename(columns=COLUMN_MAPPING)
    
    # Remove duplicates (keeping most recent), parse names in the process
    df = remove_duplicates(df)
    
    # DEBUG: Show first 5 parsed names
    print("\n*** DEBUG: First 5 parsed names from Zoho CSV:")
    for idx in range(min(5, len(df))):
        print(f"  CSV: '{df.iloc[idx]['FullName']}' -> FirstName: '{df.iloc[idx]['FirstName']}', LastName: '{df.iloc[idx]['LastName']}'")
    
    # Load database players
    db_players = load_database_players(db_path)
    
    # Load manual overrides (highest priority)
    print("\nLoading manual match overrides...")
    manual_matches = load_manual_overrides()
    
    # Load excluded players (do not draft list)
    print("\nLoading excluded players list...")
    excluded_players = load_excluded_players()
    
    # Load persistent decisions (accumulates over time)
    print("\nLoading persistent fuzzy match decisions...")
    confirmed_matches, rejected_matches, previously_seen_matches = load_persistent_decisions()
    
    # Also load from current Excel file (in case user just marked YES/NO)
    print("\nLoading decisions from current Excel file...")
    excel_confirmed, excel_rejected, excel_seen = load_confirmed_matches(OUTPUT_EXCEL_PATH)
    
    # Merge Excel decisions into persistent decisions (Excel takes priority for this run)
    confirmed_matches.update(excel_confirmed)
    rejected_matches.update(excel_rejected)
    previously_seen_matches.update(excel_seen)
    
    # DEBUG: Show first 5 database names
    print("\n*** DEBUG: First 5 names from database:")
    for idx in range(min(5, len(db_players))):
        print(f"  DB: FirstName: '{db_players.iloc[idx]['FirstName']}', LastName: '{db_players.iloc[idx]['LastName']}'")
    
    print("\n*** DEBUG: Checking if 'Jeff Lyons' would match:")
    test_match = db_players[(db_players['FirstName'] == 'Jeff') & (db_players['LastName'] == 'Lyons')]
    if len(test_match) > 0:
        print(f"  Found in database: PersonNumber={test_match.iloc[0]['PersonNumber']}")
    else:
        print(f"  NOT found in database")
    
    # Match players
    print("\nMatching players against database...")
    match_results = []
    
    for idx, row in df.iterrows():
        first_name = row['FirstName']
        last_name = row['LastName']
        
        if pd.isna(first_name) or pd.isna(last_name):
            match_results.append({
                'PersonNumber': None,
                'DB_FirstName': None,
                'DB_LastName': None,
                'MatchType': 'No Name',
                'MatchScore': 0
            })
            continue
        
        match_key = f"{first_name}|{last_name}".lower()
        
        # DEBUG: Show what we're checking
        if idx < 5 or "reed" in match_key:  # Show first 5 or anyone named Reed
            print(f"  DEBUG: Checking player '{first_name} {last_name}' with key '{match_key}'")
            print(f"    In manual? {match_key in manual_matches}")
            print(f"    In confirmed? {match_key in confirmed_matches}")
            print(f"    In rejected? {match_key in rejected_matches}")
            print(f"    In previously seen? {match_key in previously_seen_matches}")
        
        # Check if this was rejected before (false positive fuzzy match)
        if match_key in rejected_matches:
            # Treat as new player - don't try fuzzy matching again
            match_results.append({
                'PersonNumber': None,
                'DB_FirstName': None,
                'DB_LastName': None,
                'MatchType': 'New Player',
                'MatchScore': 0
            })
            continue
        
        # Check manual overrides next (highest priority after rejections)
        if match_key in manual_matches:
            person_num = manual_matches[match_key]
            # Get DB names for this person
            db_match = db_players[db_players['PersonNumber'] == person_num]
            if len(db_match) > 0:
                match_results.append({
                    'PersonNumber': person_num,
                    'DB_FirstName': db_match.iloc[0]['FirstName'],
                    'DB_LastName': db_match.iloc[0]['LastName'],
                    'MatchType': 'Manual',
                    'MatchScore': 100
                })
                continue
        
        # Check confirmed matches next
        if match_key in confirmed_matches:
            person_num = confirmed_matches[match_key]
            # Get DB names for this person
            db_match = db_players[db_players['PersonNumber'] == person_num]
            if len(db_match) > 0:
                match_results.append({
                    'PersonNumber': person_num,
                    'DB_FirstName': db_match.iloc[0]['FirstName'],
                    'DB_LastName': db_match.iloc[0]['LastName'],
                    'MatchType': 'Confirmed',
                    'MatchScore': 100
                })
                continue
        
        # Check previously seen matches (blank entries - keep the fuzzy match)
        if match_key in previously_seen_matches:
            person_num = previously_seen_matches[match_key]
            # Get DB names for this person
            db_match = db_players[db_players['PersonNumber'] == person_num]
            if len(db_match) > 0:
                match_results.append({
                    'PersonNumber': person_num,
                    'DB_FirstName': db_match.iloc[0]['FirstName'],
                    'DB_LastName': db_match.iloc[0]['LastName'],
                    'MatchType': 'PreviouslySeen',
                    'MatchScore': 100
                })
                continue
        
        # Try exact match
        person_num, match_type, score = exact_match(first_name, last_name, db_players)
        db_first = None
        db_last = None
        
        # If no exact match, try fuzzy
        if not person_num:
            person_num, db_first, db_last, match_type, score = fuzzy_match(
                first_name, last_name, db_players, FUZZY_MATCH_THRESHOLD
            )
        else:
            # For exact matches, set DB names same as CSV names
            db_first = first_name
            db_last = last_name
        
        # If still no match, mark as new
        if not person_num:
            match_type = 'New Player'
            score = 0
        
        match_results.append({
            'PersonNumber': person_num,
            'DB_FirstName': db_first,
            'DB_LastName': db_last,
            'MatchType': match_type,
            'MatchScore': score
        })
    
    # Add match results to dataframe
    match_df = pd.DataFrame(match_results)
    df = pd.concat([df, match_df], axis=1)
    
    # CRITICAL: Save PersonNumber for fuzzy matches, then clear it
    # We need it for the Fuzzy Matches review sheet, but nowhere else
    # Fuzzy matches need human review before PersonNumber is assigned
    df['FuzzyPersonNumber'] = df['PersonNumber']  # Save for fuzzy sheet
    df.loc[df['MatchType'] == 'Fuzzy', 'PersonNumber'] = None  # Clear for all other sheets
    
    fuzzy_count = len(df[df['MatchType'] == 'Fuzzy'])
    
    # Print summary
    print("\nMatching Summary:")
    print(f"  Manual matches: {len(df[df['MatchType'] == 'Manual'])}")
    print(f"  Exact matches: {len(df[df['MatchType'] == 'Exact'])}")
    print(f"  Confirmed matches (marked YES): {len(df[df['MatchType'] == 'Confirmed'])}")
    print(f"  Previously seen matches (kept, not shown again): {len(df[df['MatchType'] == 'PreviouslySeen'])}")
    print(f"  Fuzzy matches (NEW - need review): {fuzzy_count}")
    print(f"  New players: {len(df[df['MatchType'] == 'New Player'])}")
    
    # Save all decisions to persistent file
    print("\nSaving decisions to persistent file...")
    save_persistent_decisions(confirmed_matches, rejected_matches, previously_seen_matches)
    
    return df, db_players, excluded_players

def create_excel_output(df, db_players, excluded_players, output_path):
    """Generate multi-worksheet Excel file"""
    print(f"\nCreating Excel workbook: {output_path}")
    
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#667eea',
            'font_color': 'white',
            'border': 1
        })
        
        # ===== WORKSHEET 1: Full Time Players =====
        # Include ALL players who aren't SUB-ONLY (matched AND new players)
        # Managers need complete draft list regardless of PersonNumber
        # EXCLUDE players on the do-not-draft list
        # EXCLUDE non-player volunteers (VolunteerOnly)
        is_sub_only = df['SubOnly'].notna() & (df['SubOnly'].astype(str).str.lower() != 'no')
        is_volunteer_only = df['VolunteerOnly'].notna()
        full_time = df[~is_sub_only & ~is_volunteer_only].copy()
        
        # Filter out excluded players
        excluded_count = 0
        if len(excluded_players) > 0:
            full_time_before = len(full_time)
            full_time = full_time[~full_time['PersonNumber'].isin(excluded_players.keys())].copy()
            excluded_count = full_time_before - len(full_time)
        
        if len(full_time) > 0:
            full_time_output = full_time[[
                'PersonNumber', 'FirstName', 'LastName', 'Email', 'Phone', 
                'Age', 'Position1', 'Position2', 'NeedsRunner', 'Availability'
            ]].copy()
            # Sort alphabetically by LastName
            full_time_output = full_time_output.sort_values('LastName', key=lambda x: x.str.lower())
            full_time_output.to_excel(writer, sheet_name='full_time_players', index=False)
            print(f"  Created 'full_time_players' sheet: {len(full_time)} players" + 
                  (f" ({excluded_count} excluded from draft)" if excluded_count > 0 else ""))
        
        # ===== WORKSHEET 2: Fuzzy Matches =====
        # Show all fuzzy matches that need review
        fuzzy = df[df['MatchType'] == 'Fuzzy'].copy()
        if len(fuzzy) > 0:
            # Use FuzzyPersonNumber (not PersonNumber which was cleared)
            fuzzy_output = fuzzy[[
                'FuzzyPersonNumber', 'FirstName', 'LastName', 'DB_FirstName', 'DB_LastName', 'MatchScore',
                'Email', 'Phone', 'LastSeason', 'LastDivision'
            ]].copy()
            # Rename column for clarity
            fuzzy_output = fuzzy_output.rename(columns={'FuzzyPersonNumber': 'PersonNumber'})
            # Add Confirmed column for user to mark YES or NO
            fuzzy_output['Confirmed'] = ''
            # Sort alphabetically by LastName
            fuzzy_output = fuzzy_output.sort_values('LastName', key=lambda x: x.str.lower())
            fuzzy_output.to_excel(writer, sheet_name='Fuzzy Matches', index=False)
            print(f"  Created 'Fuzzy Matches' sheet: {len(fuzzy)} players (REVIEW NEEDED)")
            print(f"    Mark 'Confirmed' column with 'YES' for correct matches or 'NO' to reject")
        else:
            print(f"  No fuzzy matches to review")
        
        # ===== WORKSHEET 3: New Players =====
        # EXCLUDE non-player volunteers (VolunteerOnly)
        new_players = df[(df['MatchType'] == 'New Player') & ~is_volunteer_only].copy()
        if len(new_players) > 0:
            new_output = new_players[[
                'FirstName', 'LastName', 'Email', 'Phone', 'Age',
                'Position1', 'Position2', 'NeedsRunner',
                'EmergencyName', 'EmergencyPhone', 'Availability',
                'LastSeason', 'LastDivision', 'EvalDate', 'EvalDivision'
            ]].copy()
            # Sort alphabetically by LastName
            new_output = new_output.sort_values('LastName', key=lambda x: x.str.lower())
            new_output.to_excel(writer, sheet_name='New Players', index=False)
            print(f"  Created 'New Players' sheet: {len(new_players)} players")
        
        # ===== WORKSHEET 4: SUB-ONLY Players =====
        # EXCLUDE non-player volunteers (VolunteerOnly)
        subs = df[is_sub_only & ~is_volunteer_only].copy()
        if len(subs) > 0:
            subs_output = subs[[
                'PersonNumber', 'FirstName', 'LastName', 'Email', 'Phone',
                'Availability', 'MatchType'
            ]].copy()
            # Sort alphabetically by LastName
            subs_output = subs_output.sort_values('LastName', key=lambda x: x.str.lower())
            subs_output.to_excel(writer, sheet_name='SUB-ONLY Players', index=False)
            print(f"  Created 'SUB-ONLY Players' sheet: {len(subs)} players")
        
        # ===== WORKSHEET 5: Non-Player Volunteers =====
        volunteers = df[df['VolunteerOnly'].notna()].copy()
        if len(volunteers) > 0:
            vol_output = volunteers[[
                'FirstName', 'LastName', 'Email', 'Phone', 'VolunteerOnly'
            ]].copy()
            # Sort alphabetically by LastName
            vol_output = vol_output.sort_values('LastName', key=lambda x: x.str.lower())
            vol_output.to_excel(writer, sheet_name='Non-Player Volunteers', index=False)
            print(f"  Created 'Non-Player Volunteers' sheet: {len(volunteers)} volunteers")
        
        # ===== WORKSHEET 6: Parse Player Volunteers into separate sheets =====
        # Parse PlayerVolunteer column to extract roles
        # Use DB names if player is matched/confirmed
        managers = []
        umpires = []
        scorekeepers = []
        
        for idx, row in df.iterrows():
            volunteer_str = str(row.get('PlayerVolunteer', ''))
            if pd.notna(volunteer_str) and volunteer_str.upper() != 'NONE':
                # Use DB names if available (Exact or Confirmed match), otherwise CSV names
                if row['MatchType'] in ['Exact', 'Confirmed'] and pd.notna(row.get('DB_FirstName')):
                    first_name = row['DB_FirstName']
                    last_name = row['DB_LastName']
                else:
                    first_name = row['FirstName']
                    last_name = row['LastName']
                
                player_info = {
                    'PersonNumber': row.get('PersonNumber'),
                    'FirstName': first_name,
                    'LastName': last_name,
                    'Email': row['Email'],
                    'Phone': row['Phone']
                }
                
                # Check for each role (case-insensitive)
                if 'manager' in volunteer_str.lower():
                    managers.append(player_info)
                if 'umpire' in volunteer_str.lower():
                    umpires.append(player_info)
                if 'scorekeeper' in volunteer_str.lower() or 'announcer' in volunteer_str.lower():
                    scorekeepers.append(player_info)
        
        # Create Managers sheet
        if managers:
            managers_df = pd.DataFrame(managers)
            # Sort alphabetically by LastName
            managers_df = managers_df.sort_values('LastName', key=lambda x: x.str.lower())
            managers_df.to_excel(writer, sheet_name='Volunteer-Managers', index=False)
            print(f"  Created 'Volunteer-Managers' sheet: {len(managers)} players")
        
        # Create Umpires sheet
        if umpires:
            umpires_df = pd.DataFrame(umpires)
            # Sort alphabetically by LastName
            umpires_df = umpires_df.sort_values('LastName', key=lambda x: x.str.lower())
            umpires_df.to_excel(writer, sheet_name='Volunteer-Umpires', index=False)
            print(f"  Created 'Volunteer-Umpires' sheet: {len(umpires)} players")
        
        # Create Scorekeepers sheet
        if scorekeepers:
            scorekeepers_df = pd.DataFrame(scorekeepers)
            # Sort alphabetically by LastName
            scorekeepers_df = scorekeepers_df.sort_values('LastName', key=lambda x: x.str.lower())
            scorekeepers_df.to_excel(writer, sheet_name='Volunteer-Scorekeepers', index=False)
            print(f"  Created 'Volunteer-Scorekeepers' sheet: {len(scorekeepers)} players")
        
        # ===== WORKSHEET 7: Contact Sheet =====
        contact_output = df[[
            'PersonNumber', 'FirstName', 'LastName', 'Email', 'Phone',
            'EmergencyName', 'EmergencyPhone', 'MatchType'
        ]].copy()
        # Sort alphabetically by LastName
        contact_output = contact_output.sort_values('LastName', key=lambda x: x.str.lower())
        contact_output.to_excel(writer, sheet_name='Contact Sheet', index=False)
        print(f"  Created 'Contact Sheet' sheet: {len(df)} entries")
        
        # ===== WORKSHEET 8: Raw Cleaned (NOT SORTED - left as is) =====
        df.to_excel(writer, sheet_name='Raw Cleaned', index=False)
        print(f"  Created 'Raw Cleaned' sheet: {len(df)} entries (unsorted)")
    
    print(f"\n✓ Excel workbook created successfully!")
    print(f"  Location: {output_path}")

def create_registration_pdf(df, excluded_players, output_path="registrations.pdf"):
    """Create a PDF list of all registered players for website"""
    print(f"\nCreating PDF for website: {output_path}")
    
    # Get full-time and sub-only players
    # EXCLUDE non-player volunteers (VolunteerOnly)
    is_sub_only = df['SubOnly'].notna() & (df['SubOnly'].astype(str).str.lower() != 'no')
    is_volunteer_only = df['VolunteerOnly'].notna()
    full_time = df[~is_sub_only & ~is_volunteer_only].copy()
    sub_only = df[is_sub_only & ~is_volunteer_only].copy()
    
    # Filter out excluded players from full-time
    if len(excluded_players) > 0:
        full_time = full_time[~full_time['PersonNumber'].isin(excluded_players.keys())].copy()
    
    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Column settings
    left_margin = 15
    col_width = 90
    line_height = 5
    
    # Title
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 12, 'D1 Softball Registration List', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 8, f'Generated: {datetime.now().strftime("%B %d, %Y")}', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(3)
    
    def print_two_column_list(sorted_df, title):
        """Helper function to print names in two columns (split alphabetically)"""
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('Helvetica', '', 10)
        
        # Convert to list for easier indexing
        names = [f"{row['FirstName']} {row['LastName']}" for idx, row in sorted_df.iterrows()]
        
        # Calculate how many names fit per column on one page
        y_start = pdf.get_y()
        page_height_limit = 270
        names_per_column = int((page_height_limit - y_start) / line_height)
        names_per_page = names_per_column * 2
        
        # Distribute names to left and right columns to flow naturally across pages
        # Left column gets: indices 0, 2, 4, 6... (every other "slot")
        # Right column gets: indices 1, 3, 5, 7... (every other "slot")  
        # Where each "slot" is names_per_column items
        left_col = []
        right_col = []
        
        idx = 0
        page_num = 0
        while idx < len(names):
            # Fill left column for this page
            chunk_size = min(names_per_column, len(names) - idx)
            left_col.extend(names[idx:idx + chunk_size])
            idx += chunk_size
            
            if idx < len(names):
                # Fill right column for this page
                chunk_size = min(names_per_column, len(names) - idx)
                right_col.extend(names[idx:idx + chunk_size])
                idx += chunk_size
        
        start_page = pdf.page_no()  # Remember which page we started on
        page_height_limit = 270  # Bottom margin threshold
        
        # Print left column
        current_y_left = y_start
        left_end_page = start_page
        names_printed_on_page = 0
        for i, name in enumerate(left_col):
            # Check if we need a new page (after names_per_column names)
            if names_printed_on_page >= names_per_column:
                pdf.add_page()
                left_end_page = pdf.page_no()
                current_y_left = pdf.get_y()
                names_printed_on_page = 0
            
            pdf.set_xy(left_margin, current_y_left)
            pdf.cell(col_width, line_height, name)
            current_y_left += line_height
            names_printed_on_page += 1
        
        # Print right column - start back at the beginning
        current_y_right = y_start
        right_end_page = start_page
        if right_col:
            # Go back to the page where we started
            pdf.page = start_page
            current_y_right = y_start
            names_printed_on_page = 0
            
            for i, name in enumerate(right_col):
                # Check if we need a new page (after names_per_column names)
                if names_printed_on_page >= names_per_column:
                    pdf.add_page()
                    right_end_page = pdf.page_no()
                    current_y_right = pdf.get_y()
                    names_printed_on_page = 0
                
                pdf.set_xy(left_margin + col_width, current_y_right)
                pdf.cell(col_width, line_height, name)
                current_y_right += line_height
                names_printed_on_page += 1
        
        # Position cursor after both columns - go to whichever ends further down
        if left_end_page > right_end_page or (left_end_page == right_end_page and current_y_left > current_y_right):
            # Left column ends further down
            pdf.page = left_end_page
            pdf.set_y(current_y_left + 3)
        else:
            # Right column ends further down (or equal)
            pdf.page = right_end_page
            pdf.set_y(current_y_right + 3)
    
    # Full-Time Players Section
    if len(full_time) > 0:
        full_time_sorted = full_time.sort_values('LastName', key=lambda x: x.str.lower())
        print_two_column_list(full_time_sorted, f'Full-Time Players ({len(full_time)})')
    
    # Sub-Only Players Section
    if len(sub_only) > 0:
        sub_only_sorted = sub_only.sort_values('LastName', key=lambda x: x.str.lower())
        print_two_column_list(sub_only_sorted, f'Sub-Only Players ({len(sub_only)})')
    
    # Save PDF
    pdf.output(output_path)
    print(f"✓ PDF created: {output_path}")
    print(f"  Full-time players: {len(full_time)}")
    print(f"  Sub-only players: {len(sub_only)}")
    print(f"  Total registered: {len(full_time) + len(sub_only)}")

def main():
    """Main execution"""
    try:
        # Process registrations
        df, db_players, excluded_players = process_registrations(ZOHO_CSV_PATH, DATABASE_PATH)
        
        # Create Excel output
        create_excel_output(df, db_players, excluded_players, OUTPUT_EXCEL_PATH)
        
        # Create PDF for website
        create_registration_pdf(df, excluded_players, "registrations.pdf")
        
        print("\n" + "=" * 60)
        print("PROCESSING COMPLETE!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review 'Fuzzy Matches' sheet (only NEW matches shown):")
        print("   - Mark 'Confirmed' column with 'YES' to confirm correct matches")
        print("   - Mark 'Confirmed' column with 'NO' to reject false matches")
        print("   - Leave BLANK to accept the match as-is")
        print("   - Once reviewed, matches won't show again (even if blank)")
        print("2. Next run will auto-apply all previous decisions")
        print("3. Review 'New Players' sheet - assign PersonNumbers in database")
        print("4. Review volunteer sheets for role assignments")
        print("5. 'full_time_players' sheet is ready for draft managers")
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: File not found - {e}")
        print("Make sure these files exist:")
        print(f"  - zoho.csv (Zoho export)")
        print(f"  - softball_stats.db (Database)")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()