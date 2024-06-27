from PyQt5 import QtCore, QtGui, QtWidgets
import bcrypt
from pymongo import MongoClient

class Haslo(QtWidgets.QWidget):
    def __init__(self, konto, id_user):
        super().__init__()
        self.id_user = id_user
        self.konto = konto
        self.setStyleSheet(
            """
            QPushButton{
            background-color: rgba(0,0,0,0);
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
        self.Background.setGeometry(QtCore.QRect(0, 0, 800, 500))
        self.Background.setMinimumSize(QtCore.QSize(800, 500))
        self.Background.setMaximumSize(QtCore.QSize(800, 500))
        self.Background.setText("")
        self.Background.setPixmap(QtGui.QPixmap("Background/ZmianaHasła.png"))
        self.Background.setObjectName("Background")
        self.XButton = QtWidgets.QPushButton(self)
        self.XButton.setGeometry(QtCore.QRect(750, 0, 41, 41))
        self.XButton.setText("")
        self.XButton.setObjectName("XButton")
        self.XButton.clicked.connect(self.closeEvent)
        self.ZmienHasloButton = QtWidgets.QPushButton(self)
        self.ZmienHasloButton.setGeometry(QtCore.QRect(180, 420, 441, 70))
        self.ZmienHasloButton.setText("")
        self.ZmienHasloButton.setObjectName("ZmienHasloButton")
        self.ZmienHasloButton.clicked.connect(self.zmien)
        self.PowtorzHasloInput = QtWidgets.QLineEdit(self)
        self.PowtorzHasloInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PowtorzHasloInput.setGeometry(QtCore.QRect(210, 335, 381, 70))
        self.PowtorzHasloInput.setObjectName("PowtorzHasloInput")
        self.PowtorzHasloInput.setFont(self.czc1)
        self.NoweHasloInput = QtWidgets.QLineEdit(self)
        self.NoweHasloInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.NoweHasloInput.setGeometry(QtCore.QRect(210, 225, 381, 70))
        self.NoweHasloInput.setObjectName("NoweHasloInput")
        self.NoweHasloInput.setFont(self.czc1)
        self.StareHasloInput = QtWidgets.QLineEdit(self)
        self.StareHasloInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.StareHasloInput.setGeometry(QtCore.QRect(210, 125, 381, 70))
        self.StareHasloInput.setObjectName("StareHasloInput")
        self.StareHasloInput.setFont(self.czc1)
        self.ErrorLabel = QtWidgets.QLabel(self)
        self.ErrorLabel.setGeometry(QtCore.QRect(140, 20, 531, 61))
        self.ErrorLabel.setText("")
        self.ErrorLabel.setObjectName("ErrorLabel")
        self.ErrorLabel.setStyleSheet("color:red; font-size:35px;")
        self.ErrorLabel.setAlignment(QtCore.Qt.AlignCenter)

    def closeEvent(self,event):
        self.konto.overlay.deleteLater()
        self.konto.setEnabled(True)
        self.close()





    def zmien(self):
        if len(self.StareHasloInput.text()) < 1 or len(self.NoweHasloInput.text()) < 1 or len(self.PowtorzHasloInput.text()) < 1:
            self.ErrorLabel.setText("BRAKUJE DANYCH")
        
        elif self.NoweHasloInput.text() != self.PowtorzHasloInput.text():
            self.ErrorLabel.setText("HASŁA SIĘ RÓŻNIĄ")
        
        else:
            self.client = MongoClient('localhost', 27017)
            self.db = self.client['Fitatu']
            self.collection = self.db['users']
            hashed_stare_input = self.StareHasloInput.text()
            hashed_stare = self.collection.find_one({"id_app":self.id_user})["haslo"]
            if bcrypt.checkpw(hashed_stare_input.encode(), hashed_stare):
                inp_passwd = self.NoweHasloInput.text()
                salt = bcrypt.gensalt()
                hashed_passwd_nowe = bcrypt.hashpw(inp_passwd.encode(),salt)
                myquery = { "haslo": hashed_stare}
                newvalues = { "$set": { "haslo": hashed_passwd_nowe } }
                if self.collection.update_one(myquery, newvalues):
                    self.ErrorLabel.setStyleSheet("color:green; font-size:35px;")
                    self.ErrorLabel.setText("HASLO ZOSTALO ZMIENIONE")
            else:
                self.ErrorLabel.setText("HASŁO JEST NIEPOPRAWNE")
            self.client.close()