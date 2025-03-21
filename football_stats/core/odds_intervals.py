# core/odds_intervals.py

class OddsIntervals:
    def __init__(self, number_of_intervals=3, lower_bound=1.0, upper_bound=4.0):
        self.number_of_intervals = number_of_intervals
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.intervals = self._generate_intervals()

    def _generate_intervals(self):
        """Vytvoří seznam intervalů jako dvojice (od, do)."""
        step = (self.upper_bound - self.lower_bound) / self.number_of_intervals
        return [
            (round(self.lower_bound + i * step, 2), round(self.lower_bound + (i + 1) * step, 2))
            for i in range(self.number_of_intervals)
        ]

    def __iter__(self):
        return iter(self.intervals)

    def find_interval(self, value):
        """Vrátí první interval, do kterého hodnota patří (včetně spodní meze)."""
        for interval in self.intervals:
            if interval[0] <= value < interval[1]:
                return interval
        return None  # Pokud je mimo rozsah

    def find_index(self, value):
        """Vrátí index intervalu, do kterého daná hodnota spadá."""
        for i, (low, high) in enumerate(self.intervals):
            if low <= value < high:
                return i
        return None
