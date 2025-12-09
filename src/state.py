from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Bet:
    kind: str
    selection: Optional[int]
    amount: int

@dataclass
class RoundResult:
    round_no: int
    spin_result: int
    bets: List[Bet]
    total_bet: int
    total_payout: int
    net_change: int
    balance_after: int

@dataclass
class GameState:
    balance: int
    round_no: int = 0
    history: List[RoundResult] = field(default_factory=list)
    table_min: int = 1
    table_max: int = 500

    def can_place_bet(self, amount: int) -> bool:
        return (
            self.table_min <= amount <= self.table_max
            and amount <= self.balance
        )

    def apply_round_result(self, spin_result: int, bets: List[Bet], total_bet: int, total_payout: int):
        self.round_no += 1
        net = total_payout - total_bet
        self.balance += net

        result = RoundResult(
            round_no=self.round_no,
            spin_result=spin_result,
            bets=bets,
            total_bet=total_bet,
            total_payout=total_payout,
            net_change=net,
            balance_after=self.balance,
        )
        self.history.append(result)
        return result

    def is_broke(self) -> bool:
        return self.balance <= 0
