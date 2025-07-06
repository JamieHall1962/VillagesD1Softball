"""
D1 Softball League Schedule Generator
Creates balanced schedules for multiple teams with constraints
"""

import json
import csv
from datetime import datetime, timedelta
from ortools.sat.python import cp_model
import pandas as pd
import numpy as np

class SoftballScheduler:
    def __init__(self):
        self.teams = []
        self.games = []
        self.schedule = []
        
    def add_team(self, name, home_field=None):
        """Add a team to the league"""
        team = {
            'name': name,
            'home_field': home_field or name,
            'games_played': 0,
            'home_games': 0,
            'away_games': 0
        }
        self.teams.append(team)
        
    def generate_schedule(self, games_per_team=12, start_date=None, 
                         avoid_dates=None, max_games_per_week=3):
        """
        Generate a balanced schedule for all teams
        
        Args:
            games_per_team: Number of games each team should play
            start_date: Starting date for the season (default: next Monday)
            avoid_dates: List of dates to avoid (holidays, etc.)
            max_games_per_week: Maximum games per team per week
        """
        
        if len(self.teams) < 2:
            raise ValueError("Need at least 2 teams to generate a schedule")
            
        if len(self.teams) % 2 != 0:
            # Add a "BYE" team if odd number of teams
            self.add_team("BYE", "BYE")
            
        # Set default start date to next Monday
        if start_date is None:
            today = datetime.now()
            days_until_monday = (7 - today.weekday()) % 7
            start_date = today + timedelta(days=days_until_monday)
            
        if avoid_dates is None:
            avoid_dates = []
            
        # Convert avoid_dates to datetime objects if they're strings
        avoid_dates = [datetime.strptime(date, '%Y-%m-%d') if isinstance(date, str) else date 
                      for date in avoid_dates]
        
        # Create the constraint programming model
        model = cp_model.CpModel()
        
        num_teams = len(self.teams)
        num_rounds = games_per_team // (num_teams - 1)  # Each team plays each other team
        
        # Variables: game[i][j][r] = 1 if team i plays team j in round r
        game = {}
        for i in range(num_teams):
            for j in range(num_teams):
                if i != j:
                    for r in range(num_rounds):
                        game[i, j, r] = model.NewBoolVar(f'game_{i}_{j}_{r}')
        
        # Constraints
        
        # 1. Each team plays exactly one game per round
        for r in range(num_rounds):
            for i in range(num_teams):
                model.Add(sum(game[i, j, r] for j in range(num_teams) if i != j) +
                         sum(game[j, i, r] for j in range(num_teams) if i != j) == 1)
        
        # 2. If team i plays team j in round r, team j plays team i in round r
        for r in range(num_rounds):
            for i in range(num_teams):
                for j in range(num_teams):
                    if i != j:
                        model.Add(game[i, j, r] == game[j, i, r])
        
        # 3. Each pair of teams plays approximately the same number of times
        for i in range(num_teams):
            for j in range(num_teams):
                if i < j:  # Avoid counting same pair twice
                    total_games = sum(game[i, j, r] for r in range(num_rounds))
                    # Allow some flexibility in number of games between teams
                    model.Add(total_games >= games_per_team // (num_teams - 1) - 1)
                    model.Add(total_games <= games_per_team // (num_teams - 1) + 1)
        
        # 4. Balance home and away games
        for i in range(num_teams):
            home_games = sum(game[i, j, r] for j in range(num_teams) if i != j 
                           for r in range(num_rounds))
            away_games = sum(game[j, i, r] for j in range(num_teams) if i != j 
                           for r in range(num_rounds))
            # Home and away games should be roughly equal
            model.Add(home_games >= away_games - 2)
            model.Add(home_games <= away_games + 2)
        
        # Solve the model
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(f"Schedule generated successfully!")
            print(f"Status: {solver.StatusName(status)}")
            
            # Extract the schedule
            self._extract_schedule(solver, game, num_rounds, start_date, avoid_dates, max_games_per_week)
            
        else:
            print("No solution found!")
            return False
            
        return True
    
    def _extract_schedule(self, solver, game, num_rounds, start_date, avoid_dates, max_games_per_week):
        """Extract the schedule from the solver solution"""
        schedule = []
        current_date = start_date
        
        for r in range(num_rounds):
            round_games = []
            
            for i in range(len(self.teams)):
                for j in range(len(self.teams)):
                    if i < j and solver.Value(game[i, j, r]) == 1:
                        # Determine home team (alternate between i and j)
                        home_team = i if r % 2 == 0 else j
                        away_team = j if r % 2 == 0 else i
                        
                        # Skip if either team is BYE
                        if self.teams[home_team]['name'] == 'BYE' or self.teams[away_team]['name'] == 'BYE':
                            continue
                            
                        round_games.append({
                            'home_team': self.teams[home_team]['name'],
                            'away_team': self.teams[away_team]['name'],
                            'home_field': self.teams[home_team]['home_field'],
                            'round': r + 1
                        })
            
            # Assign dates to games in this round
            games_this_round = len(round_games)
            if games_this_round > 0:
                # Spread games across the week
                days_between_games = max(1, 7 // games_this_round)
                
                for idx, game_info in enumerate(round_games):
                    game_date = current_date + timedelta(days=idx * days_between_games)
                    
                    # Skip avoid dates
                    while game_date in avoid_dates:
                        game_date += timedelta(days=1)
                    
                    game_info['date'] = game_date.strftime('%Y-%m-%d')
                    game_info['day_of_week'] = game_date.strftime('%A')
                    schedule.append(game_info)
            
            # Move to next week
            current_date += timedelta(days=7)
        
        self.schedule = schedule
        
    def export_csv(self, filename):
        """Export schedule to CSV file"""
        if not self.schedule:
            print("No schedule to export!")
            return
            
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['date', 'day_of_week', 'home_team', 'away_team', 'home_field', 'round']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for game in self.schedule:
                writer.writerow(game)
                
        print(f"Schedule exported to {filename}")
        
    def export_json(self, filename):
        """Export schedule to JSON file"""
        if not self.schedule:
            print("No schedule to export!")
            return
            
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.schedule, jsonfile, indent=2)
            
        print(f"Schedule exported to {filename}")
        
    def print_schedule(self):
        """Print the schedule in a readable format"""
        if not self.schedule:
            print("No schedule to display!")
            return
            
        print("\n" + "="*60)
        print("D1 SOFTBALL LEAGUE SCHEDULE")
        print("="*60)
        
        # Group by date
        current_date = None
        for game in sorted(self.schedule, key=lambda x: x['date']):
            if game['date'] != current_date:
                current_date = game['date']
                print(f"\n{game['day_of_week']}, {game['date']}")
                print("-" * 40)
            
            print(f"  {game['away_team']} @ {game['home_team']} ({game['home_field']})")
            
        print("\n" + "="*60)
        
    def get_team_schedule(self, team_name):
        """Get schedule for a specific team"""
        team_games = []
        for game in self.schedule:
            if game['home_team'] == team_name or game['away_team'] == team_name:
                team_games.append(game)
        return sorted(team_games, key=lambda x: x['date'])

def main():
    """Example usage of the scheduler"""
    scheduler = SoftballScheduler()
    
    # Add teams (example)
    teams = [
        "Red Sox", "Blue Jays", "Yankees", "Orioles", 
        "Rays", "White Sox", "Indians", "Tigers"
    ]
    
    for team in teams:
        scheduler.add_team(team)
    
    # Generate schedule
    print("Generating schedule...")
    success = scheduler.generate_schedule(
        games_per_team=12,
        start_date=datetime(2024, 4, 1),  # April 1, 2024
        avoid_dates=[
            datetime(2024, 5, 27),  # Memorial Day
            datetime(2024, 7, 4),   # Independence Day
        ],
        max_games_per_week=3
    )
    
    if success:
        scheduler.print_schedule()
        scheduler.export_csv("softball_schedule.csv")
        scheduler.export_json("softball_schedule.json")
        
        # Show schedule for a specific team
        print("\nRed Sox Schedule:")
        red_sox_games = scheduler.get_team_schedule("Red Sox")
        for game in red_sox_games:
            opponent = game['away_team'] if game['home_team'] == 'Red Sox' else game['home_team']
            home_away = "HOME" if game['home_team'] == 'Red Sox' else "AWAY"
            print(f"  {game['date']}: {opponent} ({home_away})")

if __name__ == "__main__":
    main() 