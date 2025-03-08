# football_stats/
# We test the class Match in the file match.py

from football_stats.core.match import Match

def test_match():
    # An instance of the match class is created and the return value is tested.

    match = Match('2020-01-01', 'Home Team', 'Away Team', 1, 2, 'L')
    assert match.date == '2020-01-01'
    assert match.home_team == 'Home Team'
    assert match.away_team == 'Away Team'
    assert match.home_score == 1
    assert match.away_score == 2
    assert match.result == 'L'
    assert str(match) == 'Datum 2020-01-01 Home Team 1 - 2 Away Team Result: L'

print(test_match())


