# Draft Page Documentation

## Overview
The Draft page helps match player names from the draft roster CSV to database players, automatically using PersonNumbers from the registration Excel file.

## How It Works

### Automatic Matching (Most Players)
1. **Reads from Registration Excel**: The page automatically loads the `w26reg.xlsx` file's `full_time_players` sheet
2. **Smart Name Matching**: Player names are normalized (removing extra spaces, case-insensitive) and matched automatically
3. **PersonNumber Assignment**: Matched players automatically get their PersonNumber from the registration system
4. **Success Rate**: Approximately 102/132 players (77%) match automatically

### Manual Selection (New/Unmatched Players)
For the ~30 players that don't auto-match:
1. A dropdown appears with all database players
2. Select the correct player from the dropdown
3. Their PersonNumber will be used

### Saving Changes
- Click "Save All Matches" button
- A backup file is created: `draft_f25_backup_YYYYMMDD_HHMMSS.csv`
- The original `draft_f25.csv` is updated with standardized database names
- Player names are converted to match database format: `LASTNAME, FIRSTNAME`

## Access
- Navigate to: http://localhost:5020/draft
- Or click the "Draft" card from the home page

## Features
- ✅ Visual team-by-team display
- ✅ Color-coded status (green = matched, red = needs attention)
- ✅ Manager badges
- ✅ Statistics dashboard (Total/Matched/Unmatched counts)
- ✅ Automatic backup before saving
- ✅ Success confirmation messages

## Files
- **Input**: `draft_f25.csv` (draft roster)
- **Reference**: `w26reg.xlsx` (registration data with PersonNumbers)
- **Output**: Updated `draft_f25.csv` + backup file
- **Template**: `templates/draft.html`
- **Routes**: `/draft` (display), `/draft/save` (save changes)

## Next Steps
After matching is complete:
1. All player names will be standardized to database format
2. Ready to proceed to rankings page (more complex)
3. Player names will be consistent across all systems

