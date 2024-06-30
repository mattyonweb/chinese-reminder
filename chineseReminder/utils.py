import dataclasses
from math import atan
import random
import unicodedata
from typing import *

@dataclasses.dataclass
class WordCheck_Result:
    translation_correct: bool
    pinyin_correct: bool

    def is_correct(self):
        return self.translation_correct and self.pinyin_correct

@dataclasses.dataclass
class Word:
    chinese: str
    pinyin: str
    translations: list[str]
    difficulty: int

    def is_compatible_with(self, other: "Word") -> WordCheck_Result:
        w1_chinese, w2_chinese = self.chinese.strip().lower(), other.chinese.strip().lower()
        assert w1_chinese == w2_chinese  # just a sanity check

        w1_pinyin = unicodedata.normalize("NFD", self.pinyin.strip().lower())
        w2_pinyin = unicodedata.normalize("NFD", other.pinyin.strip().lower())

        # One of [self, other] will be the expected word (= may have more than 1 translation) while
        # the other will be the user-inputted word (= only 1 translation, of course). Since I don't want
        # to impose an un-enforceable calling order to `is_compatible_with`, we need to use
        # this ugly hack
        w1_trans, w2_trans = set(self.translations), set(other.translations)

        return WordCheck_Result(
            translation_correct = w1_trans.issubset(w2_trans) or w2_trans.issubset(w1_trans),
            pinyin_correct = w1_pinyin == w2_pinyin,
        )

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
        return f"Prompts: {self.prompts} | Ok: {self.giusti} | Wrong: {self.sbagliati} | Skip: {self.skippati} | Sum: {sum(self.weights)}"

    def new_prompt(self) -> tuple[K, V]:
        # for k, v in zip(self.keys, self.weights):
        #     print(k, v)
        # print("=================================")

        self.current_key, self.current_val = self.choose_new_prompt()
        self.turn_is_ongoing = True
        self.prompts += 1

        return self.current_key, self.current_val


    def choose_new_prompt(self) -> V:
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

        # print(self.weights[idx])


    def check_given_answer(self, answer: V) -> WordCheck_Result:
        check_result: WordCheck_Result = self.current_val.is_compatible_with(answer)

        if check_result.pinyin_correct and check_result.translation_correct:
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


    def is_acceptable_next_prompt(self, candidate_value: V) -> bool:
        return True


# ==========================================================================
# ==========================================================================

OPERATORS_TRANSLATION: dict[str, callable] = {
    "<=" : (lambda x,y: x<=y),
    "=" : (lambda x,y: x==y),
    ">=" : (lambda x,y: x>=y)
}

class Statistics_Words(Statistics[str, Word]):
    def __init__(self, db: dict[str, Word]):
        super().__init__(db)
        self.lvl = 0
        self.lvl_operator: Callable[[Any, Any], bool] = lambda x,y: True

    def is_acceptable_next_prompt(self, candidate_value: Word) -> bool:
        return self.lvl_operator(candidate_value.difficulty, self.lvl)

    def set_lvl(self, lvl: int):
        self.lvl = lvl

    def set_lvl_operator(self, op_str: str):
        self.lvl_operator = OPERATORS_TRANSLATION[op_str]
