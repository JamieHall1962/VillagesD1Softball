#!/usr/bin/env python3
"""
Clean up rankings spreadsheet:
1. Move PID to first column
2. Delete AVG, OBP, SLG, OPS
3. Group convBA columns together
4. Group convBA+ columns together
5. Format convBA as .999 (3 decimals)
"""

import pandas as pd
from datetime import datetime
import shutil

EXCEL_FILE = 'w26rankings.xlsx'

# Create backup
backup_file = f"w26rankings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
print(f"Creating backup: {backup_file}")
shutil.copy(EXCEL_FILE, backup_file)

# Load rankings
print(f"Loading {EXCEL_FILE}...")
df = pd.read_excel(EXCEL_FILE, sheet_name='rankings')
print(f"  Found {len(df)} players")

# Delete columns
print("Removing AVG, OBP, SLG, OPS...")
cols_to_remove = ['AVG', 'OBP', 'SLG', 'OPS']
df = df.drop(columns=cols_to_remove)

# Reorder columns
print("Reordering columns...")
new_order = [
    'PID',           # Move to first
    'FirstName',
    'LastName',
    'Position',
    'PA',
    'HR',
    'convBA_F25',    # Group raw convBA
    'convBA_S25',
    'convBA_W25',
    'convBA+_F25',   # Group convBA+
    'convBA+_S25',
    'convBA+_W25',
    'Availability'
]

df = df[new_order]

# Format convBA columns to 3 decimals (will display as .999)
print("Formatting convBA columns to 3 decimals...")
for col in ['convBA_F25', 'convBA_S25', 'convBA_W25']:
    # Round to 3 decimals
    df[col] = df[col].apply(lambda x: round(x, 3) if pd.notna(x) and isinstance(x, (int, float)) else x)

# Save
print(f"\nSaving {EXCEL_FILE}...")
with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='rankings', index=False)

print(f"\n[DONE]")
print(f"  Removed: AVG, OBP, SLG, OPS")
print(f"  Column order: PID, FirstName, LastName, Position, PA, HR,")
print(f"                convBA_F25, convBA_S25, convBA_W25,")
print(f"                convBA+_F25, convBA+_S25, convBA+_W25, Availability")
print(f"  Backup: {backup_file}")

