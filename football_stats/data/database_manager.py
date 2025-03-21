#football_stats/data/
from .csv_manager import CSVManager
import os


class DatabaseManager:

    def __init__(self) -> None:
        # Zjistí cestu ke kořenovému adresáři projektu
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.input_dir = os.path.join(project_root, "Data_from_Trefik")
        self.output_dir = os.path.join(project_root, "Data_reduced")
        self.csv_manager  = CSVManager()
        self.csv_manager.create_reduced_csv_files(self.input_dir, self.output_dir)
        self.output_dir = os.path.join(project_root, "database")
        self.csv_manager.create_noreduced_csv_files(self.input_dir, self.output_dir)