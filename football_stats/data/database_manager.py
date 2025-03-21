import os
import pandas as pd
from pathlib import Path
from football_stats.data.csv_manager import CSVManager

class DatabaseManager:
    def __init__(self) -> None:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.input_dir = Path(project_root) / "Data_from_Trefik"
        self.reduced_dir = Path(project_root) / "Data_reduced"
        self.full_dir = Path(project_root) / "database"
        self.csv_manager = CSVManager()

    def update_database(self) -> None:
        self.reduced_dir.mkdir(exist_ok=True)
        self.full_dir.mkdir(exist_ok=True)

        for input_file in self.input_dir.glob("*.csv"):
            filename = input_file.name
            reduced_file = self.reduced_dir / filename
            full_file = self.full_dir / filename

            update_reduced = (
                not reduced_file.exists() or
                os.path.getmtime(input_file) > os.path.getmtime(reduced_file)
            )
            update_full = (
                not full_file.exists() or
                os.path.getmtime(input_file) > os.path.getmtime(full_file)
            )

            if update_reduced:
                print(f"🔁 Aktualizuji redukovaný soubor: {filename}")
                self.csv_manager.create_reduced_csv_files(
                    folder=str(self.input_dir),
                    output_folder=str(self.reduced_dir)
                )

            if update_full:
                print(f"🔁 Aktualizuji plný soubor: {filename}")
                self.csv_manager.create_noreduced_csv_files(
                    folder=str(self.input_dir),
                    output_folder=str(self.full_dir)
                )

            if not update_reduced and not update_full:
                print(f"✅ Soubor {filename} je aktuální.")

    def get_dataframe(self, filename: str, reduced: bool = True) -> pd.DataFrame:
        """
        Načte jeden připravený DataFrame ze složky 'database' nebo 'Data_reduced'.

        :param filename: název souboru (včetně .csv)
        :param reduced: True = použije 'Data_reduced', False = použije 'database'
        :return: DataFrame s daty
        """
        folder = self.reduced_dir if reduced else self.full_dir
        file_path = folder / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Soubor {file_path} neexistuje.")

        df = pd.read_csv(file_path)
        return df