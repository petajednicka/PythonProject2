import os
import pandas as pd
from pathlib import Path
from football_stats.data.csv_manager import CSVManager

class DatabaseManager:
    def __init__(self) -> None:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.input_dir = Path(project_root) / "Data_from_Trefik/DilciDb"
        self.reduced_dir = Path(project_root) / "Data_reduced"
        self.full_dir = Path(project_root) / "database"

        self.csv_manager = CSVManager()

    import os
    from pathlib import Path

    def update_database(self, force: bool = False) -> None:
        print("🔄 Kontroluji, které soubory je třeba aktualizovat...")

        self.reduced_dir.mkdir(parents=True, exist_ok=True)
        self.full_dir.mkdir(parents=True, exist_ok=True)

        for input_file in Path(self.input_dir).glob("*.csv"):
            filename = input_file.name
            reduced_file = self.reduced_dir / filename
            full_file = self.full_dir / filename

            # Kontrola, zda je třeba aktualizovat reduced verzi
            update_reduced = (
                    force or
                    not reduced_file.exists() or
                    os.path.getmtime(input_file) > os.path.getmtime(reduced_file)
            )

            # Kontrola, zda je třeba aktualizovat full verzi
            update_full = (
                    force or
                    not full_file.exists() or
                    os.path.getmtime(input_file) > os.path.getmtime(full_file)
            )

            if update_reduced:
                print(f"♻️ Aktualizuji REDUKOVANÝ soubor: {filename}")
                self.csv_manager.create_reduced_csv_files(
                    folder=self.input_dir,
                    output_folder=self.reduced_dir,
                    filenames=[filename]
                )
            else:
                print(f"✅ Soubor {filename} (reduced) je aktuální.")

            if update_full:
                print(f"♻️ Aktualizuji FULL soubor: {filename}")
                self.csv_manager.create_noreduced_csv_files(
                    folder=self.input_dir,
                    output_folder=self.full_dir,
                    filenames=[filename]
                )
            else:
                print(f"✅ Soubor {filename} (full) je aktuální.")

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