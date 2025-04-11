from pathlib import Path
import pandas as pd
import shutil


class CSVConverterFromTXT:
    def __init__(self, slozka_txt: str, vystupni_slozka: str, seznam_sportu: str, seznam_lig: str):
        self.slozka_txt = Path(slozka_txt)
        print(f"📂 TXT složka: {self.slozka_txt}")
        self.vystupni_slozka = Path(vystupni_slozka)
        print(f"📤 Výstupní složka: {self.vystupni_slozka}")

        # 🧹 Mazání staré složky
        if self.vystupni_slozka.exists():
            print(f"🧹 Mažu starou složku: {self.vystupni_slozka}")
            shutil.rmtree(self.vystupni_slozka)

        self.seznam_sportu_path = Path(seznam_sportu)
        self.seznam_lig_path = Path(seznam_lig)

        self.vystupni_slozka.mkdir(parents=True, exist_ok=True)

        self.sporty = self._nacti_seznam(self.seznam_sportu_path)
        self.ligy = self._nacti_seznam(self.seznam_lig_path)
        print(self.ligy)

    def _nacti_seznam(self, cesta: Path) -> list:
        if not cesta.exists():
            print(f"⚠️ Soubor {cesta} neexistuje.")
            return []
        with open(cesta, "r", encoding="utf-8") as f:
            return [radek.strip() for radek in f if radek.strip()]

    def spustit(self):
        print(f"📂 TXT složka: {self.slozka_txt}")
        print(f"📤 Výstupní složka: {self.vystupni_slozka}")
        print(f"📄 Sporty: {self.sporty}")
        print(f"📄 Ligy: {self.ligy}")

        self.txt_soubory = sorted(self.slozka_txt.glob("*.txt"), key=lambda f: f.name)
        print(f"🧾 Nalezeno {len(self.txt_soubory)} TXT souborů k načtení.")

        df = self.spoj_vsechny_txt_soubory()
        df = self.odstran_duplikaty_a_nehrano(df)
        self.uloz_do_souboru_podle_lig(df)

        df = self.spoj_vsechny_txt_soubory()
        if df.empty:
            print("⚠️ Žádné zápasy nejsou k dispozici pro výpis lig.")
        else:
            print("👀 Záznamy podle lig:")
            print(df["Soutez"].value_counts())

    def zpracuj_txt_soubor(self, file_path: Path) -> list[dict]:
        zaznamy = []
        aktualni_sport = ""
        aktualni_soutez = ""

        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    # Rozpoznání hlavičky
                    if " / " in line:
                        parts = [p.strip() for p in line.split(" / ", 1)]
                        if len(parts) == 2:
                            sport, liga = parts
                            if sport in self.sporty and liga in self.ligy:
                                aktualni_sport = sport
                                aktualni_soutez = liga
                                print(f"✅ Hlavička rozpoznána: {sport} / {liga}")
                            else:
                                print(f"⚠️ Nepodporovaná soutěž: {sport} / {liga}")
                                aktualni_sport = None
                                aktualni_soutez = None
                        continue

                    # Přeskakujeme, pokud není aktivní soutěž
                    if not aktualni_sport or not aktualni_soutez:
                        continue

                    # Rozpoznání zápasu
                    elif aktualni_sport and aktualni_soutez:
                        try:
                            datum = line[0:16].strip()
                            den, mesic, rok = datum.split('.')
                            tym1 = line[16:56].strip().replace(' ', '_')
                            tym2 = line[56:96].strip().replace(' ', '_')
                            skore1 = line[96:104].strip()
                            skore2 = line[104:112].strip()
                            kurz1 = line[112:124].strip()
                            kurzX = line[124:136].strip()
                            kurz2 = line[136:].strip()

                            zaznam = {
                                "Sport": aktualni_sport,
                                "Soutez": aktualni_soutez,
                                "Den": den,
                                "Mesic": mesic,
                                "Rok": rok,
                                "Tym1": tym1,
                                "Tym2": tym2,
                                "Skore1": skore1,
                                "Skore2": skore2,
                                "Kurz1": kurz1,
                                "KurzX": kurzX,
                                "Kurz2": kurz2,
                            }
                            zaznamy.append(zaznam)
                        except Exception as e:
                            print(f"⚠️ Chyba při zpracování řádku: {line}\n   {e}")

                    else:
                        print(f"⚠️ Přeskočen řádek ({len(parts)} částí): {line}")

                        zaznamy.append(zaznam)

        except Exception as e:
            print(f"❌ Chyba při načítání souboru {file_path.name}: {e}")


        return zaznamy



    def odstran_duplikaty_a_nehrano(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'vysledek' not in df.columns:
            print("⚠️ Ve vstupním DataFrame chybí sloupec 'vysledek'.")
            return df

        df['vysledek_rank'] = df['vysledek'].apply(
            lambda v: 1 if v in ['1', '0', '2'] else 2
        )

        df = df.sort_values(by=["datum", "liga", "domaci", "hoste", "vysledek_rank"])
        df = df.drop_duplicates(subset=["datum", "liga", "domaci", "hoste"], keep="first")
        df = df.drop(columns=["vysledek_rank"])
        return df

    def uloz_do_souboru_podle_lig(self, df: pd.DataFrame):
        if df.empty:
            print("⚠️ DataFrame je prázdný, není co ukládat.")
            return

        grouped = df.groupby(["Sport", "Soutez"])

        for (sport, soutez), skupina in grouped:
            filename = f"Db_{sport}_{soutez}.csv".replace(" ", "_")
            output_path = self.vystupni_slozka / filename
            skupina.to_csv(output_path, index=False, encoding="utf-8-sig")
            print(f"💾 Uloženo do: {output_path.name}")

    def spoj_vsechny_txt_soubory(self) -> pd.DataFrame:
        cache = {}
        txt_soubory = sorted(self.slozka_txt.glob("komplet_*.txt"), key=lambda f: f.name)
        print(f"🧾 Nalezeno {len(txt_soubory)} souborů k načtení.")

        for file in txt_soubory:
            print(f"📥 Zpracovávám soubor: {file.name}")
            zaznamy = self.zpracuj_txt_soubor(file)

            for zaznam in zaznamy:
                try:
                    klic = f"{zaznam['Rok']}-{zaznam['Mesic']}-{zaznam['Den']}-{zaznam['Tym1']}-{zaznam['Tym2']}"
                    cache[klic] = zaznam
                except KeyError as e:
                    print(f"⚠️ Chybějící sloupec v souboru {file.name}: {e}")
                    continue

        df = pd.DataFrame(cache.values())
        print(f"✅ Výsledný počet zápasů: {len(df)}")
        return df
