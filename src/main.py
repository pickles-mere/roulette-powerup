import argparse
import random
from power import PowerManager, MultiplierX2, BonusRespins, ColorStreakBoost
from storage import HistoryLog
from analytics import analyze_results
import math
import time

class BetEvaluator:
    """Simple evaluator: returns base payout (stake * odds) and win/lose."""
    def evaluate(self, bet, spin_result):
        stake = bet.get('amount', 0)
        if bet['type'] == 'color':
            if spin_result['color'] == bet['choice']:
                return stake * 2, 'win'
            else:
                return 0, 'lose'
        elif bet['type'] == 'number':
            if spin_result['number'] == bet['choice']:
                return stake * 36, 'win'
            else:
                return 0, 'lose'
        else:
            return 0, 'lose'

class RouletteWheel:
    def __init__(self):

        self.slots = [{'number': i, 'color': 'green' if i==0 else ('red' if i%2==0 else 'black')} for i in range(37)]

    def spin(self):
        res = random.choice(self.slots)
        return res

def trigger_policy_every_n(n=5):
    return lambda idx, ctx: (idx % n == (n-1)) 

def trigger_policy_streak(streak_min=3):
    return lambda idx, ctx: ctx.get('streak', 0) >= streak_min

def cap_policy_max_multiplier(max_mult=3.0):
    def cap(mod, ctx):
        mult = mod.get('multiplier', 1.0)
        if mult > max_mult:
            mod['multiplier'] = max_mult
            mod['note'] = (mod.get('note','') + f' capped_to_{max_mult}')
        return mod
    return cap

def run_simulation(rounds=10000, seed=42, verbose=False, save_prefix="sim_report"):
    random.seed(seed)
    wheel = RouletteWheel()
    evaluator = BetEvaluator()
    log = HistoryLog(json_path=f"{save_prefix}.json", csv_path=f"{save_prefix}.csv", append=False)

    pm = PowerManager(trigger_policy=trigger_policy_every_n(5), cap_policy=cap_policy_max_multiplier(3.0))
    pm.add_rule(MultiplierX2(), weight=0.5)
    pm.add_rule(BonusRespins(respins=1), weight=0.3)
    pm.add_rule(ColorStreakBoost(streak_threshold=3, boost=1.75), weight=0.2)

    balance = 1000.0
    bet_amount = 10.0
    baseline_ev_samples = []

    streak_color = None
    streak_len = 0

    for i in range(rounds):
        bet = {'type': 'color', 'choice': 'red', 'amount': bet_amount}
        spin_res = wheel.spin()
        color = spin_res['color']
        if color == streak_color:
            streak_len += 1
        else:
            streak_color = color
            streak_len = 1

        context = {'round_index': i, 'streak': streak_len, 'color': color}

        base_payout, outcome = evaluator.evaluate(bet, spin_res)
        base_net = base_payout - bet_amount

        pm_context = {'streak': streak_len, 'color': color, 'result': outcome, 'base_payout': base_payout}
        mod = pm.maybe_apply(i, pm_context)
        multiplier = float(mod.get('multiplier', 1.0))
        extra_respins = int(mod.get('extra_respins', 0))

        final_payout = base_payout * multiplier if base_payout > 0 else 0.0
        final_net = final_payout - bet_amount

        if extra_respins > 0 and base_payout > 0:
            final_payout += base_payout * extra_respins
            final_net = final_payout - bet_amount

        balance += final_net

        event = {
            'round_index': i,
            'result': outcome,
            'number': spin_res.get('number'),
            'color': spin_res.get('color'),
            'bet_type': bet['type'],
            'bet_choice': bet['choice'],
            'stake': bet_amount,
            'base_payout': base_payout,
            'payout': final_payout,
            'net': final_net,
            'balance_after': balance,
            'power_active': str(mod.get('active', False)),
            'power_multiplier': mod.get('multiplier', 1.0),
            'power_extra_respins': mod.get('extra_respins', 0),
            'power_note': mod.get('note', ''),
            'power_rule': mod.get('rule_name', ''),
        }

        log.append(event)

        if verbose and i % 1000 == 0:
            print(f"Round {i}: outcome={outcome}, payout={final_payout:.2f}, balance={balance:.2f}")

        if balance <= 0 and i > 0:
            if verbose:
                print(f"Bankrupt at round {i}")
            break

    summary = analyze_results(log.csv_path, show_plots=True, save_prefix=save_prefix)
    print("SIM SUMMARY:", summary)
    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", "-s", type=int, default=0, help="simulate N rounds (CLI). If 0, runs a short demo.")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    if args.simulate and args.simulate > 0:
        run_simulation(rounds=args.simulate, verbose=args.verbose, save_prefix=f"sim_{int(time.time())}")
    else:
        run_simulation(rounds=100, verbose=True, save_prefix="demo")
