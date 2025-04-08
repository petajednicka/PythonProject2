from pathlib import Path

# Cesta ke složce s TXT soubory
txt_dir = Path("C:/Users/Petr/PycharmProjects/PythonProject2/football_stats/Data_from_Trefik/TXT_files_utf8/Kompletni")

print(f"📂 Kontroluji složku: {txt_dir}")

if not txt_dir.exists():
    print("❌ Složka neexistuje!")
else:
    txt_files = sorted(txt_dir.glob("*.txt"))
    if not txt_files:
        print("⚠️ Nenašly se žádné TXT soubory.")
    else:
        print(f"🧾 Nalezeno {len(txt_files)} souborů:")
        for file in txt_files:
            print("  📄", file.name)
