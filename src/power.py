from abc import ABC, abstractmethod
import random

class PowerRule(ABC):
    """Strategy base for power rules."""
    @abstractmethod
    def apply(self, round_context: dict) -> dict:
        """
        Given a round_context with keys:
            - 'base_payout' (float)
            - 'result' (e.g., 'win'/'lose' or number/color)
            - 'player_bet' (dict)
        Return a dict with modifications, e.g. {'multiplier': 2.0, 'extra_respins': 0}
        """
        pass

class MultiplierX2(PowerRule):
    def apply(self, round_context):
        return {'multiplier': 2.0, 'extra_respins': 0, 'note': 'x2'}

class BonusRespins(PowerRule):
    def __init__(self, respins=1):
        self.respins = respins
    def apply(self, round_context):
        return {'multiplier': 1.0, 'extra_respins': self.respins, 'note': f'{self.respins}_respins'}

class ColorStreakBoost(PowerRule):
    """Boost multiplier when color streak length >= threshold"""
    def __init__(self, streak_threshold=3, boost=1.5):
        self.threshold = streak_threshold
        self.boost = boost
    def apply(self, round_context):
        if round_context.get('streak', 0) >= self.threshold and round_context.get('color') is not None:
            return {'multiplier': self.boost, 'extra_respins': 0, 'note': f'streak_{self.threshold}'}
        return {'multiplier': 1.0, 'extra_respins': 0, 'note': 'no_streak'}

class PowerManager:
    def __init__(self, trigger_policy=None, cap_policy=None):
        """
        trigger_policy: function(round_index, context) -> bool
        cap_policy: function(modification_dict, context) -> modification_dict (enforce caps)
        """
        self.trigger_policy = trigger_policy or (lambda i, ctx: False)
        self.cap_policy = cap_policy or (lambda mod, ctx: mod)
        self.rules = []
        self.activated_count = 0

    def add_rule(self, rule, name=None, weight=1.0):
        self.rules.append({'rule': rule, 'name': name or rule.__class__.__name__, 'weight': weight})

    def choose_rule(self):
        total = sum(r['weight'] for r in self.rules)
        if total == 0:
            return None
        pick = random.random() * total
        cum = 0
        for r in self.rules:
            cum += r['weight']
            if pick <= cum:
                return r['rule']
        return self.rules[-1]['rule']

    def maybe_apply(self, round_index: int, context: dict) -> dict:
        """
        If trigger_policy says yes -> choose a rule, apply, enforce cap_policy and return modifications
        Otherwise return identity modification.
        """
        if self.trigger_policy(round_index, context):
            rule = self.choose_rule()
            if rule is None:
                return {'multiplier': 1.0, 'extra_respins': 0, 'active': False}
            modification = rule.apply(context)
            capped = self.cap_policy(modification, context)
            capped['active'] = True
            self.activated_count += 1
            capped['rule_name'] = rule.__class__.__name__
            return capped
        else:
            return {'multiplier': 1.0, 'extra_respins': 0, 'active': False}
