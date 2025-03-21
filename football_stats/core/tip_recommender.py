from football_stats.core.odds_analyzer import OddsAnalyzer
import pandas as pd

class TipRecommender:
    def __init__(self, df: pd.DataFrame, odds_column: str, target_result: str):
        self.df = df.copy()
        self.odds_column = odds_column
        self.target_result = target_result
        self.best_config = None  # (interval_count, (lower, upper))

    def find_best_interval(self, interval_range: range, lower_bound: float = 1.0, upper_bound: float = 5.0) -> pd.Series:
        analyzer = OddsAnalyzer(self.df, self.odds_column, self.target_result)
        all_results = analyzer.analyze_multiple(interval_range, lower_bound, upper_bound)

        # Volitelně: můžeš filtrovat jen intervaly s dostatečným počtem zápasů
        all_results = all_results[all_results["matches"] >= 10]

        # Najdi interval s nejvyšší očekávanou hodnotou
        best_row = all_results.sort_values(by="expected_value", ascending=False).iloc[0]

        # Ulož nejlepší kombinaci pro další použití
        interval_str = best_row["interval"]
        lower, upper = map(float, interval_str.split("–"))
        self.best_config = (best_row["interval_count"], (lower, upper))

        return best_row

    def recommend_tips(self) -> pd.DataFrame:
        if not self.best_config:
            raise ValueError("Nejdříve zavolej find_best_interval()")

        interval_count, (low, high) = self.best_config

        filtered = self.df[
            (self.df[self.odds_column] >= low) &
            (self.df[self.odds_column] < high)
        ]

        # Pokud chceš zobrazit jen zápasy, kde výsledek odpovídá očekávanému tipu:
        # filtered = filtered[filtered['result'] == self.target_result]

        return filtered.reset_index(drop=True)
