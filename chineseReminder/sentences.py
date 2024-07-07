import csv
import dataclasses

from PyQt5.QtWidgets import QMainWindow, QMessageBox

from chineseReminder import configs
from chineseReminder.utils import Statistics, CheckResult
from chineseReminder.ui_py.sentences_gui import Ui_SentencesWindow_UI

@dataclasses.dataclass
class SentenceCheck_Result(CheckResult):
    translation_correct: bool
    def is_correct(self) -> bool:
        return self.translation_correct


@dataclasses.dataclass
class Sentence:
    italian: str
    expected_translation: list[str]
    group_id: int

    def is_compatible_with(self, other: "Sentence") -> SentenceCheck_Result:
        # HACK: One of [self, other] will be the expected sentence (= may have more than 1 translation) while
        # the other will be the user-inputted sentence (= only 1 translation, of course). Since I don't want
        # to impose an un-enforceable calling order to `is_compatible_with`, we need to use
        # this ugly hack
        trans_self  = set([s.lower().strip() for s in self.expected_translation])
        trans_other = set([s.lower().strip() for s in other.expected_translation])
        return SentenceCheck_Result(
            trans_self.issubset(trans_other) or trans_other.issubset((trans_self))
        )

####################################################################

def import_sentences_db() -> dict[str, Sentence]:
    db = dict()
    with open(configs.APP_CONFIG.sentences_fpath, "r") as file:
        tsv = csv.reader(file, delimiter="\t")

        next(tsv, None)  # skip headers
        for group_id, italian, expected_translation in tsv:
            print(italian)
            db[italian] = Sentence(
                italian=italian,
                expected_translation=[et.strip() for et in expected_translation.split("//")],
                group_id=int(group_id)
            )

    return db

#####################################################################

class SentencesWindow(QMainWindow, Ui_SentencesWindow_UI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

        self.setWindowTitle("Chinese reminder - Sentences")

        try:
            self.stats = Statistics_Sentences(import_sentences_db())
        except FileNotFoundError:
            self.show_error_message_file_not_found()
            self.stats = Statistics_Sentences(dict())

        self.can_do_next = False

        self.new_character()

    def connectSignalsSlots(self):
        self.btnInvio.pressed.connect(self.invio)
        self.btnSkip.pressed.connect(self.skip)
        self.btnReveal.pressed.connect(self.reveal)

    ################### Interactions #######################

    def invio(self):
        """ When the user presses "Send" ... """
        if self.can_do_next:
            self.new_character()
            return

        user_inputted_sentence: Sentence = Sentence(
            italian = "",
            expected_translation = [self.lineChinese.text().strip().lower()],
            group_id = -1
        )

        if self.stats.check_given_answer(user_inputted_sentence).is_correct():
            self.labelValidTranslation.setText("Correct!")
            self.can_do_next = True
        else:
            self.labelValidTranslation.setText("Wrong!")

        self.statusbar.showMessage(str(self.stats))


    def skip(self):
        self.stats.skipped_answer()
        self.new_character()

    def reveal(self):
        self.lineChinese.setText(", ".join(self.stats.current_val.expected_translation))
        self.stats.wrong_answer()

    def new_character(self):
        # aesthetic (pre)
        self.lineChinese.clear()
        self.lineItalian.clear()
        self.labelValidTranslation.clear()

        # internals
        self.can_do_next = False
        self.stats.new_prompt()

        print(self.stats.current_val)
        self.lineItalian.setText(self.stats.current_val.italian)

        # aesthetic (post)
        self.lineChinese.setFocus()
        self.statusbar.showMessage(str(self.stats))

    def show_error_message_file_not_found(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f"No TSV (Tab Separated Values) dictionary file found at:")
        msg.setInformativeText(f"\n{configs.APP_CONFIG.sentences_fpath}\n\nThe program will likely fail.\n")
        msg.setWindowTitle("Error")
        msg.exec_()


class Statistics_Sentences(Statistics[str, Sentence]):
    def __init__(self, db: dict[str, Sentence]):
        super().__init__(db)

    # def check_given_answer(self, answer: Sentence) -> bool:
    #     return self.current_val.expected_translation == answer.expected_translation


