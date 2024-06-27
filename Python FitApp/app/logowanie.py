
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import  QLineEdit, QWidget, QPushButton, QLabel
from pymongo import MongoClient
from Wykres import Wykres
from rejestracja import Rejestracja
from konto import Konto
from wyszukiwarka import Wyszukiwarka
import bcrypt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from przepisy import Przepisy

class SuperObiekt():
    def __init__(self, dane):
        self.dane =dane
        self.wykres = Wykres(dane=dane, superObj=self)
        self.konto = Konto(dane=dane,superObj = self)
        self.produkty = Wyszukiwarka(dane=dane,superObj=self)
        self.przepisy = Przepisy(superObj=self,dane=dane)

class Logowanie(QWidget):
    def __init__(self):
        self.rej = Rejestracja(log_win=self)
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Fitatu']
        self.collection = self.db['users']
        super().__init__()
        self.setObjectName("self")
        self.resize(1920, 1080)
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setMaximumSize(QtCore.QSize(1920, 1080))
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.label.setMinimumSize(QtCore.QSize(1280, 720))
        self.label.setMaximumSize(QtCore.QSize(1920, 1080))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Background/Logowanie PC4.png"))
        self.label.setObjectName("label")
        
        self.czc1 = QFont()
        self.czc1.setPointSize(35)
        self.LoginInput = QLineEdit(self)
        self.LoginInput.setGeometry(QtCore.QRect(680, 250, 551, 71))
        self.LoginInput.setObjectName("LoginInput")
        self.LoginInput.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: black; border:none")
        self.LoginInput.setFont(self.czc1)
        self.HasloInput = QLineEdit(self)
        self.HasloInput.setGeometry(QtCore.QRect(680, 550, 551, 71))
        self.HasloInput.setObjectName("HasloInput")
        self.HasloInput.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: black; border:none")
        self.HasloInput.setFont(self.czc1)
        self.HasloInput.setEchoMode(QLineEdit.Password)
        self.LogowanieButton = QPushButton(self)
        self.LogowanieButton.setGeometry(QtCore.QRect(632, 737, 651, 91))
        self.LogowanieButton.setText("")
        self.LogowanieButton.setObjectName("LogowanieButton")
        self.LogowanieButton.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: black;")
        self.LogowanieButton.clicked.connect(self.zaloguj)
        self.RejestracjaButton = QPushButton(self)
        self.RejestracjaButton.setGeometry(QtCore.QRect(632, 877, 651, 91))
        self.RejestracjaButton.setText("")
        self.RejestracjaButton.setObjectName("RejestracjaButton")
        self.RejestracjaButton.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: black;")
        self.RejestracjaButton.clicked.connect(self.okno_rejestracji)
        self.ErrorLabel = QLabel(self)
        self.ErrorLabel.setGeometry(632,677,551,91)
        self.ErrorLabel.setStyleSheet("color: red; ")
        self.ErrorLabel.setAlignment(Qt.AlignCenter)
        self.czc = QFont()
        self.czc.setPointSize(20)
        self.ErrorLabel.setFont(self.czc)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Logowanie", "Logowanie"))
   


    def okno_rejestracji(self):
        self.rej.show()
        self.hide()

    def zaloguj(self):
        login = self.LoginInput.text()
        passwd = self.HasloInput.text()
        if self.collection.find_one({"login":login}):
            hashed = self.collection.find_one({"login":login})["haslo"]
            if bcrypt.checkpw(passwd.encode(), hashed):
                dane = {"login":login,"id_user":self.collection.find_one({"login":login})["id_app"]}
                self.super = SuperObiekt(dane)
                self.super.wykres.show()
                self.client.close()
                self.hide()
        else:
            self.ErrorLabel.setText("BŁĘDNY LOGIN LUB HASŁO")


