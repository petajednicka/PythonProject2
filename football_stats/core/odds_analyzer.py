# cor/odds_analyzer.py
import pandas as pd
from football_stats.core.odds_intervals import OddsIntervals

class OddsAnalyzer:
    def __init__(self, df: pd.DataFrame, odds_column: str, target_result: str):
        self.df = df.copy()
        self.odds_column = odds_column
        self.target_result = target_result

    def analyze(self, number_of_intervals: int = 5, lower_bound: float = 1.0, upper_bound: float = 5.0) -> pd.DataFrame:
        intervals = OddsIntervals(number_of_intervals, lower_bound, upper_bound)

        # Přiřadíme ke každému zápasu index intervalu, do kterého spadá kurz
        self.df['interval_index'] = self.df[self.odds_column].apply(lambda x: intervals.find_index(x))

        summary = []
        for i, (low, high) in enumerate(intervals):
            interval_df = self.df[self.df['interval_index'] == i]
            total = len(interval_df)
            hits = (interval_df['result'] == self.target_result).sum()
            success_rate = round(hits / total * 100, 2) if total > 0 else 0.0
            avg_odds = interval_df[self.odds_column].mean()
            expected_value = round((avg_odds or 0) * (success_rate / 100), 2) if total > 0 else 0.0

            summary.append({
                'interval': f"{low:.2f}–{high:.2f}",
                'interval_index': i,
                'matches': total,
                'hits': hits,
                'success_rate (%)': success_rate,
                'average_odds': round(avg_odds, 2) if not pd.isna(avg_odds) else 0.0,
                'expected_value': expected_value
            })

        return pd.DataFrame(summary)

    def analyze_multiple(self, interval_range: range, lower_bound: float = 1.0, upper_bound: float = 5.0) -> pd.DataFrame:
        all_results = []
        for n_intervals in interval_range:
            result_df = self.analyze(n_intervals, lower_bound, upper_bound)
            result_df['interval_count'] = n_intervals
            all_results.append(result_df)

        return pd.concat(all_results, ignore_index=True)

    def best_interval_strategy(self, interval_range: range) -> pd.Series:
        all_results = self.analyze_multiple(interval_range)
        return all_results.sort_values(by="success_rate (%)", ascending=False).iloc[0]
