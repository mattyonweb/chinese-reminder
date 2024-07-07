import csv
import dataclasses
import unicodedata
import logging
from typing import Callable, Any, Optional

from PyQt5.QtWidgets import (QMainWindow, QAction, QMenu, QMessageBox)

from chineseReminder import configs
from chineseReminder.sentences import SentencesWindow
from chineseReminder.ui_py.main_gui import Ui_MainWindow as Main_UI_MainWindow
from chineseReminder.utils import Statistics, CheckResult


@dataclasses.dataclass
class WordCheck_Result(CheckResult):
    translation_correct: bool
    pinyin_correct: bool

    def is_correct(self) -> bool:
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

        # HACK: One of [self, other] will be the expected word (= may have more than 1 translation) while
        # the other will be the user-inputted word (= only 1 translation, of course). Since I don't want
        # to impose an un-enforceable calling order to `is_compatible_with`, we need to use
        # this ugly hack
        w1_trans, w2_trans = set(self.translations), set(other.translations)

        return WordCheck_Result(
            translation_correct = w1_trans.issubset(w2_trans) or w2_trans.issubset(w1_trans),
            pinyin_correct = w1_pinyin == w2_pinyin,
        )


###################################################################

def import_db() -> dict[str, Word]:
    """ Reads the database file into a dictionary. """
    db = dict()

    with open(configs.APP_CONFIG.dictionary_fpath, "r") as file:
        tsv_file = csv.reader(file, delimiter="\t")

        next(tsv_file, None)  # skip header

        for row in tsv_file:
            if len(row) == 0: # handle empty lines that may appear at end
                continue

            logging.debug(row)
            chinese, pinyin, translations, difficulty = [x.strip() for x in row]

            db[chinese] = Word(
                chinese=chinese,
                pinyin=pinyin,
                translations=translations.split(","),
                difficulty=int(difficulty)
            )

    return db


# def inverse_db(examples: dict[str, Word]) -> dict[str, Word]:
#     """
#     From the previously imported examples/dictionary, invert the index so that you obtain:
#     {translation: (romanization, chinese_str)}
#     """
#     d_out = dict()
#
#     for chinese, word in examples.items():
#         for t in word.translations:
#             d_out[t] = word
#     return d_out


###################################################################


class ChineseToItalianWindow(QMainWindow, Main_UI_MainWindow):
    def __init__(self, db: Optional[dict]=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.sentencesWindow_obj = SentencesWindow

        self.connectSignalsSlots()
        self.setupMenuBar()

        try:
            self.stats: Statistics_Words = Statistics_Words(db if db is not None else import_db())
        except FileNotFoundError:
            self.stats: Statistics_Words = Statistics_Words(dict())
            self.show_error_message_file_not_found()

        self.can_do_next = True

        self.setWindowTitle("Chinese reminder")
        self.statusbar.showMessage(str(self.stats))

        self.setupDefaultValues()
        self.new_character()

    def setupDefaultValues(self):
        self.comboBoxLvl.addItems(["<=", "=", ">="])
        self.comboBoxLvl.setCurrentText("<=")
        self.stats.set_lvl_operator("<=")


    def connectSignalsSlots(self):
        self.btnInvio.pressed.connect(self.invio)
        self.btnSkip.pressed.connect(self.skip)
        self.btnReveal.pressed.connect(self.reveal)
        self.btnReset.pressed.connect(self.reset)

        self.spinBoxLvl.valueChanged.connect(self.update_max_lvl)
        self.comboBoxLvl.textActivated.connect(lambda op_str: self.stats.set_lvl_operator(op_str)) # lambda required

    def setupMenuBar(self):
        """
        Set up the upper menu bar.
        """
        # Setup "Sentences" main bar entry
        sentences_sub_menu = QMenu("Sentences", self)
        self.mainMenuBar.addMenu(sentences_sub_menu)

        openSentencesWindowAction = QAction("&Open...", sentences_sub_menu)
        openSentencesWindowAction.triggered.connect(lambda: self.sentencesWindow_obj(self).show())
        sentences_sub_menu.addAction(openSentencesWindowAction)


    ################### Interactions #######################

    def invio(self):
        """ When the user presses "Send" ... """
        if self.can_do_next:
            self.new_character()
            return

        user_inputted_word = Word(
            chinese = self.stats.current_val.chinese,
            pinyin  = self.lineRoman.text().strip().lower(),
            translations = [self.lineTranslation.text().strip().lower()],
            difficulty = -1 # meaningless but who cares!
        )

        check_result: WordCheck_Result = self.stats.check_given_answer(user_inputted_word)

        if not check_result.pinyin_correct:
            self.labelValidRoman.setText("Wrong!")
        else:
            self.labelValidRoman.setText("Correct!")

        if not check_result.translation_correct:
            self.labelValidTranslation.setText("Wrong!")
        else:
            self.labelValidTranslation.setText("Correct!")

        self.can_do_next = check_result.is_correct()


    def skip(self):
        self.stats.skipped_answer()
        self.new_character()

    def reveal(self):
        self.lineRoman.setText(self.stats.current_val.pinyin)
        self.lineTranslation.setText(", ".join(self.stats.current_val.translations))
        self.stats.wrong_answer()

    def reset(self):
        self.stats.reset()
        self.new_character()

    def update_max_lvl(self):
        self.stats.set_lvl(int(self.spinBoxLvl.value()))

    def new_character(self):
        # aesthetic (pre)
        self.lineTranslation.clear()
        self.lineRoman.clear()
        self.labelValidRoman.clear()
        self.labelValidTranslation.clear()

        # internals
        self.can_do_next = False
        self.stats.new_prompt()

        logging.debug(self.stats.current_val)
        html_text = ""
        for char in self.stats.current_val.chinese:
            html_text += f"<a href='https://en.wiktionary.org/wiki/{char}' style='color:black'>{char}</a>"
        self.labelCharacter.setText(html_text)

        # aesthetic (post)
        self.lineRoman.setFocus()
        self.statusbar.showMessage(str(self.stats))

    def show_error_message_file_not_found(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f"No TSV (Tab Separated Values) dictionary file found at:")
        msg.setInformativeText(f"\n{configs.APP_CONFIG.dictionary_fpath}\n\nThe program will likely fail.\n")
        msg.setWindowTitle("Error")
        msg.exec_()


####################################################################

class Statistics_Words(Statistics[str, Word]):
    def __init__(self, db: dict[str, Word]):
        super().__init__(db)
        self.lvl = 0
        self.lvl_operator: Callable[[Any, Any], bool] = lambda _,__: True

    def is_acceptable_next_prompt(self, candidate_value: Word) -> bool:
        return self.lvl_operator(candidate_value.difficulty, self.lvl)

    def set_lvl(self, lvl: int):
        self.lvl = lvl

    def set_lvl_operator(self, op_str: str):
        operators_translation: dict[str, callable] = {
            "<=": (lambda x, y: x <= y),
            "=": (lambda x, y: x == y),
            ">=": (lambda x, y: x >= y)
        }

        self.lvl_operator = operators_translation[op_str]