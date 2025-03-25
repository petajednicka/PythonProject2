from pathlib import Path
import pandas as pd
from data.database_manager import DatabaseManager
from core.tip_recommender import TipRecommender

# 🔧 Dynamicky určíme root projektu podle umístění souboru
project_root = Path(__file__).resolve().parents[1]
database_folder = project_root / "football_stats" / "database"
simulator_folder = database_folder / "simulator"
simulator_folder.mkdir(parents=True, exist_ok=True)


# ✅ Inicializace
db = DatabaseManager()
summary_rows = []

# ✅ Najdeme všechny CSV soubory v 'database/'
for csv_file in database_folder.glob("Db_*.csv"):
    league_name = csv_file.stem.replace("Db_", "")  # např. '1.anglická liga'
    df = pd.read_csv(csv_file)
    if "result" not in df.columns and "home_score" in df.columns and "away_score" in df.columns:
        def vypocitej_result(row):
            if row["home_score"] > row["away_score"]:
                return "home"
            elif row["home_score"] < row["away_score"]:
                return "away"
            else:
                return "draw"


        df["result"] = df.apply(vypocitej_result, axis=1)

    best_tip = None
    best_value = 0
    best_row = None
    best_tips_df = None

    for odds_col, result_type in [
        ("odds_home", "home"),
        ("odds_draw", "draw"),
        ("odds_away", "away")
    ]:
        recommender = TipRecommender(df, odds_column=odds_col, target_result=result_type)

        try:
            result = recommender.find_best_interval(interval_range=range(3, 8))
        except IndexError:
            continue

        if result["expected_value"] > best_value:
            best_value = result["expected_value"]
            best_tip = result_type
            best_row = result
            best_tips_df = recommender.recommend_tips()

    if best_row is not None:
        # ✅ Uložíme do složky pro simulátor
        output_filename = f"tipy_{league_name}_{best_tip}.csv"
        output_path = simulator_folder / output_filename
        best_tips_df.to_csv(output_path, index=False)
        print(f"💾 Uloženo: {output_path}")

        # ✅ Přidáme do souhrnu
        summary_rows.append({
            "league": league_name,
            "tip_type": best_tip,
            "interval": best_row["interval"],
            "expected_value": best_row["expected_value"],
            "success_rate": f"{best_row['success_rate (%)']} %",
            "matches": int(best_row["matches"])
        })
    else:
        print(f"⚠️ Liga {league_name}: žádný vhodný interval nenalezen.")

# ✅ Uložení souhrnu
if summary_rows:
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(database_folder / "tips_by_odds.csv", index=False)
    print("\n✅ Souhrnný report uložen do: database/tips_by_odds.csv")
else:
    print("\n⚠️ Nebyl nalezen žádný vhodný tip – souhrnný report nevytvořen.")





