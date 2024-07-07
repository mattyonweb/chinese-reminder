import dataclasses
from math import atan
import random
from typing import *

@dataclasses.dataclass
class CheckResult:
    def is_correct(self) -> bool:
        return False

# =============================================================

K = TypeVar('K')
V = TypeVar('V')
class Statistics(Generic[K, V]):
    def __init__(self, db: dict[K, V]):
        self.prompts = 0
        self.sbagliati, self.skippati, self.giusti = 0, 0, 0

        # turn is ongoing when new user prompts are allowed
        self.turn_is_ongoing = True

        self.db: dict[K,V] = db
        self.keys: list[K] = list(db.keys())
        self.weights: list[float] = [1 / len(self.keys) for _ in self.keys]

        self.current_key: K = None
        self.current_val: V = None


    def __str__(self):
        return f"Prompts: {self.prompts} | Ok: {self.giusti} | Wrong: {self.sbagliati} | Skip: {self.skippati}"

    def new_prompt(self) -> tuple[K, V]:
        self.current_key, self.current_val = self.choose_new_prompt()
        self.turn_is_ongoing = True
        self.prompts += 1

        return self.current_key, self.current_val


    def choose_new_prompt(self) -> tuple[K,V]:
        while True:
            candidate_key: K   = random.choices(population=self.keys, weights=self.weights, k=1)[0]
            candidate_value: V = self.db[candidate_key]
            if self.is_acceptable_next_prompt(candidate_value):
                return candidate_key, candidate_value


    def penalized_probability(self, idx):
        """ New probability when the user guess was wrong. """
        return self.weights[idx] ** 0.5

    def bonusized_probability(self, idx):
        """ New probability when the user guess was right. """
        return atan(self.weights[idx]) / 2

    def update_weights(self, key: K, was_good_answer: bool):
        """ After a good/bad guess, update every probability accordingly. """
        idx = self.keys.index(key)

        if was_good_answer:
            new_probability = self.bonusized_probability(idx)
        else:
            new_probability = self.penalized_probability(idx)

        # I calcoli di seguito sono ben ragionati e non vanno toccati
        old_partial_sum = 1 - self.weights[idx]
        new_partial_sum = 1 - new_probability

        self.weights = [w * new_partial_sum / old_partial_sum for w in self.weights]
        self.weights[idx] = new_probability

        print(self.weights[idx])


    def check_given_answer(self, answer: V) -> CheckResult:
        check_result: CheckResult = self.current_val.is_compatible_with(answer)

        if check_result.is_correct():
            self.good_answer()
        else:
            self.wrong_answer()

        return check_result


    def wrong_answer(self):
        if self.turn_is_ongoing:
            self.sbagliati += 1
            self.turn_is_ongoing = False
            self.update_weights(self.current_key, was_good_answer=False)


    def good_answer(self):
        if self.turn_is_ongoing:
            self.giusti += 1
            self.turn_is_ongoing = False
            self.update_weights(self.current_key, was_good_answer=True)


    def skipped_answer(self):
        if self.turn_is_ongoing:
            self.skippati += 1
            self.turn_is_ongoing = False


    def is_acceptable_next_prompt(self, _candidate_value: V) -> bool:
        return True

    def reset(self):
        self.weights = [1 / len(self.keys) for _ in self.keys]
        self.skippati  = 0
        self.sbagliati = 0
        self.giusti    = 0
        self.prompts   = 0