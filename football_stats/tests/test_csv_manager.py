# football stats/
import os
import shutil
import tempfile
import pandas as pd
import unittest

# Předpokládáme, že třída CSVManager je definována v souboru csv_manager.py
from football_stats.data.csv_manager import CSVManager


class TestCSVManagerModifications(unittest.TestCase):
    def setUp(self):
        # Vytvoření dočasných adresářů pro vstup a výstup
        self.test_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.test_dir, "Data_from_Trefik")
        self.output_dir = os.path.join(self.test_dir, "Data_reduced")
        os.makedirs(self.input_dir, exist_ok=True)

        # Vytvoření ukázkového CSV souboru s požadovanými sloupci a daty
        self.sample_csv_path = os.path.join(self.input_dir, "sample.csv")
        df = pd.DataFrame({
            "Sport": ["Football", "Basketball"],
            "Soutez": ["League", "Cup"],
            "Kurz1": [1.5, 2.0],
            "KurzX": [3.0, 3.5],
            "Kurz2": [4.5, 5.0],
            "Den": [1, 2],
            "Mesic": [5, 6],
            "Rok": [24, 24],  # dvojciferný zápis roku
            "Tym1": ["Team A", "Team B"],
            "Tym2": ["Team C", "Team D"],
            "Skore1": [2, 1],
            "Skore2": [1, 2],
            "vysledek": ["win", "loss"],
            "Goal": [3, 4]  # dodatečný sloupec, který by měl zůstat
        })
        df.to_csv(self.sample_csv_path, index=False)

    def tearDown(self):
        # Odstranění dočasných adresářů po skončení testu
        shutil.rmtree(self.test_dir)

    def test_create_reduced_csv_files(self):
        # Vytvoření instance CSVManager s dočasnými adresáři
        manager = CSVManager(input_directory=self.input_dir, output_directory=self.output_dir)
        manager.create_reduced_csv_files()

        # Kontrola existence výstupního souboru
        output_file = os.path.join(self.output_dir, "sample.csv")
        self.assertTrue(os.path.exists(output_file), "Výstupní CSV soubor nebyl vytvořen.")

        # Načtení zpracovaného CSV souboru
        df_reduced = pd.read_csv(output_file)

        # Kontrola, že nepotřebné sloupce již neexistují
        for col in ['Sport', 'Soutez', 'Kurz1', 'KurzX', 'Kurz2', 'Den', 'Mesic', 'Rok']:
            self.assertNotIn(col, df_reduced.columns, f"Sloupec '{col}' nebyl odstraněn.")

        # Kontrola, že byl vytvořen sloupec 'date' se správným formátem
        self.assertIn('date', df_reduced.columns, "Sloupec 'date' nebyl vytvořen.")
        expected_dates = ["2024-05-01", "2024-06-02"]
        self.assertListEqual(list(df_reduced['date']), expected_dates, "Hodnoty ve sloupci 'date' nejsou správné.")

        # Kontrola přejmenovaných sloupců
        rename_checks = {
            'home_team': "Tym1",
            'away_team': "Tym2",
            'home_score': "Skore1",
            'away_score': "Skore2",
            'result': "vysledek"
        }
        for new_name in rename_checks.keys():
            self.assertIn(new_name, df_reduced.columns, f"Sloupec '{new_name}' nebyl vytvořen přejmenováním.")

        # Kontrola zachování hodnot v přejmenovaných sloupcích
        # Původní data z testovacího CSV
        self.assertListEqual(list(df_reduced['home_team']), ["Team A", "Team B"], "Hodnoty v 'home_team' nesedí.")
        self.assertListEqual(list(df_reduced['away_team']), ["Team C", "Team D"], "Hodnoty v 'away_team' nesedí.")
        self.assertListEqual(list(df_reduced['home_score']), [2, 1], "Hodnoty v 'home_score' nesedí.")
        self.assertListEqual(list(df_reduced['away_score']), [1, 2], "Hodnoty v 'away_score' nesedí.")
        self.assertListEqual(list(df_reduced['result']), ["win", "loss"], "Hodnoty v 'result' nesedí.")

        # Kontrola, že dodatečný sloupec zůstal nezměněn
        self.assertIn('Goal', df_reduced.columns, "Sloupec 'Goal' by měl zůstat v CSV souboru.")
        self.assertListEqual(list(df_reduced['Goal']), [3, 4], "Hodnoty ve sloupci 'Goal' nesedí.")


if __name__ == "__main__":
    unittest.main()
