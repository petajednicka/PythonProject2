import csv
from pathlib import Path

class CSVManager:

    def __init__(self, folder: str = "Data_from_Trefik"):
        self.folder = Path(folder)

    def list_csv_files(self) -> list[str]:
        """Returns a list of CSV files in a directory."""

        if not self.folder.exists():
            raise FileNotFoundError(f"Directory {self.folder} does not exist.")

        return [f.name for f in self.folder.glob("*.csv")]

    def load_csv(self, filename: str) -> list[dict]:
        """Loads a CSV file into the dictionary list."""

        file_path = self.folder / filename
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist.")

        with file_path.open(mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def save_csv(self, filename: str, data: list[dict], fieldnames: list[str]) -> None:
        """Saves data to a CSV file."""
        file_path = self.folder / filename
        with file_path.open(mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
