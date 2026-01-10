"""
Convert schedule from calendar format to Doug's data entry format
"""
import pandas as pd
import re
from datetime import datetime

def parse_game(game_str, date_str):
    """Parse a game string like '9:00 Big Dawgs at Bearcats on 1'"""
    if not game_str or pd.isna(game_str):
        return None
    
    game_str = str(game_str).strip()
    
    # Skip non-game entries
    skip_keywords = ['PRACTICE', 'Playoffs', 'All-Star', 'Championship', 'Quarterfinals', 'Semifinals', 'Round']
    for keyword in skip_keywords:
        if keyword in game_str:
            return None
    
    # Skip placeholder games (Clippers #1, Ballers #2, etc.)
    if '#' in game_str:
        return None
    
    # Pattern: "Time Visitor at Home on Field"
    # Example: "9:00 Big Dawgs at Bearcats on 1"
    pattern = r'^(\d{1,2}:\d{2})\s+(.+?)\s+at\s+(.+?)\s+on\s+(\d+)$'
    match = re.match(pattern, game_str)
    
    if not match:
        print(f"Could not parse: {game_str}")
        return None
    
    time_str = match.group(1)
    visitor = match.group(2).strip()
    home = match.group(3).strip()
    location = match.group(4)
    
    # Convert time to AM format
    hour = int(time_str.split(':')[0])
    minute = time_str.split(':')[1]
    am_pm = 'AM'
    game_time = f"{hour}:{minute}:00 {am_pm}"
    
    return {
        'Game Date': date_str,
        'GameTime': game_time,
        'VisitorTeam': visitor,
        'HomeTeam': home,
        'Location': location
    }

def parse_date(date_str):
    """Parse date like 'Wednesday, January 07' to '1/7/2026'"""
    if not date_str or pd.isna(date_str):
        return None
    
    date_str = str(date_str).strip()
    
    # Skip non-date entries
    if not any(day in date_str for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']):
        return None
    
    try:
        # Remove day of week
        date_part = date_str.split(', ')[1] if ', ' in date_str else date_str
        
        # Parse month and day
        parts = date_part.split()
        month_name = parts[0]
        day = int(parts[1])
        
        # Map month name to number
        months = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        month = months.get(month_name, 1)
        
        # Year is 2026 for W26
        year = 2026
        
        return f"{month}/{day}/{year}"
    except:
        return None

def convert_schedule():
    # Read the schedule
    df = pd.read_excel('Doug_W26_Rosters_20260102.xlsx', sheet_name='Schedule', header=None)
    
    games = []
    current_wed_date = None
    current_fri_date = None
    
    for idx, row in df.iterrows():
        col0 = row[0] if 0 in row.index else None
        col2 = row[2] if 2 in row.index else None
        
        # Check for date headers
        wed_date = parse_date(col0)
        fri_date = parse_date(col2)
        
        if wed_date:
            current_wed_date = wed_date
        if fri_date:
            current_fri_date = fri_date
        
        # Parse games from column 0 (Wednesday)
        if current_wed_date and col0:
            game = parse_game(col0, current_wed_date)
            if game:
                games.append(game)
        
        # Parse games from column 2 (Friday)
        if current_fri_date and col2:
            game = parse_game(col2, current_fri_date)
            if game:
                games.append(game)
    
    # Create DataFrame and sort by date/time
    schedule_df = pd.DataFrame(games)
    
    # Sort by date then time
    schedule_df['sort_date'] = pd.to_datetime(schedule_df['Game Date'], format='%m/%d/%Y')
    schedule_df['sort_time'] = schedule_df['GameTime'].str.replace(':00 AM', '').str.replace(':', '').astype(int)
    schedule_df = schedule_df.sort_values(['sort_date', 'sort_time', 'Location'])
    schedule_df = schedule_df.drop(columns=['sort_date', 'sort_time'])
    
    # Save to Excel
    output_file = 'Doug_W26_Schedule.xlsx'
    schedule_df.to_excel(output_file, index=False, sheet_name='Schedule')
    
    print(f"Converted {len(schedule_df)} games")
    print(f"Output saved to: {output_file}")
    print("\nFirst 10 games:")
    print(schedule_df.head(10).to_string(index=False))
    
    return schedule_df

if __name__ == '__main__':
    convert_schedule()


