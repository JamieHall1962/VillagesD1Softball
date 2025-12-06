# New Season Setup Guide

This guide explains how to set up a new season in the D1 Softball Stats system.

## Overview

The `start_new_season.py` script automates the creation of:
- A new season record
- Team records (with division names if applicable)
- Player roster entries (linking existing players by PID)
- New player records (for players without PIDs)
- Team subs on each roster
- An Excel file with all rosters for data entry

---

## Step 1: Create the Draft CSV File

Create a CSV file named `draft_[season].csv` (e.g., `draft_w26.csv`) with the following format:

```csv
TEAM,PLAYER,IS_MANAGER,PID
Buckeyes,"Smith, John",YES,245
Buckeyes,"Jones, Bob",NO,389
Buckeyes,"NewGuy, Tom",NO,
Stars,"Wilson, Dave",YES,156
```

### Column Definitions

| Column | Description | Required |
|--------|-------------|----------|
| TEAM | Team name (see naming below) | Yes |
| PLAYER | Player name in "LastName, FirstName" format | Yes |
| IS_MANAGER | "YES" if player is team manager, otherwise "NO" or blank | Yes |
| PID | PersonNumber for returning players, **blank for new players** | No |

### Team Naming

**Without divisions:**
```
Buckeyes
Stars
Raptors
```

**With divisions** (division name in parentheses):
```
Buckeyes (Palmese)
Stars (Ballers)
Raptors (East)
```

The division name in parentheses will be automatically detected by the web app and used to display separate division standings.

### Finding Player IDs (PIDs)

- PIDs are the `PersonNumber` from the database
- You can find them in the registration Excel file (`w26reg.xlsx`) or by querying the database
- **Leave PID blank for brand new players** - the script will create them

### Non-Playing Managers

If a team's manager is not a player (like Steve Mills for Team USA), they won't be in the CSV. After running the script, manually update the manager:

```sql
UPDATE Teams SET Manager = 'Manager Name' WHERE LongTeamName = 'Team Name W26';
```

---

## Step 2: Configure the Script

Open `start_new_season.py` and update the configuration section near the bottom:

```python
# ============================================================
# CONFIGURE THESE FOR EACH NEW SEASON
# ============================================================
db_path = "softball_stats.db"
csv_path = "draft_w26.csv"          # Draft CSV file with PID column
season_name = "Winter 2026"          # Full season name
short_name = "W26"                   # Short code (used in team names)
year = 2026                          # Year
# ============================================================
```

### Season Naming Convention

| Season | season_name | short_name |
|--------|-------------|------------|
| Winter 2026 | "Winter 2026" | "W26" |
| Spring 2026 | "Spring 2026" | "S26" |
| Fall 2026 | "Fall 2026" | "F26" |

---

## Step 3: Run the Script

```bash
python start_new_season.py
```

### What the Script Does

1. **Creates Season** - Adds new season record to `Seasons` table
2. **Parses CSV** - Reads team/player data, identifies returning vs new players
3. **Creates Teams** - Creates team records with format "TeamName (Division) ShortName"
4. **Links Players** - 
   - Returning players (with PID): Links directly by PersonNumber
   - New players (blank PID): Creates new People record, then links
5. **Adds Subs** - 
   - Existing teams: Uses existing subs (e.g., "Buckeyes Subs")
   - New teams: Creates new subs record
6. **Exports Excel** - Creates `[ShortName]_Team_Rosters_[Date].xlsx`

### Expected Output

```
NEW SEASON SETUP
==================================================
Database: softball_stats.db
Draft CSV: draft_w26.csv
Season: Winter 2026 (W26)
==================================================

Processing team: Buckeyes (Palmese)
------------------------------
Created team: Buckeyes (Palmese) W26 (Manager: Tom Pratt) (TeamNumber: 538)
  1. Jim Okunze -> PID 383 (Jim Okunze)
  2. Michael Johnson -> PID 565 (Michael Johnson)
  ...

[OK] SETUP COMPLETE - Ready for Winter 2026 season!
```

---

## Step 4: Post-Setup Verification

### Check the Web App

1. Start the app: `python app.py`
2. Navigate to the Seasons page
3. Verify the new season appears with correct teams and divisions

### Common Fixes

**Non-playing manager not set:**
```sql
UPDATE Teams SET Manager = 'Steve Mills' WHERE LongTeamName = 'Team USA (Ballers) W26';
```

**Team name typo:**
```sql
UPDATE Teams SET LongTeamName = 'Correct Name W26' WHERE TeamNumber = XXX;
```

---

## File Outputs

After running the script, you'll have:

| File | Description |
|------|-------------|
| `[ShortName]_Team_Rosters_[Date].xlsx` | Excel file with all team rosters for data entry |

---

## Database Tables Affected

| Table | Changes |
|-------|---------|
| `Seasons` | New season record added |
| `Teams` | New team records (one per team) |
| `People` | New player records (for new players and new subs) |
| `Roster` | New roster entries (player-to-team links) |

---

## Troubleshooting

### "Expected columns" error
Your CSV columns don't match. Must be exactly: `TEAM,PLAYER,IS_MANAGER,PID`

### Player matched to wrong person
Check if there's a PID in the CSV. If blank, verify the new player was created correctly.

### Subs not linking correctly
The script matches subs by **base team name** (without division). Ensure existing subs use standard names like "Buckeyes Subs", not "Buckeyes (Palmese) Subs".

### Unicode errors on Windows
The script uses ASCII characters for output. If you see encoding errors, check for special characters in team/player names.

---

## Quick Reference

### Typical Season Setup Checklist

- [ ] Create draft CSV with TEAM, PLAYER, IS_MANAGER, PID columns
- [ ] Include division names in parentheses if using divisions
- [ ] Verify PIDs for all returning players
- [ ] Leave PID blank for new players
- [ ] Update script configuration (csv_path, season_name, short_name, year)
- [ ] Run `python start_new_season.py`
- [ ] Update any non-playing managers manually
- [ ] Verify in web app

---

## Contact

For questions about this process, check with the current league statistician or review the git history for this repository.

*Last updated: December 2024*

