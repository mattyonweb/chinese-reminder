# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/database_editor_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DatabaseEditor_UI(object):
    def setupUi(self, DatabaseEditor_UI):
        DatabaseEditor_UI.setObjectName("DatabaseEditor_UI")
        DatabaseEditor_UI.resize(445, 240)
        self.centralwidget = QtWidgets.QWidget(DatabaseEditor_UI)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 10, 441, 228))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = QtWidgets.QTableView(self.widget)
        self.tableView.setSortingEnabled(True)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnReset = QtWidgets.QPushButton(self.widget)
        self.btnReset.setObjectName("btnReset")
        self.horizontalLayout.addWidget(self.btnReset)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        DatabaseEditor_UI.setCentralWidget(self.centralwidget)

        self.retranslateUi(DatabaseEditor_UI)
        self.pushButton_2.released.connect(DatabaseEditor_UI.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DatabaseEditor_UI)

    def retranslateUi(self, DatabaseEditor_UI):
        _translate = QtCore.QCoreApplication.translate
        DatabaseEditor_UI.setWindowTitle(_translate("DatabaseEditor_UI", "Database Editor"))
        self.btnReset.setText(_translate("DatabaseEditor_UI", "Reset"))
        self.pushButton_3.setText(_translate("DatabaseEditor_UI", "Save"))
        self.pushButton_2.setText(_translate("DatabaseEditor_UI", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DatabaseEditor_UI = QtWidgets.QMainWindow()
    ui = Ui_DatabaseEditor_UI()
    ui.setupUi(DatabaseEditor_UI)
    DatabaseEditor_UI.show()
    sys.exit(app.exec_())
