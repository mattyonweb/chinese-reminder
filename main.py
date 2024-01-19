import configs # Keep it first!

import csv
import sys
import random
import unicodedata
from typing import Any

from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QMenu
)

from ui_py.database_editor_gui import Ui_DatabaseEditor_UI
from ui_py.main_gui import Ui_MainWindow as Main_UI_MainWindow
from ui_py.secondary_gui import Ui_MainWindow as Secondary_UI_MainWindow
from utils import Statistics


def import_db() -> dict[str, tuple[str, list]]:
    """ Reads the database file into a dictionary of the form:
     {chinese_str: (romanization, translation)}
     """
    db = dict()

    with open(configs.APP_CONFIG.dictionary_fpath, "r") as file:
        tsv_file = csv.reader(file, delimiter="\t")

        for row in tsv_file:
            if len(row) == 0: # handle empty lines that may appear at end
                continue
            db[row[0].strip()] = (row[1].strip(), row[2].strip().split(","))

    return db


def inverse_db(db: dict[str, tuple[str, list]]) -> dict[str, tuple[str, str]]:
    """From the previously imported db/dictionary, invert the index so that you obtain:
    {translation: (romanization, chinese_str)}
    """
    d_out = dict()
    for chinese_char,(roman,trans) in db.items():
        for k_inv in trans:
            d_out[k_inv] = (roman, chinese_char)
    return d_out



DB = import_db()
DB_INV = inverse_db(DB)


################################################################à

class ChineseToItalianWindow(QMainWindow, Main_UI_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.dbWindow = DatabaseEditorWindow(self)
        self.secondaryWindow = ItalianToChineseWindow(self)

        self.connectSignalsSlots()
        self.setupMenuBar()

        self.setWindowTitle("Chinese reminder")

        self.db = DB
        self.chars = list(self.db.keys())

        self.current_expected = None
        self.can_do_next = True
        self.stats = Statistics()

        self.statusbar.showMessage(str(self.stats))

        self.new_character()


    def connectSignalsSlots(self):
        self.btnInvio.pressed.connect(self.invio)
        self.btnSkip.pressed.connect(self.skip)

    def setupMenuBar(self):
        # Setup "Database" main bar entry
        db_sub_menu = QMenu("Database", self)
        self.mainMenuBar.addMenu(db_sub_menu)

        openDbWindowAction = QAction("&Edit...", db_sub_menu)
        openDbWindowAction.triggered.connect(lambda: self.dbWindow.show())
        db_sub_menu.addAction(openDbWindowAction)

        # Setup "Inverse" main bar entry (inverse game)
        inv_sub_menu = QMenu("Inverse", self)
        self.mainMenuBar.addMenu(inv_sub_menu)

        openSecondaryWindowAction = QAction("&Open...", inv_sub_menu)
        openSecondaryWindowAction.triggered.connect(lambda: self.secondaryWindow.show())
        inv_sub_menu.addAction(openSecondaryWindowAction)


    def invio(self):
        if self.can_do_next:
            self.new_character()
            return

        can_do_next_local = True

        user_roman = self.lineRoman.text().strip().lower()
        user_trans = self.lineTranslation.text().strip().lower()

        real_roman, real_trans = self.current_expected

        if unicodedata.normalize("NFD", user_roman) != unicodedata.normalize("NFD", real_roman):
            self.labelValidRoman.setText("Wrong!")
            can_do_next_local = False
        else:
            self.labelValidRoman.setText("Correct!")


        if user_trans not in real_trans:
            self.labelValidTranslation.setText("Wrong!")
            can_do_next_local = False
        else:
            self.labelValidTranslation.setText("Correct!")


        if can_do_next_local:
            self.can_do_next = True
            self.stats.good_answer()
        else:
            self.stats.wrong_answer()


    def skip(self):
        self.stats.skipped_answer()
        self.new_character()

    def new_character(self):
        # aesthetic (pre)
        self.lineTranslation.clear()
        self.lineRoman.clear()
        self.labelValidRoman.clear()
        self.labelValidTranslation.clear()

        # internals
        self.can_do_next = False
        self.stats.new_prompt()

        # new char
        while not self.acceptable_next(key := random.choice(self.chars)):
            pass

        # key = random.choice(self.chars)
        self.current_expected = self.db[key]
        self.labelCharacter.setText(key)

        # aesthetic (post)
        self.lineRoman.setFocus()
        self.statusbar.showMessage(str(self.stats))

    def acceptable_next(self, chinese_char: str):
        if self.checkBoxLunghe.isChecked():
            return len(chinese_char) > 1
        return True


################################################################à
from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, Qt

class VocabularyModel(QAbstractTableModel):
    def __init__(self, *args, todos=None, **kwargs):
        self.data = [[k, roman, ",".join(trans)] for k,(roman,trans) in DB.items()]
        super(VocabularyModel, self).__init__(*args, **kwargs)

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    def headerData(self, section: int, orientation: Qt.Orientation, role=...):
        if role == QtCore.Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return "Chinese"
                if section == 1:
                    return "Pinyu"
                if section == 2:
                    return "Translation"
            else:
                return str(section)

    def columnCount(self, parent=None):
        return len(self.data[0])

    def rowCount(self, parent=None):
        return len(self.data)

    def data(self, index: QModelIndex, role=...) -> str:
        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
            row = index.row()
            col = index.column()
            return str(self.data[row][col])

    def setData(self, index: QModelIndex, value: Any, role=...) -> bool:
        if role == Qt.EditRole:
            if index.column() == 0:
                if value in [t[0] for t in self.data]:
                    return False

            self.data[index.row()][index.column()] = value
            return True


class DatabaseEditorWindow(QMainWindow, Ui_DatabaseEditor_UI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.populateDbWindow()

    def connectSignalsSlots(self):
        pass

    def populateDbWindow(self):
        vocMod = VocabularyModel()
        self.tableView.setModel(vocMod)


################################################################à

class ItalianToChineseWindow(QMainWindow, Secondary_UI_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

        self.setWindowTitle("Chinese reminder 2")

        self.db_inv = DB_INV
        self.words = list(self.db_inv.keys())

        self.current_word: str = ""
        self.current_roman: str = ""
        self.current_chinese: str = ""

        self.can_do_next = True

        self.new_word()



    def connectSignalsSlots(self):
        self.btnInvio.pressed.connect(self.invio)


    def invio(self):
        if self.can_do_next:
            self.new_word()
            return

        self.labelCharacter.setText(self.current_chinese)
        self.lineRoman.setText(self.current_roman)
        self.btnInvio.setText("Next")

        self.can_do_next = True


    def new_word(self):
        # aesthetic (pre)
        self.labelCharacter.clear()
        self.lineRoman.clear()
        self.btnInvio.setText("Send")

        # internals
        self.can_do_next = False

        # new char
        self.current_word = random.choice(self.words)
        self.current_roman, self.current_chinese = self.db_inv[self.current_word]
        self.labelWord.setText(self.current_word)

        # aesthetic (post)
        self.btnInvio.setFocus()


################################################################à

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ChineseToItalianWindow()
    # win = ItalianToChineseWindow()
    win.show()
    sys.exit(app.exec())
