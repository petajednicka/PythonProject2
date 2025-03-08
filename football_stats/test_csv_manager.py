# football stats/
# The class CsvManager is tested in the file test_csv_manager.py

from data.csv_manager import CSVManager

csv_manager = CSVManager()

# List of available CSV files
csv_files = csv_manager.list_csv_files()
print("Available CSV files:", csv_files)

# If there are any CSV files, load the first one
if csv_files:
    data = csv_manager.load_csv(csv_files[0])
    print(f"{len(data)} rows retrieved from {csv_files[0]}")
