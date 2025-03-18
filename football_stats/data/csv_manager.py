import os
import pandas as pd


class CSVManager:
    def __init__(self, input_directory: object = "Data_from_Trefik", output_directory: object = "Data_reduced") -> None:
        self.input_directory = input_directory
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def create_reduced_csv_files(self):
        columns_to_remove = ['Sport', 'Soutez', 'Kurz1', 'KurzX', 'Kurz2']

        for filename in os.listdir(self.input_directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(self.input_directory, filename)
                try:
                    df = pd.read_csv(file_path)

                    # Odstraníme nepotřebné sloupce
                    df = df.drop(columns=columns_to_remove, errors='ignore')

                    # Vytvoříme nový sloupec 'date' spojením sloupců 'Den', 'Mesic' a 'Rok'
                    # Upravíme rok (dvojciferné číslo) na čtyřciferný rok přičtením 2000
                    if {'Den', 'Mesic', 'Rok'}.issubset(df.columns):
                        def convert_date(row):
                            day = int(row['Den'])
                            month = int(row['Mesic'])
                            year = int(row['Rok'])
                            # Předpoklad: pokud je rok menší než 100, přičteme 2000
                            if year < 100:
                                year += 2000
                            return f"{year:04d}-{month:02d}-{day:02d}"

                        df['date'] = df.apply(convert_date, axis=1)
                        # Odstraníme původní sloupce Den, Mesic, Rok
                        df = df.drop(columns=['Den', 'Mesic', 'Rok'])

                    # Přejmenujeme sloupce dle zadání, pokud existují
                    rename_mapping = {
                        'Tym1': 'home_team',
                        'Tym2': 'away_team',
                        'Skore1': 'home_score',
                        'Skore2': 'away_score',
                        'vysledek': 'result'
                    }
                    df = df.rename(columns=rename_mapping)

                    # Úprava sloupce 'result', pokud existuje
                    if 'result' in df.columns:
                        df['result'] = df['result'].replace({
                            'Tym1': 'home_team',
                            'Tym2': 'away_team',
                            'Remiza': 'draw'
                        })
                    # Převod 'home_score' a 'away_score' na integer
                    for col in ['home_score', 'away_score']:
                        if col in df.columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')  # Převod na čísla (NaN pokud chyba)
                            df[col] = df[col].fillna(0).astype(int)  # Nahrazení NaN nulou a převod na int

                    # Uložíme zpracovaný DataFrame do nového souboru
                    output_path = os.path.join(self.output_directory, filename)
                    df.to_csv(output_path, index=False)

                    print(f"Zpracován soubor: {filename}")
                except Exception as e:
                    print(f"Chyba při zpracování souboru {filename}: {e}")



