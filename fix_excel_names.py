#!/usr/bin/env python3
"""
Update FirstName and LastName in Excel to match database
- If PersonNumber exists, get correct name from database
- If no PersonNumber, leave as-is (new players)
"""

import pandas as pd
import sqlite3
from datetime import datetime

EXCEL_FILE = 'w26reg.xlsx'
SHEET_NAME = 'full_time_players'
DATABASE_PATH = 'softball_stats.db'

# Create backup
backup_file = f"w26reg_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
print(f"Creating backup: {backup_file}")
import shutil
shutil.copy(EXCEL_FILE, backup_file)

# Load Excel
print(f"Loading {EXCEL_FILE}...")
df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
print(f"  Found {len(df)} players")

# Load database
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

# Update names
print("\nUpdating names...")
updated = 0
skipped = 0

for idx, row in df.iterrows():
    person_number = row['PersonNumber']
    
    # Skip if no PersonNumber (new player)
    if pd.isna(person_number):
        print(f"  [SKIP] No ID: {row['FirstName']} {row['LastName']}")
        skipped += 1
        continue
    
    person_number = int(person_number)
    
    # Get database name
    if person_number in db_players:
        db_first = db_players[person_number]['FirstName']
        db_last = db_players[person_number]['LastName']
        
        old_first = row['FirstName']
        old_last = row['LastName']
        
        if db_first != old_first or db_last != old_last:
            df.at[idx, 'FirstName'] = db_first
            df.at[idx, 'LastName'] = db_last
            print(f"  [OK] {old_first} {old_last} -> {db_first} {db_last} (ID: {person_number})")
            updated += 1
    else:
        print(f"  [WARN] ID {person_number} not in database: {row['FirstName']} {row['LastName']}")
        skipped += 1

# Save Excel - preserve all other sheets
print(f"\nSaving {EXCEL_FILE}...")
# Read all sheets first
excel_file = pd.ExcelFile(EXCEL_FILE)
all_sheets = {}
for sheet in excel_file.sheet_names:
    if sheet == SHEET_NAME:
        all_sheets[sheet] = df  # Use our updated dataframe
    else:
        all_sheets[sheet] = pd.read_excel(EXCEL_FILE, sheet_name=sheet)

# Write all sheets back
with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
    for sheet_name, sheet_df in all_sheets.items():
        sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"\n[DONE]")
print(f"  Updated: {updated} players")
print(f"  Skipped: {skipped} players (no ID or not found)")
print(f"  Total: {len(df)} players")
print(f"  Backup: {backup_file}")

