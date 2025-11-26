#!/usr/bin/env python3
"""
Create new w26rankings.xlsx file with rankings data
Columns: FirstName, LastName, PID, Position, Position1, Position2, Availability
"""

import pandas as pd

SOURCE_EXCEL = 'w26reg.xlsx'
OUTPUT_EXCEL = 'w26rankings.xlsx'

# Load the full_time_players sheet
print(f"Loading {SOURCE_EXCEL}...")
df = pd.read_excel(SOURCE_EXCEL, sheet_name='full_time_players')
print(f"  Found {len(df)} players")

# Create rankings dataframe with selected columns
rankings_df = df[['FirstName', 'LastName', 'PersonNumber', 'Position1', 'Position2', 'Availability']].copy()

# Rename PersonNumber to PID
rankings_df = rankings_df.rename(columns={'PersonNumber': 'PID'})

# Add new empty Position column (for manual entry) - insert after PID
rankings_df.insert(2, 'Position', '')

# Sort by LastName, FirstName
rankings_df = rankings_df.sort_values(['LastName', 'FirstName']).reset_index(drop=True)

print(f"  Created rankings with {len(rankings_df)} players")

# Write to new Excel file
print(f"\nCreating {OUTPUT_EXCEL}...")
with pd.ExcelWriter(OUTPUT_EXCEL, engine='openpyxl') as writer:
    rankings_df.to_excel(writer, sheet_name='rankings', index=False)

print(f"\n[DONE]")
print(f"  Created: {OUTPUT_EXCEL}")
print(f"  Sheet: rankings")
print(f"  Players: {len(rankings_df)}")
print(f"  Columns: FirstName, LastName, PID, Position (empty), Position1, Position2, Availability")

