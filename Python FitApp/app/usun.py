
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
import time
import sys
from pymongo import MongoClient
import bcrypt


class Usun(QWidget):
    def __init__(self, konto, id_user):
        super().__init__()
        self.id_user = id_user
        self.konto = konto
        self.setStyleSheet(
            """
            QPushButton{
            background-color: rgba(125,125,125,0);
            }

            QLineEdit{
            background-color: rgba(255, 255, 255, 0); 
            color: black; 
            border:none
            }

            """
        )
        self.czc1 = QtGui.QFont()
        self.czc1.setPointSize(35)  
        self.setObjectName("self")
        self.resize(800, 500)
        self.setMinimumSize(QtCore.QSize(800, 500))
        self.setMaximumSize(QtCore.QSize(800, 500))
        self.Background = QtWidgets.QLabel(self)
        self.Background.setGeometry(QtCore.QRect(0, 0, 801, 501))
        self.Background.setText("")
        self.Background.setPixmap(QtGui.QPixmap("Background/UsuńKonto.png"))
        self.Background.setObjectName("Background")
        self.HasloInput = QtWidgets.QLineEdit(self)
        self.HasloInput.setGeometry(QtCore.QRect(210, 150, 381, 61))
        self.HasloInput.setObjectName("HasloInput")
        self.HasloInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.HasloInput.setFont(self.czc1)
        self.PowtorzHasloInput = QtWidgets.QLineEdit(self)
        self.PowtorzHasloInput.setGeometry(QtCore.QRect(210, 280, 381, 61))
        self.PowtorzHasloInput.setObjectName("PowtorzHasloInput")
        self.PowtorzHasloInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PowtorzHasloInput.setFont(self.czc1)
        self.ErrorLabel = QtWidgets.QLabel(self)
        self.ErrorLabel.setGeometry(QtCore.QRect(180, 20, 461, 91))
        self.ErrorLabel.setText("")
        self.ErrorLabel.setObjectName("ErrorLabel")
        self.ErrorLabel.setStyleSheet("color:red; font-size:35px;")
        self.ErrorLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.UsunKontoButton = QtWidgets.QPushButton(self)
        self.UsunKontoButton.setGeometry(QtCore.QRect(180, 370, 441, 71))
        self.UsunKontoButton.setText("")
        self.UsunKontoButton.setObjectName("UsunKontoButton")
        self.UsunKontoButton.clicked.connect(self.usun)
        self.XButton = QtWidgets.QPushButton(self)
        self.XButton.setGeometry(QtCore.QRect(752, 0, 41, 41))
        self.XButton.setText("")
        self.XButton.setObjectName("XButton")
        self.XButton.clicked.connect(self.closeEvent)


    def closeEvent(self,event):
        self.konto.overlay.deleteLater()
        self.konto.setEnabled(True)
        self.close()

    def usun(self):
        if len(self.HasloInput.text()) < 1 or len(self.PowtorzHasloInput.text()) < 1:
            self.ErrorLabel.setText("BRAKUJE DANYCH")
        
        elif self.HasloInput.text() != self.PowtorzHasloInput.text():
            self.ErrorLabel.setText("HASŁA SIĘ RÓŻNIĄ")
        
        else:
            self.client = MongoClient('localhost', 27017)
            self.db = self.client['Fitatu']
            self.collection = self.db['users']
            hashed_stare_input = self.HasloInput.text()
            hashed_stare = self.collection.find_one({"id_app":self.id_user})["haslo"]
            if bcrypt.checkpw(hashed_stare_input.encode(), hashed_stare):
                self.collection.delete_one({"id_app":self.id_user})
                col_name = "users_daily_"+str(self.id_user)
                if self.db.drop_collection(col_name):
                    self.ErrorLabel.setStyleSheet("color:green; font-size:35px;")
                    self.ErrorLabel.setText("KONTO ZOSTAŁO USUNIĘTE")
                    time.sleep(5)
                    sys.exit()
                    
            else:
                self.ErrorLabel.setText("HASŁO JEST NIEPOPRAWNE")



