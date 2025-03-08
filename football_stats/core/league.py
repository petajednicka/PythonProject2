#  core/league.py
from re import match
from football_stats.core.match import Match

class League:
    def __init__(self, name):
        self.name = name
        self.matches = []

    def add_match(self, match : Match):
        self.matches.append(match)

    def __str__(self):
        return f'{self.name}'

    def __len__(self):
        return len(self.matches)

    def __getitem__(self, item):
        return self.matches[item]

    def __iter__(self):
        return iter(self.matches)