# core/match.py

class Match:
    def __init__(self, date, home_team, away_team, home_score, away_score, result):

        self.date = date
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = home_score
        self.away_score = away_score
        self.result = result

    def __str__(self):
        return (
            f'Datum {self.date} {self.home_team} {self.home_score} - {self.away_score} {self.away_team} '
            f'Result: {self.result}')# core/match.py

