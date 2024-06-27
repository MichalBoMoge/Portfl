from tabelka import Nastepne
from pymongo import MongoClient    
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel, QTableWidgetItem
from PyQt5 import QtCore, QtWidgets, QtGui

def zapiszRodzaj(rdz):
    match rdz:
        case 1: return "warzywa"
        case 2: return "owoce"
        case 3: return "orzechy"
        case 4: return "mieso"
        case 5: return "nabial"
        case _: return "nieokreslony"

class Wyszukiwarka(QWidget):
    def __init__(self,dane,superObj):
        super().__init__()
        self.setStyleSheet(
            """
            QPushButton{
            background-color: rgba(125,125,125,0);
            }


            
            """

        )
        self.login = dane["login"]
        self.id_user = dane["id_user"]
        self.superObj = superObj
        self.setObjectName("self")
        self.resize(1920, 1080)
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setMaximumSize(QtCore.QSize(1920, 1080))
        self.czc1 = QtGui.QFont()
        self.czc1.setPointSize(35)
        self.BackgroundPrzepisy = QtWidgets.QLabel(self)
        self.BackgroundPrzepisy.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.BackgroundPrzepisy.setMinimumSize(QtCore.QSize(1280, 720))
        self.BackgroundPrzepisy.setMaximumSize(QtCore.QSize(1920, 1080))
        self.BackgroundPrzepisy.setText("")
        self.BackgroundPrzepisy.setPixmap(QtGui.QPixmap("Background/Wyszukiwarka PC2.png"))
        self.BackgroundPrzepisy.setObjectName("BackgroundPrzepisy")
        self.WyszukiwanieProduktow = QtWidgets.QLineEdit(self)
        self.WyszukiwanieProduktow.setGeometry(QtCore.QRect(720, 46, 600, 91))
        self.WyszukiwanieProduktow.setObjectName("wpis")
        self.WyszukiwanieProduktow.textChanged.connect(self.find_products)
        self.WyszukiwanieProduktow.setFont(self.czc1)
        self.WyszukiwanieProduktow.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: black; border:none")
        self.PrzepisyButton = QtWidgets.QPushButton(self)
        self.PrzepisyButton.setGeometry(QtCore.QRect(0, 120, 121, 141))
        self.PrzepisyButton.setText("")
        self.PrzepisyButton.setObjectName("PrzepisyButton")
        self.PrzepisyButton.clicked.connect(self.otworz_przepisy)
        self.ProgresButton = QtWidgets.QPushButton(self)
        self.ProgresButton.setGeometry(QtCore.QRect(0, 280, 121, 131))
        self.ProgresButton.setText("")
        self.ProgresButton.setObjectName("ProgresButton")
        self.ProgresButton.clicked.connect(self.otworz_progres)
        self.UstawieniaButton = QtWidgets.QPushButton(self)
        self.UstawieniaButton.setGeometry(QtCore.QRect(0, 590, 121, 141))
        self.UstawieniaButton.setText("")
        self.UstawieniaButton.setObjectName("UstawieniaButton")
        self.UstawieniaButton.clicked.connect(self.otworz_ustawienia)
        self.listView = QtWidgets.QListWidget(self)
        self.listView.setGeometry(QtCore.QRect(320, 280, 1400, 600))
        self.listView.setMinimumSize(QtCore.QSize(1400, 600))
        self.listView.setMaximumSize(QtCore.QSize(1400, 600))
        self.listView.setObjectName("lista")
        self.listView.clicked.connect(self.Wypisz)    
        self.listView.setStyleSheet("border: none; font-size: 30px;")

    def otworz_progres(self):
        self.superObj.wykres.show()
        self.hide()

    def otworz_ustawienia(self):
        self.superObj.konto.show()
        self.hide()

    def otworz_przepisy(self):
        self.superObj.przepisy.show()
        self.hide()


    def find_products(self):
        text_object = self.findChildren(QtWidgets.QLineEdit,"wpis")[0].text()
        list_find = self.findChildren(QtWidgets.QListWidget,"lista")[0]
        list_find.clear()   
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Fitatu']
        self.collection = self.db['produkty']
        query = {"nazwa": {"$regex": text_object , "$options": "i"}}
        result = self.collection.find(query)
        for single in result:
            name = single["nazwa"]
            list_find.insertItem(0,name)

    def Wypisz(self):
        checking = self.listView.currentItem().text()
        query = {"nazwa": {"$regex": checking , "$options": "i"}}
        result = self.collection.find(query)
        self.w = Nastepne(superObj=self.superObj, wyszukiwarka=self,dane=self.superObj.dane)
        self.w.NazwaDisplay.setText(str(result[0]['nazwa']))
        self.w.RodzajDisplay.setText(zapiszRodzaj(result[0]['rodzaj']))
        self.w.KalorieDisplay.setText(str(result[0]['kalorie']))
        self.w.TluszczDisplay.setText(str(result[0]['tluszcz']))
        self.w.WegleDisplay.setText(str(result[0]['weglowodany']))
        self.w.BialkoDisplay.setText(str(result[0]['bialko']))
        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        self.overlay.setGeometry(QtCore.QRect(0,0,1920,1080))
        self.overlay.show()
        self.w.show()


