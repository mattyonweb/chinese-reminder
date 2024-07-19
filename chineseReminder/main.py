import chineseReminder.configs # Keep it first! Don't remove it!
import sys
from PyQt5.QtWidgets import QApplication
from chineseReminder.words_from_chinese import ChineseToItalianWindow

def run():
    app = QApplication(sys.argv)
    win = ChineseToItalianWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()






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





