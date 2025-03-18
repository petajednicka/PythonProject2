#football_stats/tests/

from football_stats.data.database_manager import DatabaseManager

test_db_manager = DatabaseManager()
print('test_db_manager.input_directory:')
print(test_db_manager.input_dir)
print('test_db_manager.output_directory:')
print(test_db_manager.output_dir)