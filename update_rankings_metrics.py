#!/usr/bin/env python3
"""
Update rankings:
1. Remove Position1 and Position2 columns
2. Add advanced metrics from database (latest season)
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

# Remove Position1 and Position2 if they exist
if 'Position1' in df.columns and 'Position2' in df.columns:
    print("Removing Position1 and Position2 columns...")
    df = df.drop(columns=['Position1', 'Position2'])
else:
    print("Position1 and Position2 already removed")

# Remove old stat columns if they exist (so we can replace them)
old_stat_columns = ['PA', 'AVG', 'OBP', 'SLG', 'OPS', 'HR', 'convBA']
existing_stat_cols = [col for col in old_stat_columns if col in df.columns]
if existing_stat_cols:
    print(f"Removing old stat columns: {existing_stat_cols}")
    df = df.drop(columns=existing_stat_cols)

# Connect to database and get latest season stats for each player
print("Fetching advanced metrics from database...")
conn = sqlite3.connect(DATABASE_PATH)

stats_list = []
for idx, row in df.iterrows():
    pid = row['PID']
    
    if pd.isna(pid):
        # New player - no stats
        stats_list.append({
            'PA': 'NEW',
            'AVG': 'NEW', 
            'OBP': 'NEW',
            'SLG': 'NEW',
            'OPS': 'NEW',
            'HR': 'NEW',
            'convBA': 'NEW'
        })
        continue
    
    pid = int(pid)
    
    # Get F25 season stats (aggregate all games for F25 team)
    query = """
        SELECT 
            SUM(PA) as PA,
            SUM(H) as H,
            SUM(BB) as BB,
            SUM(SF) as SF,
            SUM(OE) as OE,
            SUM([2B]) as Doubles,
            SUM([3B]) as Triples,
            SUM(HR) as HR
        FROM batting_stats bs
        INNER JOIN Teams t ON bs.TeamNumber = t.TeamNumber
        WHERE bs.PlayerNumber = ?
        AND t.LongTeamName LIKE '% F25'
    """
    
    cursor = conn.cursor()
    cursor.execute(query, (pid,))
    result = cursor.fetchone()
    
    if result and result[0]:  # Has stats
        pa, h, bb, sf, oe, doubles, triples, hr = result
        
        # Calculate AB
        ab = pa - bb - sf
        
        # Calculate stats
        avg = round(h / ab, 3) if ab > 0 else 0.000
        obp = round((h + bb + oe) / pa, 3) if pa > 0 else 0.000
        
        # Calculate SLG
        total_bases = h + doubles + (2 * triples) + (3 * hr)
        slg = round(total_bases / ab, 3) if ab > 0 else 0.000
        
        ops = round(obp + slg, 3)
        
        # Calculate convBA (the JHM easter egg): (((4*(H+BB)+TB)/PA)/0.305*0.25)/10
        conv_ba = round((((4*(h+bb)+total_bases)/pa)/0.305*0.25)/10, 3) if pa > 0 else 0.000
        
        stats_list.append({
            'PA': int(pa),
            'AVG': avg,
            'OBP': obp,
            'SLG': slg,
            'OPS': ops,
            'HR': int(hr),
            'convBA': conv_ba
        })
    else:
        # No stats
        stats_list.append({
            'PA': 0,
            'AVG': 0.000,
            'OBP': 0.000,
            'SLG': 0.000,
            'OPS': 0.000,
            'HR': 0,
            'convBA': 0.000
        })

conn.close()

# Add stats to dataframe
stats_df = pd.DataFrame(stats_list)
df = pd.concat([df, stats_df], axis=1)

# Reorder columns: FirstName, LastName, PID, Position, PA, AVG, OBP, SLG, OPS, HR, convBA, Availability
df = df[['FirstName', 'LastName', 'PID', 'Position', 'PA', 'AVG', 'OBP', 'SLG', 'OPS', 'HR', 'convBA', 'Availability']]

# Save
print(f"\nSaving {EXCEL_FILE}...")
with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='rankings', index=False)

print(f"\n[DONE]")
print(f"  Removed: Position1, Position2")
print(f"  Added: PA, AVG, OBP, SLG, OPS, HR, convBA")
print(f"  Backup: {backup_file}")

