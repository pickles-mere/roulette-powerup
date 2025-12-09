import statistics
import matplotlib.pyplot as plt
import csv
from pathlib import Path

def analyze_results(csv_path, show_plots=True, save_prefix="report"):
    """
    Reads the CSV log, computes summary statistics and generates plots.
    Returns a summary dict.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    rounds = []
    payouts = []
    balances = []
    power_active = 0
    base_payouts = []

    with open(csv_path, newline='', encoding='utf-8') as cf:
        reader = csv.DictReader(cf)
        for row in reader:
            try:
                payout = float(row.get('payout', 0))
            except:
                payout = 0.0
            try:
                base = float(row.get('base_payout', payout))
            except:
                base = payout
            try:
                balance = float(row.get('balance_after', 0))
            except:
                balance = 0.0
            active = row.get('power_active', "").lower() in ("true", "1", "yes", "active")
            rounds.append(row)
            payouts.append(payout)
            base_payouts.append(base)
            balances.append(balance)
            if active:
                power_active += 1

    n = len(rounds)
    avg_payout = statistics.mean(payouts) if payouts else 0
    median_payout = statistics.median(payouts) if payouts else 0
    stdev_payout = statistics.pstdev(payouts) if payouts else 0
    ev = avg_payout
    power_pct = (power_active / n * 100) if n else 0

    summary = {
        'rounds': n,
        'avg_payout': avg_payout,
        'median_payout': median_payout,
        'stdev_payout': stdev_payout,
        'power_activation_pct': power_pct,
    }

    if show_plots and n > 0:
        outcomes = {}
        for r in rounds:
            key = r.get('result', 'unknown')
            outcomes[key] = outcomes.get(key, 0) + 1
        plt.figure()
        plt.bar(list(outcomes.keys()), list(outcomes.values()))
        plt.title("Outcome distribution")
        plt.xlabel("Result")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(f"{save_prefix}_outcomes.png")
        plt.close()

        plt.figure()
        plt.plot(balances)
        plt.title("Bankroll / Balance over time")
        plt.xlabel("Round index")
        plt.ylabel("Balance")
        plt.tight_layout()
        plt.savefig(f"{save_prefix}_balance.png")
        plt.close()

        plt.figure()
        plt.hist(payouts, bins=40)
        plt.title("Payout distribution")
        plt.xlabel("Payout")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig(f"{save_prefix}_payout_hist.png")
        plt.close()

    return summary
