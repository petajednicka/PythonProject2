#football_stats/tests/

from football_stats.data.database_manager import DatabaseManager

test_db_manager = DatabaseManager()
print('input_dir:', test_db_manager.input_dir)
print('reduced_dir:', test_db_manager.reduced_dir)
print('full_dir:', test_db_manager.full_dir)

from football_stats.data.database_manager import DatabaseManager

dbm = DatabaseManager()
dbm.update_database()


