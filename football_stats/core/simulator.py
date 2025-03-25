import pandas as pd
from pathlib import Path

class Simulator:
    def __init__(self, summary_path: str = "football_stats/database/tips_by_odds.csv", tips_folder: str = "football_stats/database/simulator", stake: float = 100.0):
        project_root = Path(__file__).resolve().parents[2]  # root = PythonProject2
        self.summary_path = project_root / summary_path
        self.tips_folder = project_root / tips_folder
        self.stake = stake

        print(f"👉 Očekávaná cesta k souhrnnému CSV: {self.summary_path}")

        if not self.summary_path.exists():
            raise FileNotFoundError(f"Soubor se souhrnem nenalezen: {self.summary_path}")

        self.summary_df = pd.read_csv(self.summary_path)



    def simulate(self) -> pd.DataFrame:
        results = []

        for _, row in self.summary_df.iterrows():
            league = row["league"]
            tip_type = row["tip_type"]
            odds_col = f"odds_{tip_type}"
            tips_file = self.tips_folder / f"tipy_{league}_{tip_type}.csv"

            if not tips_file.exists():
                print(f"⚠️ Soubor nenalezen: {tips_file}")
                continue

            tips_df = pd.read_csv(tips_file)
            if odds_col not in tips_df.columns:
                print(f"⚠️ Sloupec {odds_col} chybí v {tips_file}")
                continue

            total_bets = len(tips_df)
            wins = tips_df[tips_df["result"] == tip_type]
            losses = tips_df[tips_df["result"] != tip_type]

            win_count = len(wins)
            loss_count = len(losses)

            gain = (wins[odds_col] * self.stake).sum()
            loss = loss_count * self.stake
            profit = round(gain - loss, 2)
            roi = round(profit / (total_bets * self.stake) * 100, 2) if total_bets > 0 else 0.0

            results.append({
                "league": league,
                "tip_type": tip_type,
                "bets": total_bets,
                "wins": win_count,
                "losses": loss_count,
                "profit": profit,
                "roi (%)": roi
            })

        return pd.DataFrame(results)

    from pathlib import Path
    import pandas as pd

    def simulate_weekly(self, initial_bankroll: float = 5000.0, stake_fraction: float = 0.2):
        bankroll = initial_bankroll
        timeline = []

        # Načteme souhrnný report s očekávanou pravděpodobností
        summary = pd.read_csv(self.summary_path)

        # Najdeme všechny soubory se sázkami
        tip_files = list(self.tips_folder.glob("tipy_*.csv"))

        all_bets = []

        for tip_file in tip_files:
            df = pd.read_csv(tip_file)
            df["date"] = pd.to_datetime(df["date"])

            # Získáme název ligy a typ sázky ze jména souboru
            filename = tip_file.stem

            parts = filename.split("_")
            if len(parts) < 3:
                print(f"⚠️ Neočekávaný název souboru: {filename}")
                continue

            # Vezmeme vše kromě prvního a posledního jako název ligy
            league_name = "_".join(parts[1:-1])
            tip_type = parts[-1]

            # Najdeme odpovídající pravděpodobnost z reportu
            match = summary[(summary["league"] == league_name) & (summary["tip_type"] == tip_type)]

            if match.empty:
                print(f"⚠️ Nenalezena očekávaná pravděpodobnost pro {league_name} ({tip_type})")
                continue

            p = float(match.iloc[0]["success_rate"].strip(" %")) / 100

            df["league"] = league_name
            df["tip_type"] = tip_type
            df["p"] = p
            df["odds"] = df[f"odds_{tip_type}"]

            all_bets.append(df)

        if not all_bets:
            print("⚠️ Nebyly načteny žádné tipy pro simulaci.")
            return pd.DataFrame()

        df_bets = pd.concat(all_bets, ignore_index=True)

        def get_betting_week_start(dt: pd.Timestamp) -> pd.Timestamp:
            weekday = dt.weekday()
            delta_days = (weekday - 1) % 7  # úterý = 1
            return dt - pd.Timedelta(days=delta_days)

        df_bets["betting_week"] = df_bets["date"].apply(get_betting_week_start)
        df_bets = df_bets.sort_values(by="date").reset_index(drop=True)

        # Simulace po týdnech
        weekly_groups = df_bets.groupby("betting_week")

        for week, group in weekly_groups:
            num_bets = len(group)
            if num_bets == 0:
                continue

            total_weekly_stake = bankroll * stake_fraction
            stake_per_bet = total_weekly_stake / num_bets

            print(
                f"📅 Týden od {week.date()} | Bankroll: {bankroll:.2f} Kč | Sázky: {num_bets} | Vklad na zápas: {stake_per_bet:.2f} Kč")

            for _, row in group.iterrows():
                p = row["p"]
                o = row["odds"]
                r = row["result"]
                tip = row["tip_type"]

                edge = (p * (o - 1)) - (1 - p)
                f = edge / (o - 1) if (o - 1) != 0 else 0
                f = max(0, min(f, 1))

                bet_amount = stake_per_bet * f

                if r == tip:
                    profit = bet_amount * (o - 1)
                    bankroll += profit
                else:
                    bankroll -= bet_amount

            timeline.append({
                "week_start": week.date(),
                "bankroll": round(bankroll, 2),
                "num_bets": num_bets,
                "stake_per_bet": round(stake_per_bet, 2)
            })

        timeline_df = pd.DataFrame(timeline)
        total_profit = bankroll - initial_bankroll
        roi = round((total_profit / initial_bankroll) * 100, 2)

        print(f"\n✅ Konečný bankroll: {bankroll:.2f} Kč")
        print(f"💹 Zisk: {total_profit:.2f} Kč | ROI: {roi:.2f} %")

        # Uložení vývoje bankrollu
        timeline_df.to_csv(self.tips_folder / "bankroll_timeline.csv", index=False)

        return timeline_df