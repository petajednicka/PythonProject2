from data.database_manager import DatabaseManager
from core.odds_analyzer import OddsAnalyzer

db_manager = DatabaseManager()
db_manager.update_database()

db = DatabaseManager()
df = db.get_dataframe("Db_Fotbal_1.anglická liga.csv", reduced=False)

print(df.columns)

analyzer = OddsAnalyzer(df, odds_column="odds_home", target_result="home")
results = analyzer.analyze_multiple(interval_range=range(3, 8))

print(results)
