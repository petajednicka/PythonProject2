from data.database_manager import DatabaseManager
from core.tip_recommender import TipRecommender

db = DatabaseManager()
df = db.get_dataframe("Db_Fotbal_1.anglická liga.csv", reduced=False)

# Přehled, co budeme analyzovat
tip_variants = [
    ("odds_home", "home", "tipy_home.csv"),
    ("odds_draw", "draw", "tipy_draw.csv"),
    ("odds_away", "away", "tipy_away.csv")
]

for odds_col, result_type, output_filename in tip_variants:
    print(f"\n🔍 Analyzuji tip: {result_type.upper()} na základě {odds_col}")

    recommender = TipRecommender(df, odds_column=odds_col, target_result=result_type)

    best = recommender.find_best_interval(interval_range=range(3, 8))
    print("Nejlepší interval:")
    print(best)

    tips = recommender.recommend_tips()
    print(f"📌 Doporučeno zápasů: {len(tips)}")

    # Uložíme do CSV
    tips.to_csv(output_filename, index=False)
    print(f"💾 Uloženo do souboru: {output_filename}")


