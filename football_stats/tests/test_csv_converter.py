from football_stats.data.csv_converter import CSVConverterFromTXT
from pathlib import Path

def main():
    BASE_DIR = Path(__file__).resolve().parent.parent  # vrátí se o dvě úrovně nahoru z tests/

    konvertor = CSVConverterFromTXT(
        slozka_txt=BASE_DIR / "Data_from_Trefik" / "TXT_files_utf8" / "Kompletni",
        vystupni_slozka=BASE_DIR / "Data_from_Trefik" / "DilciDb",
        seznam_sportu=BASE_DIR / "Data_from_Trefik" / "seznam_sportu.txt",
        seznam_lig=BASE_DIR / "Data_from_Trefik" / "seznam_lig.txt"
    )

    konvertor.spustit()
    print (konvertor.ligy)

if __name__ == "__main__":
    main()
