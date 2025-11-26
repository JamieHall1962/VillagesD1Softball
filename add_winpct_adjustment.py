#!/usr/bin/env python3
"""
Add Win_Pct_Adj to Ranking_Score
- Requires minimum 50 games
- Formula: (Win_Pct - 0.500) * 10, capped at ±5
- Conservative weighting since you're 1 of 11 players
"""

import pandas as pd
from datetime import datetime
import shutil
from openpyxl import load_workbook

EXCEL_FILE = 'w26rankings.xlsx'
MIN_GAMES = 50  # Minimum games to qualify

# Create backup
backup_file = f"w26rankings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
print(f"Creating backup: {backup_file}")
shutil.copy(EXCEL_FILE, backup_file)

# Load rankings
print(f"Loading {EXCEL_FILE}...")
df = pd.read_excel(EXCEL_FILE, sheet_name='rankings')
print(f"  Found {len(df)} players")

print(f"\nCalculating Win_Pct_Adj (min {MIN_GAMES} games)...")

# Calculate Win_Pct_Adj
win_pct_adjs = []
for idx, row in df.iterrows():
    total_games = row['Career_Wins'] + row['Career_Losses'] + row['Career_Ties']
    win_pct = row['Win_Pct']
    
    if total_games >= MIN_GAMES and pd.notna(win_pct):
        # Formula: (Win_Pct - 0.500) * 10, capped at ±5
        adj = (win_pct - 0.500) * 10
        adj = max(-5, min(5, adj))  # Cap at ±5
        win_pct_adjs.append(round(adj, 1))
    else:
        win_pct_adjs.append(0)

df['Win_Pct_Adj'] = win_pct_adjs

# Recalculate Ranking_Score (add Win_Pct_Adj)
print("Recalculating Ranking_Score...")
ranking_scores = []
for idx, row in df.iterrows():
    base = row['Weighted_convBA+'] if pd.notna(row['Weighted_convBA+']) else 0
    defense = row['Def_Spectrum_Pts']
    age = row['Age_Factor']
    manual = row['Manual_Adj']
    win_adj = row['Win_Pct_Adj']
    
    if base > 0:  # Only rank players with stats
        score = round(base + defense + age + manual + win_adj, 1)
        ranking_scores.append(score)
    else:
        ranking_scores.append(None)

df['Ranking_Score'] = ranking_scores

# Sort by Ranking_Score (descending)
df = df.sort_values('Ranking_Score', ascending=False, na_position='last')

# Reorder columns - add Win_Pct_Adj after Manual_Adj
new_order = [
    'PID',
    'FirstName',
    'LastName',
    'Position',
    'Age',
    'PA',
    'HR',
    'Win_Pct',
    'Career_Wins',
    'Career_Losses',
    'Career_Ties',
    'convBA_F25',
    'convBA_S25',
    'convBA_W25',
    'convBA+_F25',
    'convBA+_S25',
    'convBA+_W25',
    'Weighted_convBA+',
    'Def_Spectrum_Pts',
    'Age_Factor',
    'Manual_Adj',
    'Win_Pct_Adj',
    'Ranking_Score',
    'Availability'
]

df = df[new_order]

# Save
print(f"\nSaving {EXCEL_FILE}...")
with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='rankings', index=False)

# Re-apply formatting
print("Re-applying number formats...")
wb = load_workbook(EXCEL_FILE)
ws = wb['rankings']

# Format convBA columns (L, M, N)
for col_idx in [12, 13, 14]:  # convBA_F25, S25, W25
    for row in range(2, ws.max_row + 1):
        cell = ws.cell(row=row, column=col_idx)
        if cell.value is not None and isinstance(cell.value, (int, float)):
            cell.number_format = '.000'

# Format Win_Pct column (H)
for row in range(2, ws.max_row + 1):
    cell = ws.cell(row=row, column=8)  # Win_Pct column
    if cell.value is not None and isinstance(cell.value, (int, float)):
        cell.number_format = '.000'

wb.save(EXCEL_FILE)

print(f"\n[DONE]")
print(f"  Added: Win_Pct_Adj (requires {MIN_GAMES}+ games)")
print(f"  Formula: (Win_Pct - 0.500) * 10, capped at ±5")
print(f"  Updated: Ranking_Score includes Win_Pct_Adj")
print(f"  Backup: {backup_file}")

print(f"\nTop 10 with Win_Pct_Adj:")
display_cols = ['FirstName', 'LastName', 'Win_Pct', 'Career_Wins', 'Career_Losses', 'Win_Pct_Adj', 'Ranking_Score']
print(df[display_cols].head(10).to_string(index=False))

print(f"\nPlayers who got Win_Pct boost (50+ games, .550+):")
boosted = df[(df['Win_Pct_Adj'] > 0) & ((df['Career_Wins'] + df['Career_Losses'] + df['Career_Ties']) >= MIN_GAMES)]
if len(boosted) > 0:
    print(boosted[['FirstName', 'LastName', 'Win_Pct', 'Career_Wins', 'Career_Losses', 'Win_Pct_Adj']].head(15).to_string(index=False))

