#!/usr/bin/env python3
"""
Find players marked as "Roster" in data.csv batting/pitching stats
but who are NOT actually on that team's roster
"""

import csv

# Parse data.csv to extract tables
def parse_data_csv():
    roster = {}  # {TeamNumber: set of PersonNumbers}
    batting_stats = []
    pitching_stats = []
    
    current_table = None
    
    with open('data.csv', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            if line.startswith('Table:'):
                current_table = line.split(':')[1].strip()
                next(f)  # Skip header row
                continue
            
            if not line:
                current_table = None
                continue
            
            if current_table == 'Roster':
                parts = line.strip('"').split('","')
                if len(parts) >= 2:
                    team_num = parts[0].strip('"')
                    person_num = parts[1].strip('"')
                    
                    if team_num not in roster:
                        roster[team_num] = set()
                    roster[team_num].add(person_num)
            
            elif current_table == 'BattingStats':
                # Parse CSV line
                parts = [p.strip('"') for p in line.split('","')]
                if len(parts) >= 25:  # Make sure we have enough columns
                    team_num = parts[0].strip('"')
                    game_num = parts[1]
                    person_num = parts[2]
                    roster_status = parts[24]  # Roster column is index 24
                    
                    batting_stats.append({
                        'TeamNumber': team_num,
                        'GameNumber': game_num,
                        'PersonNumber': person_num,
                        'Roster': roster_status
                    })
            
            elif current_table == 'PitchingStats':
                parts = [p.strip('"') for p in line.split('","')]
                if len(parts) >= 15:  # Make sure we have enough columns
                    team_num = parts[0].strip('"')
                    game_num = parts[1]
                    person_num = parts[2]
                    roster_status = parts[14]  # Roster column is index 14
                    
                    pitching_stats.append({
                        'TeamNumber': team_num,
                        'GameNumber': game_num,
                        'PersonNumber': person_num,
                        'Roster': roster_status
                    })
    
    return roster, batting_stats, pitching_stats

print("Parsing data.csv...")
roster, batting_stats, pitching_stats = parse_data_csv()

print(f"\nFound {len(roster)} teams in Roster table")
print(f"Found {len(batting_stats)} batting stat records")
print(f"Found {len(pitching_stats)} pitching stat records")

# Find mismatches
mismatches = []

# Check batting stats
for stat in batting_stats:
    team_num = stat['TeamNumber']
    person_num = stat['PersonNumber']
    roster_status = stat['Roster']
    
    # Check if marked as "Roster" but NOT on that team
    if roster_status == 'Roster':
        if team_num not in roster or person_num not in roster[team_num]:
            mismatches.append({
                'Type': 'Batting',
                'TeamNumber': team_num,
                'GameNumber': stat['GameNumber'],
                'PersonNumber': person_num,
                'CurrentStatus': 'Roster',
                'ShouldBe': 'Sub'
            })

# Check pitching stats
for stat in pitching_stats:
    team_num = stat['TeamNumber']
    person_num = stat['PersonNumber']
    roster_status = stat['Roster']
    
    # Check if marked as "Roster" but NOT on that team
    if roster_status == 'Roster':
        if team_num not in roster or person_num not in roster[team_num]:
            mismatches.append({
                'Type': 'Pitching',
                'TeamNumber': team_num,
                'GameNumber': stat['GameNumber'],
                'PersonNumber': person_num,
                'CurrentStatus': 'Roster',
                'ShouldBe': 'Sub'
            })

print(f"\n{'='*80}")
print(f"FOUND {len(mismatches)} MISMATCHES")
print(f"{'='*80}")

if mismatches:
    print("\nPlayers marked as 'Roster' but NOT on that team's roster:")
    print(f"{'Type':<10} {'Team':<8} {'Game':<6} {'Player':<8} {'Status':<10} {'Should Be'}")
    print("-" * 60)
    
    for m in mismatches[:50]:  # Show first 50
        print(f"{m['Type']:<10} {m['TeamNumber']:<8} {m['GameNumber']:<6} {m['PersonNumber']:<8} {m['CurrentStatus']:<10} {m['ShouldBe']}")
    
    if len(mismatches) > 50:
        print(f"\n... and {len(mismatches) - 50} more")
    
    # Group by team to see which teams have the most issues
    print(f"\n{'='*80}")
    print("Mismatches by Team:")
    print(f"{'='*80}")
    team_counts = {}
    for m in mismatches:
        team = m['TeamNumber']
        team_counts[team] = team_counts.get(team, 0) + 1
    
    for team, count in sorted(team_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"Team {team}: {count} mismatches")
    
    # Save to CSV
    with open('roster_mismatches.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Type', 'TeamNumber', 'GameNumber', 'PersonNumber', 'CurrentStatus', 'ShouldBe'])
        writer.writeheader()
        writer.writerows(mismatches)
    
    print(f"\nFull list saved to: roster_mismatches.csv")
else:
    print("\n[OK] No mismatches found! All 'Roster' designations are correct.")

