from football_stats.core.engine import Engine

engine = Engine()
engine.start()

db = engine.get_db_manager()
df = db.get_dataframe("Db_Fotbal_1.belgická_liga.csv", reduced=True)
print(df.head())
