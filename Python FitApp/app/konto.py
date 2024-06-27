from tabelka import Nastepne
from pymongo import MongoClient    
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel,QPushButton
from PyQt5 import QtCore, QtWidgets, QtGui
from Wykres import generate_plot
from haslo import Haslo
from usun import Usun

class Konto(QWidget):



    def __init__(self,dane,superObj):
        super().__init__()
        self.login = dane["login"]
        self.dane = dane
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Fitatu']
        self.collection = self.db[('users')]
        self.setStyleSheet(
            """
            QPushButton{
            background-color: rgba(0,0,0,0);
            }


            QLabel{
            font-size: 45px;
            }

            QTextEdit{
            background-color: rgba(255, 255, 255, 0); 
            color: black; 
            border:none
            }

            """
        )
        self.superObj = superObj
        self.id_user = dane["id_user"]
        self.setObjectName("self")
        self.resize(1920, 1080)
        self.czc1 = QtGui.QFont()
        self.czc1.setPointSize(30)
        self.setMinimumSize(QtCore.QSize(1920, 1080))
        self.setMaximumSize(QtCore.QSize(1920, 1080))
        self.Background = QtWidgets.QLabel(self)
        self.Background.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.Background.setMinimumSize(QtCore.QSize(1920, 1080))
        self.Background.setText("")
        self.Background.setPixmap(QtGui.QPixmap("Background/Zmiany PCv2.png"))
        self.Background.setObjectName("Background")
        self.LoginInput = QtWidgets.QTextEdit(self)
        self.LoginInput.setGeometry(QtCore.QRect(330, 240, 461, 60))
        self.LoginInput.setObjectName("LoginInput")
        self.LoginInput.setFont(self.czc1)
        self.KalorieInput = QtWidgets.QTextEdit(self)
        self.KalorieInput.setGeometry(QtCore.QRect(330, 400, 461, 60))
        self.KalorieInput.setObjectName("KalorieInput")
        self.KalorieInput.setFont(self.czc1)
        self.BialkoInput = QtWidgets.QTextEdit(self)
        self.BialkoInput.setGeometry(QtCore.QRect(330, 550, 461, 60))
        self.BialkoInput.setObjectName("BialkoInput")
        self.BialkoInput.setFont(self.czc1)
        self.TluszczInput = QtWidgets.QTextEdit(self)
        self.TluszczInput.setGeometry(QtCore.QRect(330, 690, 461, 60))
        self.TluszczInput.setObjectName("TluszczInput")
        self.TluszczInput.setFont(self.czc1)
        self.WegleInput = QtWidgets.QTextEdit(self)
        self.WegleInput.setGeometry(QtCore.QRect(330, 850, 461, 60))
        self.WegleInput.setObjectName("WegleInput")
        self.WegleInput.setFont(self.czc1)
        self.ZmienHasloButton = QtWidgets.QPushButton(self)
        self.ZmienHasloButton.setGeometry(QtCore.QRect(290, 950, 541, 81))
        self.ZmienHasloButton.setText("")
        self.ZmienHasloButton.setObjectName("ZmienHasloButton")
        self.ZmienHasloButton.clicked.connect(self.zmienHaslo)
        self.UsunKontoButton = QtWidgets.QPushButton(self)
        self.UsunKontoButton.setGeometry(QtCore.QRect(1090, 950, 531, 81))
        self.UsunKontoButton.setText("")
        self.UsunKontoButton.setObjectName("UsunKontoButton")
        self.UsunKontoButton.clicked.connect(self.usunKonto)
        self.KalorieLabel = QtWidgets.QLabel(self)
        self.KalorieLabel.setGeometry(QtCore.QRect(1380, 703, 361, 41))
        self.KalorieLabel.setText("")
        self.KalorieLabel.setObjectName("KalorieLabel")
        self.BialkoLabel = QtWidgets.QLabel(self)
        self.BialkoLabel.setGeometry(QtCore.QRect(1380, 748, 371, 41))
        self.BialkoLabel.setText("")
        self.BialkoLabel.setObjectName("BialkoLabel")
        self.TluszczLabel = QtWidgets.QLabel(self)
        self.TluszczLabel.setGeometry(QtCore.QRect(1380, 791, 381, 41))
        self.TluszczLabel.setText("")
        self.TluszczLabel.setObjectName("TluszczLabel")
        self.WegleLabel = QtWidgets.QLabel(self)
        self.WegleLabel.setGeometry(QtCore.QRect(1380, 838, 551, 41))
        self.WegleLabel.setText("")
        self.WegleLabel.setObjectName("WegleLabel")
        self.PrzepisyButton = QtWidgets.QPushButton(self)
        self.PrzepisyButton.setGeometry(QtCore.QRect(0, 130, 121, 121))
        self.PrzepisyButton.setText("")
        self.PrzepisyButton.setObjectName("PrzepisyButton")
        self.PrzepisyButton.clicked.connect(self.otworz_przepisy)
        self.ProgresButton = QtWidgets.QPushButton(self)
        self.ProgresButton.setGeometry(QtCore.QRect(0, 280, 121, 121))
        self.ProgresButton.setText("")
        self.ProgresButton.setObjectName("ProgresButton")
        self.ProgresButton.clicked.connect(self.otworz_progres)
        self.ProduktyButton = QtWidgets.QPushButton(self)
        self.ProduktyButton.setGeometry(QtCore.QRect(0, 430, 121, 131))
        self.ProduktyButton.setText("")
        self.ProduktyButton.setObjectName("ProduktyButton")
        self.ProduktyButton.clicked.connect(self.otworz_produkty)
        self.WprowadzButton = QtWidgets.QPushButton(self)
        self.WprowadzButton.setGeometry(QtCore.QRect(1080, 530, 541, 91))
        self.WprowadzButton.setText("")
        self.WprowadzButton.setObjectName("WprowadzButton")
        self.WprowadzButton.clicked.connect(self.zmienKonto )
        self.uzupelnij()

    def otworz_produkty(self):
        self.superObj.produkty.show()
        self.hide()

    def otworz_progres(self):
        self.superObj.wykres.show()
        self.hide()

    def otworz_przepisy(self):
        self.superObj.przepisy.show()
        self.hide()


    def zmienHaslo(self):

        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        self.overlay.setGeometry(QtCore.QRect(0,0,1920,1080))
        self.overlay.show()
        self.pswd = Haslo(konto=self, id_user=self.id_user)
        self.pswd.show()

        
    def usunKonto(self):
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        self.overlay.setGeometry(QtCore.QRect(0,0,1920,1080))
        self.overlay.show()
        self.usun = Usun(konto=self, id_user=self.id_user)
        self.usun.show()


    def uzupelnij(self):
        dane = self.collection.find_one({"login":self.login})
        self.KalorieLabel.setText(str(dane["cel_kcal"]))
        self.WegleLabel.setText(str(dane["cel_wegle"]))
        self.TluszczLabel.setText(str(dane["cel_tluszcz"]))
        self.BialkoLabel.setText(str(dane["cel_bialko"]))

    def powrot(self):
        pass


    def zmienKonto(self):
        dane = self.collection.find_one({"login":self.login})
        zmiana = self.LoginInput.toPlainText()
        if len(zmiana) > 1:
            myquery = { "login": self.login }
            newvalues = { "$set": { "login": zmiana } }
            if self.collection.update_one(myquery, newvalues):
                self.login = zmiana
            self.LoginInput.setText("")


        zmiana = self.KalorieInput.toPlainText()
        if zmiana is not None and zmiana.isnumeric():
            myquery = { "cel_kcal": int(dane["cel_kcal"])}
            newvalues = { "$set": { "cel_kcal": int(zmiana) } }
            if self.collection.update_one(myquery, newvalues):
                pass
            generate_plot(self.superObj.wykres,"kalorie","cel_kcal", self.id_user)
            self.KalorieInput.setText("")

        zmiana = self.WegleInput.toPlainText()
        if zmiana is not None and zmiana.isnumeric():
            myquery = { "cel_wegle": int(dane["cel_wegle"])}
            newvalues = { "$set": { "cel_wegle": int(zmiana) } }
            if self.collection.update_one(myquery, newvalues):
                pass
            self.WegleInput.setText("")

        zmiana = self.TluszczInput.toPlainText()
        if zmiana is not None and zmiana.isnumeric():
            myquery = { "cel_tluszcz": int(dane["cel_tluszcz"])}
            newvalues = { "$set": { "cel_tluszcz": int(zmiana) } }
            if self.collection.update_one(myquery, newvalues):
                pass
            self.TluszczInput.setText("")

        zmiana = self.BialkoInput.toPlainText()
        if zmiana is not None and zmiana.isnumeric():
            myquery = { "cel_bialko": int(dane["cel_bialko"])}
            newvalues = { "$set": { "cel_bialko": int(zmiana) } }
            if self.collection.update_one(myquery, newvalues):
                pass
            self.BialkoInput.setText("")
        
        self.uzupelnij()