import sqlite3

conn = sqlite3.connect('softball_stats.db')
conn.row_factory = sqlite3.Row

# Check Seasons table structure
print("=== SEASONS TABLE ===")
seasons = conn.execute("SELECT * FROM Seasons WHERE short_name = 'W25' LIMIT 1").fetchone()
if seasons:
    print("Columns:", list(seasons.keys()))
    print("Data:", dict(seasons))
else:
    print("No W25 season found")

print("\n=== TEAMS FOR W25 ===")
# Try the current query method
teams_current = conn.execute('''
    SELECT COUNT(DISTINCT t.TeamNumber) as TeamCount
    FROM Teams t
    WHERE t.LongTeamName LIKE '%' || ? || '%'
''', ('W25',)).fetchone()
print(f"Current method count: {teams_current['TeamCount']}")

# List actual teams
teams_list = conn.execute('''
    SELECT TeamNumber, LongTeamName 
    FROM Teams 
    WHERE LongTeamName LIKE '%W25%'
    ORDER BY LongTeamName
''').fetchall()
print(f"\nActual teams found ({len(teams_list)}):")
for team in teams_list:
    print(f"  {team['TeamNumber']}: {team['LongTeamName']}")

# Try alternative - check if there's a leading/trailing space issue
print("\n=== CHECKING FOR SPACE ISSUES ===")
teams_with_space = conn.execute('''
    SELECT TeamNumber, LongTeamName, LENGTH(LongTeamName) as len
    FROM Teams 
    WHERE LongTeamName LIKE '% W25' OR LongTeamName LIKE '%W25 %' OR LongTeamName LIKE '%W25'
    ORDER BY LongTeamName
''').fetchall()
print(f"Teams with W25 pattern ({len(teams_with_space)}):")
for team in teams_with_space:
    print(f"  {team['TeamNumber']}: '{team['LongTeamName']}' (len={team['len']})")

conn.close()

