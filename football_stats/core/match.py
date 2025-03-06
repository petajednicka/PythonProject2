# core/match.py

class Match:
    def __init__(self, home_team, away_team, home_score, away_score):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score

    def __str__(self):
        return f"{self.home_team} {self.home_score} - {self.away_score} {self.away_team}"# core/match.py

