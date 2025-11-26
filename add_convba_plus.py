#!/usr/bin/env python3
"""
Add convBA+ columns (normalized to league average = 100)
Formula: convBA+ = (player_convBA / league_avg_convBA) * 100
"""

import pandas as pd
import sqlite3
from datetime import datetime
import shutil

EXCEL_FILE = 'w26rankings.xlsx'
DATABASE_PATH = 'softball_stats.db'

# Create backup
backup_file = f"w26rankings_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
print(f"Creating backup: {backup_file}")
shutil.copy(EXCEL_FILE, backup_file)

# Load rankings
print(f"Loading {EXCEL_FILE}...")
df = pd.read_excel(EXCEL_FILE, sheet_name='rankings')
print(f"  Found {len(df)} players")

# Connect to database
print("\nCalculating league average convBA for each season...")
conn = sqlite3.connect(DATABASE_PATH)

def calculate_league_avg_convba(season_suffix):
    """Calculate league average convBA for a season"""
    query = """
        SELECT 
            SUM(PA) as PA,
            SUM(H) as H,
            SUM(BB) as BB,
            SUM(SF) as SF,
            SUM([2B]) as Doubles,
            SUM([3B]) as Triples,
            SUM(HR) as HR
        FROM batting_stats bs
        INNER JOIN Teams t ON bs.TeamNumber = t.TeamNumber
        WHERE t.LongTeamName LIKE ?
    """
    
    cursor = conn.cursor()
    cursor.execute(query, (f'% {season_suffix}',))
    result = cursor.fetchone()
    
    if result and result[0]:
        pa, h, bb, sf, doubles, triples, hr = result
        total_bases = h + doubles + (2 * triples) + (3 * hr)
        
        if pa > 0:
            conv_ba = (((4*(h+bb)+total_bases)/pa)/0.305*0.25)/10
            return conv_ba
    
    return None

# Calculate league averages
league_avg_f25 = calculate_league_avg_convba('F25')
league_avg_s25 = calculate_league_avg_convba('S25')
league_avg_w25 = calculate_league_avg_convba('W25')

print(f"  F25 league avg convBA: {league_avg_f25:.3f}" if league_avg_f25 else "  F25: No data")
print(f"  S25 league avg convBA: {league_avg_s25:.3f}" if league_avg_s25 else "  S25: No data")
print(f"  W25 league avg convBA: {league_avg_w25:.3f}" if league_avg_w25 else "  W25: No data")

conn.close()

# Calculate convBA+ for each player
print("\nCalculating convBA+ for each player...")

convba_plus_f25 = []
convba_plus_s25 = []
convba_plus_w25 = []

for idx, row in df.iterrows():
    # F25
    try:
        if pd.notna(row['convBA_F25']) and league_avg_f25 and isinstance(row['convBA_F25'], (int, float)):
            convba_plus_f25.append(int(round((row['convBA_F25'] / league_avg_f25) * 100)))
        else:
            convba_plus_f25.append(None)
    except:
        convba_plus_f25.append(None)
    
    # S25
    try:
        if pd.notna(row['convBA_S25']) and league_avg_s25 and isinstance(row['convBA_S25'], (int, float)):
            convba_plus_s25.append(int(round((row['convBA_S25'] / league_avg_s25) * 100)))
        else:
            convba_plus_s25.append(None)
    except:
        convba_plus_s25.append(None)
    
    # W25
    try:
        if pd.notna(row['convBA_W25']) and league_avg_w25 and isinstance(row['convBA_W25'], (int, float)):
            convba_plus_w25.append(int(round((row['convBA_W25'] / league_avg_w25) * 100)))
        else:
            convba_plus_w25.append(None)
    except:
        convba_plus_w25.append(None)

# Add new columns
df['convBA+_F25'] = convba_plus_f25
df['convBA+_S25'] = convba_plus_s25
df['convBA+_W25'] = convba_plus_w25

# Reorder columns: put convBA+ right after convBA
base_cols = ['FirstName', 'LastName', 'PID', 'Position', 'PA', 'AVG', 'OBP', 'SLG', 'OPS', 'HR']
convba_cols = ['convBA_F25', 'convBA+_F25', 'convBA_S25', 'convBA+_S25', 'convBA_W25', 'convBA+_W25']
end_cols = ['Availability']

df = df[base_cols + convba_cols + end_cols]

# Save
print(f"\nSaving {EXCEL_FILE}...")
with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='rankings', index=False)

print(f"\n[DONE]")
print(f"  Added: convBA+_F25, convBA+_S25, convBA+_W25")
print(f"  100 = league average, >100 = above average, <100 = below average")
print(f"  Backup: {backup_file}")

