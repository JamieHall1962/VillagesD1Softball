#!/usr/bin/env python3
"""
Add a new 'rankings' tab to the Excel file
Columns: FirstName, LastName, PersonNumber, Position1, Position2, Availability
"""

import pandas as pd
from datetime import datetime
import shutil

EXCEL_FILE = 'w26reg.xlsx'

# Create backup
backup_file = f"w26reg_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
print(f"Creating backup: {backup_file}")
shutil.copy(EXCEL_FILE, backup_file)

# Load the full_time_players sheet
print(f"Loading {EXCEL_FILE}...")
df = pd.read_excel(EXCEL_FILE, sheet_name='full_time_players')
print(f"  Found {len(df)} players")

# Create rankings dataframe with selected columns
rankings_df = df[['FirstName', 'LastName', 'PersonNumber', 'Position1', 'Position2', 'Availability']].copy()

# Rename PersonNumber to PID
rankings_df = rankings_df.rename(columns={'PersonNumber': 'PID'})

# Add new empty Position column (for manual entry)
rankings_df.insert(3, 'Position', '')

# Sort by LastName, FirstName
rankings_df = rankings_df.sort_values(['LastName', 'FirstName']).reset_index(drop=True)

print(f"  Created rankings sheet with {len(rankings_df)} players")

# Read all existing sheets
print("Reading all worksheets...")
excel_file = pd.ExcelFile(EXCEL_FILE)
all_sheets = {}
for sheet in excel_file.sheet_names:
    all_sheets[sheet] = pd.read_excel(EXCEL_FILE, sheet_name=sheet)
    print(f"  - {sheet}")

# Add rankings sheet
all_sheets['rankings'] = rankings_df

# Write all sheets back
print(f"\nSaving {EXCEL_FILE} with new rankings tab...")
with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
    for sheet_name, sheet_df in all_sheets.items():
        sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"  - Writing: {sheet_name}")

print(f"\n[DONE]")
print(f"  Added 'rankings' tab with {len(rankings_df)} players")
print(f"  Backup: {backup_file}")

