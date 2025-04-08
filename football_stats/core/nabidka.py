# core/nabidka.py
from pathlib import Path
import pandas as pd
from datetime import datetime


class Nabidka:
    def __init__(self, simulator_dir='database/simulator', result_dir='result'):
        project_root = Path(__file__).resolve().parent.parent  # ⬅️ jdeš do kořene projektu
        self.simulator_dir = project_root / simulator_dir
        self.result_dir = project_root / result_dir
        self.result_dir.mkdir(exist_ok=True)

    def create_an_offer(self, from_date=None):
        if from_date is None:
            from_date = datetime.today().strftime('%Y-%m-%d')
        elif isinstance(from_date, datetime):
            from_date = from_date.strftime('%Y-%m-%d')

        nabidka_df = pd.DataFrame()

        for file in self.simulator_dir.glob("*.csv"):
            print(f"📂 Kontroluji soubor: {file.name}")  # 👈 výpis názvu souboru
            try:
                df = pd.read_csv(file)
                if 'date' in df.columns:
                    # ✅ Porovnání jako stringy
                    df_filtered = df[df['date'] >= from_date]
                    nabidka_df = pd.concat([nabidka_df, df_filtered], ignore_index=True)
            except Exception as e:
                print(f"⚠️ Chyba při načítání souboru {file.name}: {e}")

        if not nabidka_df.empty:
            nabidka_df = nabidka_df.sort_values(by='date')
            output_filename = f"nabidka_{from_date}.csv"
            output_path = self.result_dir / output_filename
            nabidka_df.to_csv(output_path, index=False)
            print(f"✅ Nabídka uložena: {output_path}")
        else:
            print("⚠️ Žádná nabídka nesplňuje podmínku datumu.")
