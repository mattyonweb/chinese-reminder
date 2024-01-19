from typing import *


class Statistics:
    def __init__(self):
        self.prompts = 0
        self.sbagliati, self.skippati, self.giusti = 0,0,0
        self.accept_new = True

    def __str__(self):
        return f"Prompts: {self.prompts} | Ok: {self.giusti} | Wrong: {self.sbagliati} | Skip: {self.skippati}"

    def new_prompt(self):
        self.accept_new = True
        self.prompts += 1

    def wrong_answer(self):
        if self.accept_new:
            self.sbagliati += 1
            self.accept_new = False

    def good_answer(self):
        if self.accept_new:
            self.giusti += 1
            self.accept_new = False

    def skipped_answer(self):
        if self.accept_new:
            self.skippati += 1
            self.accept_new = False
