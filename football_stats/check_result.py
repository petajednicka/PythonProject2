
import os
from pathlib import Path

def list_csv_files(directory):
    print(f"Kontroluji složku: {os.path.abspath(directory)}")
    try:
        files = os.listdir(directory)
        csv_files = [file for file in files if file.lower().endswith('.csv')]
        if csv_files:
            print(f"Nalezeno {len(csv_files)} CSV souborů v result:")
            for file in csv_files:
                print(f"- {file}")
        else:
            print("⚠️ Ve složce nejsou žádné CSV soubory.")
    except FileNotFoundError:
        print(f"⚠️ Složka {directory} nebyla nalezena.")
    except Exception as e:
        print(f"⚠️ Nastala chyba: {e}")

if __name__ == "__main__":
    target_folder = Path("result")
    list_csv_files(target_folder)
