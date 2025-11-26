#!/usr/bin/env python3
"""
Add trending convBA columns: F25, S25, W25
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

# Rename existing convBA to convBA_F25
if 'convBA' in df.columns:
    print("Renaming convBA to convBA_F25...")
    df = df.rename(columns={'convBA': 'convBA_F25'})

# Connect to database
print("Fetching convBA for S25 and W25...")
conn = sqlite3.connect(DATABASE_PATH)

def get_convba_for_season(pid, season_suffix):
    """Get convBA for a specific season (e.g., 'F25', 'S25', 'W25')"""
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
        WHERE bs.PlayerNumber = ?
        AND t.LongTeamName LIKE ?
    """
    
    cursor = conn.cursor()
    cursor.execute(query, (pid, f'% {season_suffix}'))
    result = cursor.fetchone()
    
    if result and result[0]:  # Has stats
        pa, h, bb, sf, doubles, triples, hr = result
        total_bases = h + doubles + (2 * triples) + (3 * hr)
        
        if pa > 0:
            conv_ba = round((((4*(h+bb)+total_bases)/pa)/0.305*0.25)/10, 3)
            return conv_ba
    
    return None  # No stats for this season

# Add S25 and W25 convBA
convba_s25_list = []
convba_w25_list = []

for idx, row in df.iterrows():
    pid = row['PID']
    
    if pd.isna(pid):
        # New player - no stats
        convba_s25_list.append(None)
        convba_w25_list.append(None)
        continue
    
    pid = int(pid)
    
    # Get S25 and W25 convBA
    convba_s25 = get_convba_for_season(pid, 'S25')
    convba_w25 = get_convba_for_season(pid, 'W25')
    
    convba_s25_list.append(convba_s25)
    convba_w25_list.append(convba_w25)

conn.close()

# Add new columns
df['convBA_S25'] = convba_s25_list
df['convBA_W25'] = convba_w25_list

# Reorder columns to put trending convBA columns together
# Keep all existing columns, just reorder the convBA ones
base_cols = ['FirstName', 'LastName', 'PID', 'Position', 'PA', 'AVG', 'OBP', 'SLG', 'OPS', 'HR']
convba_cols = ['convBA_F25', 'convBA_S25', 'convBA_W25']
end_cols = ['Availability']

df = df[base_cols + convba_cols + end_cols]

# Save
print(f"\nSaving {EXCEL_FILE}...")
with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='rankings', index=False)

print(f"\n[DONE]")
print(f"  Added: convBA_S25, convBA_W25")
print(f"  Renamed: convBA -> convBA_F25")
print(f"  Column order: ...HR, convBA_F25, convBA_S25, convBA_W25, Availability")
print(f"  Backup: {backup_file}")

