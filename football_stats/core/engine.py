from football_stats.data.database_manager import DatabaseManager

class Engine:
    def __init__(self):
        self.db_manager = None
        self.ready = False

    def start(self):
        print("🧠 Inicializuji databázi...")
        self.db_manager = DatabaseManager()
        self.ready = True
        print("✅ Databáze připravena.")
        dbm = DatabaseManager()
        dbm.update_database(force=False)  # <- nutí přegenerování všech výstupů

    def get_db_manager(self):
        if not self.ready:
            raise RuntimeError("Engine nebyl spuštěn. Zavolej nejprve start().")
        return self.db_manager

    # Místo pro další funkce
    def spustit_simulaci(self):
        print("🚀 (Zde později spustíme simulaci)")
