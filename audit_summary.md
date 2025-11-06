# Fall 2025 Stats Audit Summary

## Overview
Compared data.csv (from data provider) against softball_stats.db for Fall 2025 teams (526-537)

## Key Findings

### ✅ GAME STATS: No Action Needed
- All 204 games exist in both CSV and database
- Differences shown are only data type formatting (int vs float, date format)
- **No corrections needed** - sync process handles these conversions automatically

### ⚠️ BATTING STATS: 12 Records to Consider Deleting
These records exist in your database but NOT in the provider's CSV:

1. **Team 526, Game 2, Player 606** (Keith Turney)
   - PA=3, H=0, HR=0, RBI=0

2. **Team 526, Game 12, Player 635** (Unknown player)
   - PA=3, H=2, HR=0, RBI=0

3. **Team 526, Game 13, Player 639** (Unknown player)
   - PA=4, H=2, HR=0, RBI=3

4. **Team 526, Game 14, Player 639** (Unknown player)
   - PA=4, H=1, HR=0, RBI=0

5. **Team 531, Game 14, Player 635** (Unknown player)
   - PA=3, H=1, HR=0, RBI=1

6. **Team 533, Game 14, Player 636** (Unknown player)
   - PA=3, H=0, HR=0, RBI=0

7. **Team 535, Game 6, Player 626** (Unknown player)
   - PA=3, H=1, HR=0, RBI=2

8. **Team 535, Game 7, Player 626** (Unknown player)
   - PA=3, H=1, HR=0, RBI=0

9. **Team 535, Game 8, Player 630** (Unknown player)
   - PA=3, H=2, HR=0, RBI=0

10. **Team 535, Game 9, Player 630** (Unknown player)
    - PA=4, H=2, HR=0, RBI=1

11. **Team 535, Game 13, Player 638** (Unknown player)
    - PA=3, H=0, HR=0, RBI=0

12. **Team 535, Game 14, Player 638** (Unknown player)
    - PA=3, H=2, HR=0, RBI=1

### ⚠️ PITCHING STATS: 10 Records to Consider Deleting
These records exist in your database but NOT in the provider's CSV:

1. **Team 526, Game 11, Player 274** (Stars Subs)
   - IP=7.0, W=1, L=0, BB=2

2. **Team 531, Game 6, Player 542** (Raptors Subs)
   - IP=7.0, W=1, L=0, BB=0

3. **Team 532, Game 14, Player 540** (Lightning Strikes Subs)
   - IP=7.0, W=0, L=1, BB=1

4. **Team 533, Game 14, Player 636** (Unknown player)
   - IP=6.0, W=1, L=0, BB=0

5. **Team 534, Game 17, Player 493** (Buckeyes Subs)
   - IP=7.0, W=0, L=1, BB=1

6. **Team 535, Game 6, Player 626** (Unknown player)
   - IP=7.0, W=1, L=0, BB=1

7. **Team 535, Game 7, Player 626** (Unknown player)
   - IP=7.0, W=0, L=1, BB=1

8. **Team 535, Game 10, Player 548** (Shorebirds Subs)
   - IP=7.0, W=1, L=0, BB=0

9. **Team 535, Game 13, Player 638** (Unknown player)
   - IP=7.0, W=0, L=1, BB=2

10. **Team 535, Game 14, Player 638** (Unknown player)
    - IP=7.0, W=1, L=0, BB=2

## Analysis

### Patterns Identified:
1. **Unknown Players (#626, #630, #635, #636, #638, #639)**: These player numbers don't exist in the People table. Likely data entry errors.
2. **Sub Players**: Several sub player records exist in pitching stats. The data provider may not be tracking sub player stats separately.
3. **Team 535 (Shorebirds)**: Has the most discrepancies (8 out of 22 total)

## Recommendations

### Option 1: Trust the Data Provider (Safest)
Delete all 22 records (12 batting + 10 pitching) from your database since they don't appear in the official data.

### Option 2: Investigate First (More Thorough)
1. Check scoresheets for the specific games to verify which source is correct
2. Verify if Keith Turney (#606) actually played in Team 526, Game 2
3. Determine if the unknown player numbers are typos or data entry errors
4. Decide if sub player pitching stats should be tracked separately

### Option 3: Selective Cleanup (Balanced)
1. **Delete unknown players (#626, #630, #635, #636, #638, #639)** - clearly errors
2. **Investigate Keith Turney** - he's a real player, might be legitimate
3. **Keep sub player pitching stats** - if you want to track them separately
4. **Delete unknown player pitching** - matches batting cleanup

## Next Steps

1. Review this summary and decide which option to pursue
2. If needed, check original scoresheets for verification
3. Run the cleanup script (to be created) with your decisions
4. Re-run audit to confirm all corrections applied

