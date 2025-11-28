#!/usr/bin/env python3
"""
Fix the 5 Roster/Sub mismatches in data.csv
Change these pitching records from "Roster" to "Sub":
- Team 531, Game 6, Player 483
- Team 535, Game 10, Player 427
- Team 526, Game 11, Player 270
- Team 533, Game 13, Player 62
- Team 531, Game 17, Player 260
"""

from datetime import datetime
import shutil

# Create backup
backup_file = f"data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
print(f"Creating backup: {backup_file}")
shutil.copy('data.csv', backup_file)

# Records to fix
fixes = [
    ('531', '6', '483'),
    ('535', '10', '427'),
    ('526', '11', '270'),
    ('533', '13', '62'),
    ('531', '17', '260')
]

print("\nReading data.csv...")
with open('data.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Fixing mismatches...")
fixed_count = 0
current_table = None
in_pitching_stats = False

for i, line in enumerate(lines):
    if line.strip().startswith('Table:'):
        current_table = line.strip().split(':')[1].strip()
        in_pitching_stats = (current_table == 'PitchingStats')
        continue
    
    if in_pitching_stats and line.strip() and not line.startswith('TeamNumber'):
        # Parse the line
        parts = line.strip().strip('"').split('","')
        if len(parts) >= 15:
            team_num = parts[0].strip('"')
            game_num = parts[1]
            person_num = parts[2]
            roster_status = parts[14]
            
            # Check if this is one of the records to fix
            if (team_num, game_num, person_num) in fixes:
                if roster_status == 'Roster':
                    # Replace "Roster" with "Sub" in this line
                    # The Roster column is at index 14
                    parts[14] = 'Sub'
                    
                    # Rebuild the line
                    new_line = '"' + '","'.join(parts) + '"\n'
                    lines[i] = new_line
                    
                    print(f"  Fixed: Team {team_num}, Game {game_num}, Player {person_num}: Roster -> Sub")
                    fixed_count += 1

# Write the corrected file
print(f"\nWriting corrected data.csv...")
with open('data.csv', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"\n[DONE]")
print(f"  Fixed {fixed_count} records")
print(f"  Backup: {backup_file}")
print(f"\nNext step: Run data_update.py to import the corrected data into the database")

