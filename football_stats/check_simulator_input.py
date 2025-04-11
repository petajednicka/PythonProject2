
import os
import pandas as pd
from pathlib import Path

def check_simulator_input(directory):
    print(f"Kontroluji složku: {os.path.abspath(directory)}")
    try:
        files = os.listdir(directory)
        csv_files = [file for file in files if file.lower().endswith('.csv')]
        if csv_files:
            print(f"Nalezeno {len(csv_files)} CSV souborů v simulator_input:")
            for file in csv_files:
                print(f"- {file}")
        else:
            print("⚠️ Ve složce nejsou žádné CSV soubory.")
    except FileNotFoundError:
        print(f"⚠️ Složka {directory} nebyla nalezena.")
    except Exception as e:
        print(f"⚠️ Nastala chyba: {e}")

def check_tips_by_odds(file_path):
    print(f"\nKontroluji soubor: {os.path.abspath(file_path)}")
    try:
        df = pd.read_csv(file_path)
        if "expected_value" not in df.columns:
            print("⚠️ Sloupec 'expected_value' nebyl nalezen v souboru.")
            return

        invalid_rows = df[df["expected_value"] <= 1.3]

        if invalid_rows.empty:
            print("✅ Všechny hodnoty 'expected_value' jsou větší než 1.3.")
        else:
            print(f"⚠️ Nalezeno {len(invalid_rows)} řádků s 'expected_value' ≤ 1.3:")
            print(invalid_rows)
    except FileNotFoundError:
        print(f"⚠️ Soubor {file_path} nebyl nalezen.")
    except Exception as e:
        print(f"⚠️ Nastala chyba při kontrole souboru: {e}")

if __name__ == "__main__":
    base_folder = Path("database")
    simulator_input_folder = base_folder / "simulator_input"
    tips_by_odds_file = base_folder / "tips_by_odds.csv"

    check_simulator_input(simulator_input_folder)
    check_tips_by_odds(tips_by_odds_file)
