
# Tento skript slouží k testování simulátoru fotbalového zápasu
# PythonProject2/football_stats/tests/test_run_simulator.py

from football_stats.core.simulator import Simulator

# Vytvoříme instanci simulátoru
sim = Simulator()

# Spustíme simulaci
result = sim.simulate()

# Výpis výsledku do konzole
print(result)
