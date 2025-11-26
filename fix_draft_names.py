#!/usr/bin/env python3
"""
Simple script to fix draft names:
- Look up PersonNumber from Excel registration
- Get correct database name for that PersonNumber
- Update draft CSV with database names
- Leave new players (not in Excel) as-is
"""

import pandas as pd
import sqlite3
import csv
from datetime import datetime
import re

EXCEL_FILE = 'w26reg.xlsx'
DRAFT_CSV = 'draft_f25.csv'
DATABASE_PATH = 'softball_stats.db'

def normalize_name(name):
    """Remove extra spaces"""
    return re.sub(r'\s+', ' ', name.strip().upper())

# Load Excel to get PersonNumbers
print("Loading registration Excel...")
excel_df = pd.read_excel(EXCEL_FILE, sheet_name='full_time_players')
print(f"  Found {len(excel_df)} registered players")

# Create lookup: normalized name -> PersonNumber
name_to_id = {}
for _, row in excel_df.iterrows():
    key = normalize_name(f"{row['LastName']}, {row['FirstName']}")
    name_to_id[key] = row['PersonNumber']

# Load database names
print("Loading database...")
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()
cursor.execute("SELECT PersonNumber, FirstName, LastName FROM People")
db_players = {}
for row in cursor.fetchall():
    db_players[row[0]] = {  # PersonNumber
        'FirstName': row[1],
        'LastName': row[2]
    }
conn.close()
print(f"  Found {len(db_players)} players in database")

# Load draft CSV
print(f"\nLoading draft CSV: {DRAFT_CSV}")
with open(DRAFT_CSV, 'r', encoding='utf-8-sig') as f:  # utf-8-sig handles BOM
    reader = csv.DictReader(f)
    draft_data = list(reader)

print(f"  Found {len(draft_data)} players in draft")

# Create backup
backup_file = f"draft_f25_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
with open(backup_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['TEAM', 'PLAYER', 'IS_MANAGER'])
    writer.writeheader()
    writer.writerows(draft_data)
print(f"  Created backup: {backup_file}")

# Process each player
print("\nProcessing players...")
updated = 0
unchanged = 0

for row in draft_data:
    original_name = row['PLAYER']
    normalized = normalize_name(original_name)
    
    # Look up in Excel
    if normalized in name_to_id:
        person_number = name_to_id[normalized]
        
        # Get database name
        if person_number in db_players:
            db_player = db_players[person_number]
            new_name = f"{db_player['LastName']}, {db_player['FirstName']}"
            
            if new_name != original_name:
                row['PLAYER'] = new_name
                updated += 1
                print(f"  [OK] Updated: {original_name} -> {new_name} (ID: {person_number})")
            else:
                unchanged += 1
        else:
            print(f"  [WARN] PersonNumber {person_number} not in database for {original_name}")
            unchanged += 1
    else:
        print(f"  [NEW] Keeping as-is: {original_name}")
        unchanged += 1

# Write updated CSV
print(f"\nWriting updated CSV...")
with open(DRAFT_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['TEAM', 'PLAYER', 'IS_MANAGER'])
    writer.writeheader()
    writer.writerows(draft_data)

print(f"\n[DONE]")
print(f"  Updated: {updated} players")
print(f"  Unchanged: {unchanged} players (already correct or new)")
print(f"  Total: {len(draft_data)} players")

