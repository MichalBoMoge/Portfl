from PyQt5.QtWidgets import QLineEdit, QWidget, QPushButton, QLabel
from pymongo import MongoClient
import bcrypt
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import QFont

class Rejestracja(QWidget):
    def __init__(self, log_win):
        self.log_win = log_win
        super().__init__()
        self.setObjectName("self")
        self.resize(1920, 1080)
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setMaximumSize(QtCore.QSize(1920, 1080))
        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.label.setMinimumSize(QtCore.QSize(1280, 720))
        self.label.setMaximumSize(QtCore.QSize(1920, 1080))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Background/Rejestracja PCv5.png"))
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

        self.HasloInput2 = QLineEdit(self)
        self.HasloInput2.setGeometry(QtCore.QRect(680, 400, 551, 71))
        self.HasloInput2.setObjectName("HasloInput2")
        self.HasloInput2.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: black; border:none")
        self.HasloInput2.setFont(self.czc1)
        self.HasloInput2.setEchoMode(QLineEdit.Password)


        self.RejestracjaButton = QtWidgets.QPushButton(self)
        self.RejestracjaButton.setGeometry(QtCore.QRect(632, 737, 651, 91))
        self.RejestracjaButton.setText("")
        self.RejestracjaButton.setObjectName("RejestracjaButton")
        self.RejestracjaButton.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: black;")
        self.RejestracjaButton.clicked.connect(self.zarejestruj)


        self.PowrotButton = QtWidgets.QPushButton(self)
        self.PowrotButton.setGeometry(QtCore.QRect(632, 877, 651, 91))
        self.PowrotButton.setText("")
        self.PowrotButton.setObjectName("RejestracjaButton")
        self.PowrotButton.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: black;")
        self.PowrotButton.clicked.connect(self.powrot)
        
        self.ErrorLabel = QLabel(self)
        self.ErrorLabel.setGeometry(632,677,651,91)
        self.ErrorLabel.setStyleSheet("color: red; ")
        self.ErrorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.czc = QFont()
        self.czc.setPointSize(20)
        self.ErrorLabel.setFont(self.czc)

    def zarejestruj(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Fitatu']
        self.collection = self.db['users']
        find_id = self.collection.find_one(sort=[("id_app", -1)])
        if find_id is None:
            do_inputu = 1
        else:
            do_inputu = int(find_id["id_app"] + 1)
        inp_login = self.LoginInput.text()
        inp_passwd = self.HasloInput.text()
        inp_passwd2 = self.HasloInput2.text()

        if len(inp_login) == 0 | len(inp_passwd) == 0 | len(inp_passwd2) == 0:
            self.ErrorLabel.setText("NIE WYPEŁNIONO WSZYSTKICH PÓL")
        elif inp_passwd != inp_passwd2:
            self.ErrorLabel.setText("HASŁA NIE SĄ TAKIE SAME")
        elif self.collection.find_one({"login":inp_login}):
            self.ErrorLabel.setText("ISTNIEJE JUŻ UŻYTKOWNIK O TAKIM LOGINIE")

        else:
            
            salt = bcrypt.gensalt()
            hashed_passwd = bcrypt.hashpw(inp_passwd.encode(),salt)

            if(self.collection.insert_one({"id_app":do_inputu,"login":inp_login,"haslo":hashed_passwd,
                "cel_kcal":2000,"cel_wegle":200,"cel_tluszcz":80,"cel_bialko":120})):
                self.ErrorLabel.setStyleSheet("Color: green;")
                self.ErrorLabel.setText("POMYŚLNIE ZAREJESTROWANO")
                self.LoginInput.setText("")
                self.HasloInput.setText("")
                self.HasloInput2.setText("")
                self.client.close()
            
    def powrot(self):
        self.log_win.show()
        self.hide()