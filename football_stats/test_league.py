# football_stats/
# We test the class League in the file league.py

from football_stats.core.league import League
from football_stats.core.match import Match

def test_league():
    # An instance of the league class is created and the return value is tested.
    match1 = Match('2020-01-01', 'Home Team', 'Away Team', 1, 2, 'L')
    match2 = Match('2020-01-02', 'Home Team', 'Away Team', 2, 2, 'D')

    league = League('Bundesliga')
    assert league.name == 'Bundesliga'
    assert len(league) == 0

    league.add_match(match1)
    assert len(league) == 1
    assert str(league) == 'Bundesliga'

    league.add_match(match2)
    assert len(league) == 2
    assert league.__getitem__(0) == match1
    assert league.__getitem__(1) == match2

    for i, match in enumerate(league):
        assert match == league.__getitem__(i)

    assert list(league.__iter__()) == [match1, match2]
    assert list(league.__iter__()) == list(iter(league.matches))

    print('All tests passed')

test_league()