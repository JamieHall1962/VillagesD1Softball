#!/usr/bin/env python3
"""
Find all pitching_stats records where BOTH an individual player AND team subs
have W or L for the same game
"""

import sqlite3

conn = sqlite3.connect('softball_stats.db')
cursor = conn.cursor()

# Team subs mapping
SUBS_MAPPING = {
    529: 600,   # Bad News Bears Subs
    534: 493,   # Buckeyes Subs  
    527: 480,   # Clippers Subs
    532: 540,   # Lightning Strikes Subs
    537: 584,   # Norsemen Subs
    531: 542,   # Raptors Subs
    533: 302,   # Rebels Subs
    535: 548,   # Shorebirds Subs
    526: 274,   # Stars Subs
    536: 617,   # The Sandlot Subs
    528: 400,   # Warhawks Subs
    530: 554,   # Xtreme Subs
}

print("Finding duplicate pitching records (individual + team subs)...\n")

duplicates = []

for team_num, subs_player in SUBS_MAPPING.items():
    # Find games where BOTH team subs AND another player have W or L
    cursor.execute('''
        SELECT ps1.TeamNumber, ps1.GameNumber, ps1.PlayerNumber, ps1.W, ps1.L,
               ps2.PlayerNumber as SubsPlayer, ps2.W as SubsW, ps2.L as SubsL
        FROM pitching_stats ps1
        JOIN pitching_stats ps2 ON ps1.TeamNumber = ps2.TeamNumber 
                                AND ps1.GameNumber = ps2.GameNumber
        WHERE ps1.TeamNumber = ?
          AND ps2.PlayerNumber = ?
          AND ps1.PlayerNumber != ps2.PlayerNumber
          AND ((ps1.W > 0 OR ps1.L > 0) AND (ps2.W > 0 OR ps2.L > 0))
        ORDER BY ps1.GameNumber
    ''', (team_num, subs_player))
    
    rows = cursor.fetchall()
    for row in rows:
        duplicates.append(row)
        print(f"Team {row[0]}, Game {row[1]}: Player {row[2]} (W={row[3]}, L={row[4]}) + Subs {row[5]} (W={row[6]}, L={row[7]})")

print(f"\n{'='*80}")
print(f"FOUND {len(duplicates)} DUPLICATE PITCHING RECORDS")
print(f"{'='*80}")

if duplicates:
    print("\nThese individual pitcher records should be DELETED:")
    for dup in duplicates:
        print(f"  DELETE FROM pitching_stats WHERE TeamNumber={dup[0]} AND GameNumber={dup[1]} AND PlayerNumber={dup[2]};")

conn.close()

