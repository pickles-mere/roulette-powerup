import random
from typing import List

from state import GameState, Bet
from display import show_round_status

# Turn this to True when running on a real computer with a screen.
USE_PYGAME_DISPLAY = False

RED = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
BLACK = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

def spin_wheel() -> int:
    return random.randint(0, 36)

def evaluate_bet(n: int, bet: Bet) -> int:
    if bet.kind == "number":
        return 36 * bet.amount if bet.selection == n else 0
    if n == 0:
        return 0
    if bet.kind == "red":
        return 2 * bet.amount if n in RED else 0
    if bet.kind == "black":
        return 2 * bet.amount if n in BLACK else 0
    if bet.kind == "odd":
        return 2 * bet.amount if n % 2 == 1 else 0
    if bet.kind == "even":
        return 2 * bet.amount if n % 2 == 0 else 0
    if bet.kind == "low":
        return 2 * bet.amount if 1 <= n <= 18 else 0
    if bet.kind == "high":
        return 2 * bet.amount if 19 <= n <= 36 else 0
    return 0

class GameController:
    def __init__(self, starting_balance: int):
        self.state = GameState(balance=starting_balance)

    def get_bets(self) -> List[Bet]:
        bets = []
        print("\n--- Place Bets ---")
        print(f"Balance: {self.state.balance}")
        print("Types: number, red, black, odd, even, low, high")

        while True:
            kind = input("Bet type (ENTER to stop): ").strip().lower()
            if kind == "":
                break
            if kind not in {"number","red","black","odd","even","low","high"}:
                print("Invalid type.")
                continue

            selection = None
            if kind == "number":
                try:
                    selection = int(input("Number 0–36: ").strip())
                except:
                    print("Invalid number.")
                    continue

            try:
                amount = int(input("Amount: ").strip())
            except:
                print("Invalid amount.")
                continue

            if not self.state.can_place_bet(amount):
                print("Bet not allowed.")
                continue

            bets.append(Bet(kind, selection, amount))

        return bets

    def run_round(self):
        if self.state.is_broke():
            print("You are out of money.")
            return None

        bets = self.get_bets()
        if not bets:
            print("No bets placed.")
            return None

        total_bet = sum(b.amount for b in bets)
        if total_bet > self.state.balance:
            print("Not enough balance.")
            return None

        spin = spin_wheel()
        print(f"\nWheel spins... {spin}")

        payout = sum(evaluate_bet(spin, b) for b in bets)
        result = self.state.apply_round_result(spin, bets, total_bet, payout)

        print(f"Bet: {total_bet}")
        print(f"Payout: {payout}")
        print(f"Net: {result.net_change}")
        print(f"Balance: {result.balance_after}")

        if USE_PYGAME_DISPLAY:
            show_round_status(result.balance_after, spin, result.net_change)

        return result

def main():
    print("=== Roulette ===")
    while True:
        start = input("Starting balance (or q): ").strip()
        if start.lower() == "q":
            return
        try:
            bal = int(start)
            if bal > 0:
                break
        except:
            pass
        print("Invalid amount.")

    game = GameController(bal)

    while True:
        if game.state.is_broke():
            print("You are broke.")
            break

        c = input("\nENTER = play, q = quit: ").strip().lower()
        if c == "q":
            print(f"You cash out with {game.state.balance}.")
            break

        game.run_round()

if __name__ == "__main__":
    main()
