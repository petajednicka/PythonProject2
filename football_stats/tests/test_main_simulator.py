from football_stats.core.simulator import Simulator
from pathlib import Path

database_folder = Path(__file__).resolve().parents[1] / "database"

sim = Simulator()
result = sim.simulate()
print(result)

# Volitelně uložit do CSV
result.to_csv(database_folder / "simulation_result.csv", index=False)

from football_stats.core.simulator import Simulator

sim = Simulator()
timeline = sim.simulate_weekly()
