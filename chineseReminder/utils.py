import random
from typing import *


class Statistics:
    def __init__(self, keys: list[str]):
        self.prompts = 0
        self.sbagliati, self.skippati, self.giusti = 0,0,0
        self.accept_new = True

        self.keys: list[str] = keys
        self.weights: list[float] = [1 / len(self.keys) for _ in self.keys]
        self.current_key = None
        self.penalty_factor = 8
        self.bonus_factor = 0.9

    def __str__(self):
        return f"Prompts: {self.prompts} | Ok: {self.giusti} | Wrong: {self.sbagliati} | Skip: {self.skippati} | Sum: {sum(self.weights)}"

    def new_prompt(self) -> str:
        for k,v in zip(self.keys, self.weights):
            print(k,v)
        print("=================================")

        self.current_key = self.choose_new_prompt()
        self.accept_new = True
        self.prompts += 1

        return self.current_key

    def choose_new_prompt(self) -> str:
        return random.choices(population=self.keys, weights=self.weights, k=1)[0]

    def wrong_answer(self):
        if self.accept_new:
            self.sbagliati += 1
            self.accept_new = False

            idx = self.keys.index(self.current_key)
            self.weights = [w * (1 - self.penalty_factor / (len(self.keys)-1)) if i!=idx else w for i,w in enumerate(self.weights)]
            self.weights[idx] = 1 - (sum(self.weights) - self.weights[idx])

    def good_answer(self):
        if self.accept_new:
            self.giusti += 1
            self.accept_new = False

            idx = self.keys.index(self.current_key)
            self.weights = [w * (1 + self.bonus_factor / (len(self.keys)-1)) if i!=idx else w for i,w in enumerate(self.weights)]
            self.weights[idx] = 1 - (sum(self.weights) - self.weights[idx])

    def skipped_answer(self):
        if self.accept_new:
            self.skippati += 1
            self.accept_new = False
