# Description: Třída CSVManager pro zpracování CSV souborů.
import pandas as pd
from pathlib import Path


def df_adjustment(df: pd.DataFrame) -> pd.DataFrame:
    """Upraví DataFrame před uložením."""

    if {'Den', 'Mesic', 'Rok'}.issubset(df.columns):
        def convert_date(row):
            day = int(row['Den'])
            month = int(row['Mesic'])
            year = int(row['Rok'])

            if year < 50:  # Například do 49 je 2000+, jinak 1900+
                year += 2000
            else:
                year += 1900

            return f"{year:04d}-{month:02d}-{day:02d}"

        df['date'] = df.apply(convert_date, axis=1)
        df = df.drop(columns=['Den', 'Mesic', 'Rok'])

    rename_mapping = {
        'Sport': 'sport',
        'Soutez': 'league',
        'Tym1': 'home_team',
        'Tym2': 'away_team',
        'Skore1': 'home_score',
        'Skore2': 'away_score',
        'Kurz1': 'odds_home',
        'KurzX': 'odds_draw',
        'Kurz2': 'odds_away',
        'vysledek': 'result'
    }
    # Přejmenujeme sloupce dle zadání, pokud existují
    rename_mapping = {key: value for key, value in rename_mapping.items() if key in df.columns}
    df = df.rename(columns=rename_mapping)

    # Uspořádáme sloupce dle zadání
    ordered_cols = ['sport', 'league', 'date', 'home_team', 'away_team', 'home_score', 'away_score', 'odds_home',
                    'odds_draw', 'odds_away', 'result']
    df = df[[col for col in ordered_cols if col in df.columns]]

    # Nahrazení hodnot ve sloupci 'result'
    if 'result' in df.columns:
        df['result'] = df['result'].str.strip().replace({
            'Tym1': 'home',
            'Tym2': 'away',
            'Remiza': 'draw'
        })
        df.loc[~df['result'].isin(['home', 'away', 'draw']), 'result'] = 'unknown'


    for col in ['home_score', 'away_score']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()  # 🔹 Odstranění mezer kolem čísel
            df[col] = pd.to_numeric(df[col], errors='coerce')  # 🔹 Převod na čísla (NaN pokud chyba)
            df[col] = df[col].fillna(0).round().astype(
                int)  # 🔹 Nahrazení NaN nulou, zaokrouhlení a převod na `int`

    odds_columns = ['odds_home', 'odds_draw', 'odds_away']
    for col in odds_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '.', regex=False)  # 🔹 Změna čárky na tečku
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(1.00).round(
                2)  # 🔹 Převod na float, vyplnění NaN, zaokrouhlení

    return df


class CSVManager:

    def __init__(self) -> None:
        self.folder = None
        self.output_folder = None
        pass

    def list_csv_files(self) -> list[Path]:
        """Vrátí seznam cest k souborům ve složce jako `Path` objekty."""
        return [file for file in self.folder.glob("*.csv")]

    def load_csv(self, filename: str) -> pd.DataFrame:
        """
        Načte CSV soubor jako DataFrame.
        """
        file_path = Path('database') / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Soubor {file_path} neexistuje.")

        df = pd.read_csv(file_path)

        # Úklid typických problémů – strip, odstranění whitespace
        df.columns = df.columns.str.strip()

        # Pokud chceš volat rovnou úpravu:
        # df = self.df_adjustment(df)

        return df

    def create_reduced_csv_files(self, folder: str = 'Data_from_Trefik', output_folder: str = 'Data_reduced',
                                     filenames: list[str] = None) -> None:

        """Načte CSV soubory, provede úpravy a uloží redukované verze do `Data_reduced`."""

        self.folder = Path(folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True)

        # ⬇️ Nově: filtrujeme jen vybrané soubory, pokud jsou zadány
        if filenames:
            files = [self.folder / fname for fname in filenames]
        else:
            files = list(self.folder.glob("*.csv"))

        for file_path in self.list_csv_files():  # Iterujeme přes všechny CSV soubory
            try:
                df = pd.read_csv(file_path)  # Načtení CSV
                df = df_adjustment(df)  # Upravíme DataFrame pomocí df_adjustment()

                # Redukujeme sloupce na pouze ty důležité
                required_columns = ['date', 'home_team', 'away_team',
                                    'home_score', 'away_score', 'result']

                df = df[[col for col in required_columns if col in df.columns]]  # Vybereme jen existující sloupce

                # Uložíme upravený soubor do Data_reduced/
                output_path = self.output_folder / file_path.name
                df.to_csv(output_path, index=False)

                print(f"Redukovaný soubor uložen: {output_path}")
            except Exception as e:
                print(f"Chyba při zpracování souboru {file_path.name}: {e}")

    def create_noreduced_csv_files(self, folder:str='Data_from_Trefik', output_folder:str='database',filenames: list[str] = None):
        self.folder = Path(folder)
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(exist_ok=True) # Vytvoříme složku pro výstupní soubory
        # ⬇️ Nově: filtrujeme jen vybrané soubory, pokud jsou zadány
        if filenames:
            files = [self.folder / fname for fname in filenames]
        else:
            files = list(self.folder.glob("*.csv"))

        for file_path in self.list_csv_files():
            try:
                df = pd.read_csv(file_path)

                df = df_adjustment(df)  # 🔹 Upravíme DataFrame před uložením

                output_path = self.output_folder / file_path.name
                df.to_csv(output_path, index=False)
                print(f"Zpracován soubor: {file_path.name}")
            except Exception as e:
                print(f"Chyba při zpracování souboru {file_path.name}: {e}")





