import csv
import dataclasses

from PyQt5.QtWidgets import QMainWindow

from chineseReminder import configs
from ui_py.sentences_gui import Ui_SentencesWindow_UI


@dataclasses.dataclass
class Sentence:
    italian: str
    expected_translation: str
    group_id: int


def import_sentences_db() -> dict[str, Sentence]:
    db = dict()
    with open(configs.APP_CONFIG.sentences_fpath, "r") as file:
        tsv = csv.reader(file, delimiter="\t")

        next(tsv, None)  # skip headers
        for group_id, italian, expected_translation in tsv:

            db[italian] = Sentence(
                italian=italian,
                expected_translation=expected_translation,
                group_id=group_id
            )

    return db



class SentencesWindow(QMainWindow, Ui_SentencesWindow_UI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # self.connectSignalsSlots()

        self.setWindowTitle("Chinese reminder - Sentences")

        self.db = import_sentences_db()
        self.sentences = list(self.db.keys())

        self.current_sentence: str = ""
        self.current_expected_translation: str = ""

        self.can_do_next = True

        # self.new_word()


    # def connectSignalsSlots(self):
    #     self.btnInvio.pressed.connect(self.invio)
    #
    #
    # def invio(self):
    #     if self.can_do_next:
    #         self.new_word()
    #         return
    #
    #     self.labelCharacter.setText(self.current_chinese)
    #     self.lineRoman.setText(self.current_roman)
    #     self.btnInvio.setText("Next")
    #
    #     self.can_do_next = True
    #
    #
    # def new_word(self):
    #     # aesthetic (pre)
    #     self.labelCharacter.clear()
    #     self.lineRoman.clear()
    #     self.btnInvio.setText("Send")
    #
    #     # internals
    #     self.can_do_next = False
    #
    #     # new char
    #     self.current_word = random.choice(self.words)
    #     self.current_roman, self.current_chinese = self.db_inv[self.current_word]
    #     self.labelWord.setText(self.current_word)
    #
    #     # aesthetic (post)
    #     self.btnInvio.setFocus()