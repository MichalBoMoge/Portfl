from PyQt5 import QtCore, QtGui, QtWidgets
from pymongo import MongoClient
from dodajPrzepis import dodajPrzepis
from wyswietlPrzepis import wyswietlPrzepis
from filtrujPrzepis import filtrujPrzepis


class Przepisy(QtWidgets.QWidget):
    def __init__(self,superObj,dane):
        super().__init__()
        self.login = dane["login"]
        self.dane = dane
        self.superObj = superObj
        self.id_user = dane["id_user"]
        self.setObjectName("self")
        self.resize(1920, 1080)
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.setMaximumSize(QtCore.QSize(1920, 1080))
        self.setStyleSheet(
            """
            QPushButton{
            background-color: rgba(0,0,0,0);
            }


            QLabel{
            font-size: 45px;
            }

            QLineEdit{
            background-color: rgba(255, 255, 255, 0); 
            color: black; 
            border:none;
            text-align: center;
            font-size: 40px;
            }

            """
        )
        self.Background = QtWidgets.QLabel(self)
        self.Background.setGeometry(QtCore.QRect(0, 0, 1920, 1071))
        self.Background.setMinimumSize(QtCore.QSize(1280, 720))
        self.Background.setMaximumSize(QtCore.QSize(1920, 1080))
        self.Background.setText("")
        self.Background.setPixmap(QtGui.QPixmap("Background/Przepisy PC2.png"))
        self.Background.setObjectName("Background")
        self.WyszukiwaniePrzepisu = QtWidgets.QLineEdit(self)
        self.WyszukiwaniePrzepisu.setGeometry(QtCore.QRect(723, 46, 541, 81))
        self.WyszukiwaniePrzepisu.setObjectName("wpis")
        self.WyszukiwaniePrzepisu.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: black; border:none")
        self.ProgresButton = QtWidgets.QPushButton(self)
        self.ProgresButton.setGeometry(QtCore.QRect(0, 260, 121, 141))
        self.ProgresButton.setText("")
        self.ProgresButton.setObjectName("ProgresButton")
        self.ProgresButton.clicked.connect(self.otworz_progres)
        self.DodajButton = QtWidgets.QPushButton(self)
        self.DodajButton.setGeometry(QtCore.QRect(700,950,520,130))
        self.DodajButton.setText("")
        self.DodajButton.clicked.connect(self.dodaj_przepis)

        self.ProduktyButton = QtWidgets.QPushButton(self)
        self.ProduktyButton.setGeometry(QtCore.QRect(0, 430, 121, 131))
        self.ProduktyButton.setText("")
        self.ProduktyButton.setObjectName("ProduktyButton")
        self.ProduktyButton.clicked.connect(self.otworz_produkty)
        self.UstawieniaButton = QtWidgets.QPushButton(self)
        self.UstawieniaButton.setGeometry(QtCore.QRect(0, 590, 121, 131))
        self.UstawieniaButton.setText("")
        self.UstawieniaButton.setObjectName("UstawieniaButton")
        self.UstawieniaButton.clicked.connect(self.otworz_ustawienia)
        self.FiltryButton = QtWidgets.QPushButton(self)
        self.FiltryButton.setGeometry(QtCore.QRect(540, 40, 111, 91))
        self.FiltryButton.setText("")
        self.FiltryButton.setObjectName("FiltryButton")
        self.FiltryButton.clicked.connect(self.otworz_filtry)
        self.WyszukajButton = QtWidgets.QPushButton(self)
        self.WyszukajButton.setGeometry(QtCore.QRect(1260, 40, 111, 91))
        self.WyszukajButton.setText("")
        self.WyszukajButton.setObjectName("WyszukajButton")
        self.WyszukajButton.clicked.connect(self.find_products)
        self.listView = QtWidgets.QListWidget(self)
        self.listView.setGeometry(QtCore.QRect(340, 240, 1200, 690))
        self.listView.setMinimumSize(QtCore.QSize(1200, 690))
        self.listView.setMaximumSize(QtCore.QSize(1200, 690))
        self.listView.setObjectName("lista")
        self.listView.setStyleSheet("border: none; font-size: 30px;")
        self.listView.clicked.connect(self.otworzPrzepis)

    def otworz_filtry(self):
        self.overlay = QtWidgets.QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        self.overlay.setGeometry(QtCore.QRect(0,0,1920,1080))
        self.overlay.show()
        self.dodaj = filtrujPrzepis(self)
        self.dodaj.show()

    def dodaj_przepis(self):
        self.overlay = QtWidgets.QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        self.overlay.setGeometry(QtCore.QRect(0,0,1920,1080))
        self.overlay.show()
        self.dodaj = dodajPrzepis(self)
        self.dodaj.show()


    def otworzPrzepis(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Fitatu']
        self.collection = self.db[('users')]
        checking = self.listView.currentItem().text()
        query = {"nazwa": {"$regex": checking , "$options": "i"}}
        self.collection = self.db['przepisy']
        result = self.collection.find(query)
        self.overlay = QtWidgets.QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        self.overlay.setGeometry(QtCore.QRect(0,0,1920,1080))
        self.overlay.show()
        self.wyswietl = wyswietlPrzepis(self,self.superObj,self.dane)
        self.wyswietl.KalorieWPrzepisie.setText(str(result[0]['kalorie']))
        self.wyswietl.WegleWPrzepisie.setText(str(result[0]['weglowodany']))
        self.wyswietl.BialkoWPrzepisie.setText(str(result[0]['bialko']))
        self.wyswietl.NazwaPrzepisu.setText(result[0]['nazwa'])
        self.wyswietl.TluszczWPrzepisie.setText(str(result[0]['tluszcz']))
        self.wyswietl.TrescPrzepisu.setText(result[0]['przepis'])
        self.client.close()
        self.wyswietl.show()

    def otworz_progres(self):
        self.superObj.wykres.show()
        self.hide()

    def otworz_ustawienia(self):
        self.superObj.konto.show()
        self.hide()


    def otworz_produkty(self):
        self.superObj.produkty.show()
        self.hide()

    def find_products(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Fitatu']
        self.collection = self.db[('users')]        
        text_object = self.findChildren(QtWidgets.QLineEdit,"wpis")[0].text()
        list_find = self.findChildren(QtWidgets.QListWidget,"lista")[0]
        list_find.clear()   
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['Fitatu']
        self.collection = self.db['przepisy']
        query = {"nazwa": {"$regex": text_object , "$options": "i"}}
        result = self.collection.find(query)
        for single in result:
            name = single["nazwa"]
            list_find.insertItem(0,name)
        self.client.close()
