# football_stats/tests/test_nabidka.py
# football_stats/tests/test_nabidka.py

from football_stats.core.nabidka import Nabidka
from datetime import datetime, timedelta

def main():
    print("🔍 Spouštím test metody create_an_offer()...")

    # Vytvoříme instanci nabídky
    n = Nabidka()

    # Testujeme s dnešním datem
    dnes = datetime.today().strftime('%Y-%m-%d')
    n.create_an_offer(from_date=dnes)

    # Testujeme i zpětně o pár dní (pokud je potřeba více dat)
    vcera = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    n.create_an_offer(from_date=vcera)

    print("✅ Test metody create_an_offer() dokončen.")

if __name__ == "__main__":
    main()
