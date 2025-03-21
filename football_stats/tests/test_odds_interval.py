import unittest
from football_stats.core.odds_intervals import OddsIntervals

class TestOddsIntervals(unittest.TestCase):

    def test_generate_intervals_default(self):
        odds = OddsIntervals()  # Výchozí počet: 3, rozsah 1–4
        expected = [(1.0, 2.0), (2.0, 3.0), (3.0, 4.0)]
        self.assertEqual(odds.intervals, expected)

    def test_generate_intervals_custom(self):
        odds = OddsIntervals(number_of_intervals=4, lower_bound=1.0, upper_bound=5.0)
        expected = [(1.0, 2.0), (2.0, 3.0), (3.0, 4.0), (4.0, 5.0)]
        self.assertEqual(odds.intervals, expected)

    def test_find_interval(self):
        odds = OddsIntervals(number_of_intervals=3, lower_bound=1.0, upper_bound=4.0)
        self.assertEqual(odds.find_interval(1.5), (1.0, 2.0))
        self.assertEqual(odds.find_interval(3.99), (3.0, 4.0))
        self.assertIsNone(odds.find_interval(4.5))  # Mimo rozsah

    def test_iteration(self):
        odds = OddsIntervals(3, 1.0, 4.0)
        intervals = list(odds)
        expected = [(1.0, 2.0), (2.0, 3.0), (3.0, 4.0)]
        self.assertEqual(intervals, expected)

if __name__ == '__main__':
    unittest.main()
