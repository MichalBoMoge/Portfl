from PyQt5 import QtCore, QtGui, QtWidgets
from pymongo import MongoClient

class dodajPrzepis(QtWidgets.QWidget):
    def __init__(self,przepisy):
        super().__init__()
        self.przepisy = przepisy
        self.setObjectName("self")
        self.setStyleSheet(
            """
            QPushButton{
            background-color: rgba(0,0,0,0);
            }

            QTextEdit{
            background-color: rgba(255, 255, 255, 0); 
            color: black; 
            border:none
            }

            QLineEdit{
            background-color: rgba(255, 255, 255, 0); 
            color: black; 
            border:none
            }

            """
        )
        self.czc1 = QtGui.QFont()
        self.czc1.setPointSize(15)
        self.czc2 = QtGui.QFont()
        self.czc2.setPointSize(25)
        self.resize(900, 600)
        self.setMinimumSize(QtCore.QSize(900, 600))
        self.setMaximumSize(QtCore.QSize(900, 600))
        self.Background = QtWidgets.QLabel(self)
        self.Background.setGeometry(QtCore.QRect(0, 0, 901, 601))
        self.Background.setText("")
        self.Background.setPixmap(QtGui.QPixmap("Background/Dodawanie Przepisów.png"))
        self.Background.setObjectName("Background")
        self.NazwaPrzepisuInput = QtWidgets.QLineEdit(self)
        self.NazwaPrzepisuInput.setGeometry(QtCore.QRect(80, 80, 361, 41))
        self.NazwaPrzepisuInput.setObjectName("NazwaPrzepisuInput")
        self.NazwaPrzepisuInput.setFont(self.czc2)
        self.BialkoInput =  QtWidgets.QLineEdit(self)
        self.BialkoInput.setGeometry(QtCore.QRect(650, 52, 231, 16))
        self.BialkoInput.setObjectName("BialkoInput")
        self.BialkoInput.setFont(self.czc1)
        self.TluszczInput =  QtWidgets.QLineEdit(self)
        self.TluszczInput.setGeometry(QtCore.QRect(650, 79, 231, 16))
        self.TluszczInput.setObjectName("TluszczInput")
        self.TluszczInput.setFont(self.czc1)
        self.WegleInput =  QtWidgets.QLineEdit(self)
        self.WegleInput.setGeometry(QtCore.QRect(650, 105, 231, 16))
        self.WegleInput.setObjectName("WegleInput")
        self.WegleInput.setFont(self.czc1)
        self.KalorieInput =  QtWidgets.QLineEdit(self)
        self.KalorieInput.setGeometry(QtCore.QRect(650, 132, 231, 16))
        self.KalorieInput.setObjectName("KalorieInput")
        self.KalorieInput.setFont(self.czc1)
        self.XButton = QtWidgets.QPushButton(self)
        self.XButton.setGeometry(QtCore.QRect(850, 0, 41, 41))
        self.XButton.setText("")
        self.XButton.setObjectName("XButton")
        self.XButton.clicked.connect(self.closeEvent)
        self.TrescPrzepisuInput = QtWidgets.QTextEdit(self)
        self.TrescPrzepisuInput.setGeometry(QtCore.QRect(100, 190, 771, 341))
        self.TrescPrzepisuInput.setObjectName("TrescPrzepisuInput")
        self.TrescPrzepisuInput.setFont(self.czc1)
        self.DodajButton = QtWidgets.QPushButton(self)
        self.DodajButton.setGeometry(QtCore.QRect(330, 550, 251, 41))
        self.DodajButton.setText("")
        self.DodajButton.setObjectName("DodajButton")
        self.DodajButton.clicked.connect(self.dodaj)

    def closeEvent(self,event):
        self.przepisy.overlay.deleteLater()
        self.przepisy.setEnabled(True)
        self.close()

    def dodaj(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Fitatu']
        self.collection = self.db['przepisy']
        nazwa = self.NazwaPrzepisuInput.text()
        kalorie = self.KalorieInput.text()
        wegle = self.WegleInput.text()
        tluszcz = self.TluszczInput.text()
        bialko = self.BialkoInput.text()
        tresc = self.TrescPrzepisuInput.toPlainText()
        if kalorie.isnumeric() and wegle.isnumeric() and tluszcz.isnumeric() and bialko.isnumeric():
            if self.collection.insert_one({"nazwa":nazwa,"kalorie":int(kalorie),"weglowodany":int(wegle),
                                        "tluszcz":int(tluszcz),"bialko":int(bialko),"przepis":tresc}):
                self.client.close()
                self.przepisy.overlay.deleteLater()
                self.przepisy.setEnabled(True)
                self.close()
    