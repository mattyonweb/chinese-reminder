import configs # Keep it first!

import csv
import sys
from typing import Any

from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QMenu
)

from chineseReminder.sentences import SentencesWindow
from ui_py.main_gui import Ui_MainWindow as Main_UI_MainWindow
from utils import Word, WordCheck_Result, Statistics_Words


def import_db() -> dict[str, Word]:
    """ Reads the database file into a dictionary. """
    db = dict()

    with open(configs.APP_CONFIG.dictionary_fpath, "r") as file:
        tsv_file = csv.reader(file, delimiter="\t")

        for row in tsv_file:
            if len(row) == 0: # handle empty lines that may appear at end
                continue

            print(row)
            chinese, pinyin, translations, difficulty = [x.strip() for x in row]

            db[chinese] = Word(
                chinese=chinese,
                pinyin=pinyin,
                translations=translations.split(","),
                difficulty=int(difficulty)
            )
            # db[row[0].strip()] = (row[1].strip(), row[2].strip().split(","))

    return db


def inverse_db(db: dict[str, Word]) -> dict[str, Word]:
    """From the previously imported db/dictionary, invert the index so that you obtain:
    {translation: (romanization, chinese_str)}
    """
    d_out = dict()

    for chinese, word in db.items():
        for t in word.translations:
            d_out[t] = word
    return d_out



DB = import_db()
DB_INV = inverse_db(DB)


################################################################à


class ChineseToItalianWindow(QMainWindow, Main_UI_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.sentencesWindow = SentencesWindow(self)

        self.connectSignalsSlots()
        self.setupMenuBar()

        self.stats = Statistics_Words(DB)

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
        openSentencesWindowAction.triggered.connect(lambda: self.sentencesWindow.show())
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

        print(self.stats.current_val)
        html_text = ""
        for char in self.stats.current_val.chinese:
            html_text += f"<a href='https://en.wiktionary.org/wiki/{char}' style='color:black'>{char}</a>"
        self.labelCharacter.setText(html_text)

        # aesthetic (post)
        self.lineRoman.setFocus()
        self.statusbar.showMessage(str(self.stats))




################################################################à
# from PyQt5 import QtCore
# from PyQt5.QtCore import QModelIndex, Qt
#
# class VocabularyModel(QAbstractTableModel):
#     def __init__(self, *args, todos=None, **kwargs):
#         self.data = [[k, roman, ",".join(trans)] for k,(roman,trans) in DB.items()]
#         super(VocabularyModel, self).__init__(*args, **kwargs)
#
#     def flags(self, index):
#         return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
#
#     def headerData(self, section: int, orientation: Qt.Orientation, role=...):
#         if role == QtCore.Qt.DisplayRole:
#             if orientation == Qt.Horizontal:
#                 if section == 0:
#                     return "Chinese"
#                 if section == 1:
#                     return "Pinyu"
#                 if section == 2:
#                     return "Translation"
#             else:
#                 return str(section)
#
#     def columnCount(self, parent=None):
#         return len(self.data[0])
#
#     def rowCount(self, parent=None):
#         return len(self.data)
#
#     def data(self, index: QModelIndex, role=...) -> str:
#         if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
#             row = index.row()
#             col = index.column()
#             return str(self.data[row][col])
#
#     def setData(self, index: QModelIndex, value: Any, role=...) -> bool:
#         if role == Qt.EditRole:
#             if index.column() == 0:
#                 if value in [t[0] for t in self.data]:
#                     return False
#
#             self.data[index.row()][index.column()] = value
#             return True


# class DatabaseEditorWindow(QMainWindow, Ui_DatabaseEditor_UI):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setupUi(self)
#         self.connectSignalsSlots()
#         self.populateDbWindow()
#
#     def connectSignalsSlots(self):
#         pass
#
#     def populateDbWindow(self):
#         vocMod = VocabularyModel()
#         self.tableView.setModel(vocMod)


################################################################à

def run():
    app = QApplication(sys.argv)
    win = ChineseToItalianWindow()
    # win = ItalianToChineseWindow()
    win.show()
    sys.exit(app.exec())


################################################################à

# class ItalianToChineseWindow(QMainWindow, Secondary_UI_MainWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setupUi(self)
#         self.connectSignalsSlots()
# 
#         self.setWindowTitle("Chinese reminder 2")
# 
#         self.db_inv = DB_INV
#         self.words = list(self.db_inv.keys())
# 
#         self.current_word: str = ""
#         self.current_roman: str = ""
#         self.current_chinese: str = ""
# 
#         self.can_do_next = True
# 
#         self.new_word()
# 
# 
# 
#     def connectSignalsSlots(self):
#         self.btnInvio.pressed.connect(self.invio)
# 
# 
#     def invio(self):
#         if self.can_do_next:
#             self.new_word()
#             return
# 
#         self.labelCharacter.setText(self.current_chinese)
#         self.lineRoman.setText(self.current_roman)
#         self.btnInvio.setText("Next")
# 
#         self.can_do_next = True
# 
# 
#     def new_word(self):
#         # aesthetic (pre)
#         self.labelCharacter.clear()
#         self.lineRoman.clear()
#         self.btnInvio.setText("Send")
# 
#         # internals
#         self.can_do_next = False
# 
#         # new char
#         self.current_word = random.choice(self.words)
#         self.current_roman, self.current_chinese = self.db_inv[self.current_word]
#         self.labelWord.setText(self.current_word)
# 
#         # aesthetic (post)
#         self.btnInvio.setFocus()




if __name__ == "__main__":
    run()
