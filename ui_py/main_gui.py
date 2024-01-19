# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/main_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(518, 160)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 10, 431, 100))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelCharacter = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelCharacter.sizePolicy().hasHeightForWidth())
        self.labelCharacter.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(48)
        self.labelCharacter.setFont(font)
        self.labelCharacter.setAcceptDrops(True)
        self.labelCharacter.setFrameShape(QtWidgets.QFrame.Panel)
        self.labelCharacter.setFrameShadow(QtWidgets.QFrame.Raised)
        self.labelCharacter.setScaledContents(True)
        self.labelCharacter.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCharacter.setWordWrap(False)
        self.labelCharacter.setObjectName("labelCharacter")
        self.horizontalLayout_4.addWidget(self.labelCharacter)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineRoman = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineRoman.setObjectName("lineRoman")
        self.horizontalLayout_2.addWidget(self.lineRoman)
        self.labelValidRoman = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelValidRoman.sizePolicy().hasHeightForWidth())
        self.labelValidRoman.setSizePolicy(sizePolicy)
        self.labelValidRoman.setMinimumSize(QtCore.QSize(50, 0))
        self.labelValidRoman.setFrameShape(QtWidgets.QFrame.Panel)
        self.labelValidRoman.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.labelValidRoman.setText("")
        self.labelValidRoman.setScaledContents(False)
        self.labelValidRoman.setObjectName("labelValidRoman")
        self.horizontalLayout_2.addWidget(self.labelValidRoman)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineTranslation = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineTranslation.setObjectName("lineTranslation")
        self.horizontalLayout_3.addWidget(self.lineTranslation)
        self.labelValidTranslation = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelValidTranslation.sizePolicy().hasHeightForWidth())
        self.labelValidTranslation.setSizePolicy(sizePolicy)
        self.labelValidTranslation.setMinimumSize(QtCore.QSize(50, 0))
        self.labelValidTranslation.setFrameShape(QtWidgets.QFrame.Panel)
        self.labelValidTranslation.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.labelValidTranslation.setText("")
        self.labelValidTranslation.setObjectName("labelValidTranslation")
        self.horizontalLayout_3.addWidget(self.labelValidTranslation)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnInvio = QtWidgets.QPushButton(self.layoutWidget)
        self.btnInvio.setAutoDefault(True)
        self.btnInvio.setDefault(True)
        self.btnInvio.setObjectName("btnInvio")
        self.horizontalLayout.addWidget(self.btnInvio)
        self.btnSkip = QtWidgets.QPushButton(self.layoutWidget)
        self.btnSkip.setAutoDefault(True)
        self.btnSkip.setObjectName("btnSkip")
        self.horizontalLayout.addWidget(self.btnSkip)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.checkBoxLunghe = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxLunghe.setGeometry(QtCore.QRect(440, 10, 71, 24))
        self.checkBoxLunghe.setObjectName("checkBoxLunghe")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.mainMenuBar = QtWidgets.QMenuBar(MainWindow)
        self.mainMenuBar.setGeometry(QtCore.QRect(0, 0, 518, 23))
        self.mainMenuBar.setDefaultUp(False)
        self.mainMenuBar.setObjectName("mainMenuBar")
        MainWindow.setMenuBar(self.mainMenuBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelCharacter.setText(_translate("MainWindow", "女"))
        self.lineRoman.setPlaceholderText(_translate("MainWindow", "romanization"))
        self.lineTranslation.setPlaceholderText(_translate("MainWindow", "translation"))
        self.btnInvio.setText(_translate("MainWindow", "Send"))
        self.btnSkip.setText(_translate("MainWindow", "Skip"))
        self.checkBoxLunghe.setText(_translate("MainWindow", "Longer"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
