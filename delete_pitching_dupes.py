#!/usr/bin/env python3
"""
Delete duplicate pitching records where both individual pitcher and team subs have W/L
"""

import sqlite3
from datetime import datetime
import shutil

# Create backup
backup_file = f"softball_stats.db.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
print(f"Creating backup: {backup_file}")
shutil.copy('softball_stats.db', backup_file)

conn = sqlite3.connect('softball_stats.db')
cursor = conn.cursor()

# Records to delete (individual pitchers that were subs)
deletes = [
    (532, 14, 133),
    (532, 14, 427),
    (537, 17, 438),
    (531, 6, 483),
    (531, 17, 260),
    (533, 13, 62),
    (535, 10, 427),
    (535, 17, 315),
    (526, 11, 270),
]

print(f"\nDeleting {len(deletes)} duplicate pitching records...")

for team_num, game_num, player_num in deletes:
    cursor.execute('''
        DELETE FROM pitching_stats 
        WHERE TeamNumber = ? AND GameNumber = ? AND PlayerNumber = ?
    ''', (team_num, game_num, player_num))
    print(f"  Deleted: Team {team_num}, Game {game_num}, Player {player_num}")

conn.commit()
print(f"\n[DONE] Deleted {len(deletes)} records")
print(f"Backup: {backup_file}")

# Verify
print("\nVerifying duplicates are gone...")
cursor.execute('''
    SELECT COUNT(*) 
    FROM pitching_stats ps1
    JOIN pitching_stats ps2 ON ps1.TeamNumber = ps2.TeamNumber 
                            AND ps1.GameNumber = ps2.GameNumber
    WHERE ps1.PlayerNumber != ps2.PlayerNumber
      AND ((ps1.W > 0 OR ps1.L > 0) AND (ps2.W > 0 OR ps2.L > 0))
      AND ps2.PlayerNumber IN (600, 493, 480, 540, 584, 542, 302, 548, 274, 617, 400, 554)
''')
remaining = cursor.fetchone()[0]
if remaining == 0:
    print("[OK] No duplicate pitching records remain!")
else:
    print(f"[WARNING] {remaining} duplicate records still exist")

conn.close()

