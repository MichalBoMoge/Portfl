import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QVBoxLayout,QLabel, QWidget, QPushButton, QMainWindow
from datetime import datetime,timedelta, date
from pymongo import MongoClient
from PyQt5 import QtCore, QtGui

class Wykres(QMainWindow):
    def __init__(self, dane,superObj):
        super().__init__()
        self.superObj = superObj
        self.login = dane["login"]
        self.id_user = dane["id_user"]
        self.setWindowTitle("Twój progres")
        self.setStyleSheet(
            """
            QPushButton{
            background-color: rgba(125,125,125,0);
            }
            """
        )
        self.setObjectName("self")
        self.resize(1920, 1080)
        self.setMinimumSize(QtCore.QSize(1920, 1080))
        self.setMaximumSize(QtCore.QSize(1920, 1080))
        self.Background = QLabel(self)
        self.Background.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.Background.setMinimumSize(QtCore.QSize(1920, 1080))
        self.Background.setMaximumSize(QtCore.QSize(1920, 1080))
        self.Background.setText("")
        self.Background.setPixmap(QtGui.QPixmap("Background/Wykres.png"))
        self.Background.setObjectName("Background")
        self.PrzepisyButton = QPushButton(self)
        self.PrzepisyButton.setGeometry(QtCore.QRect(0, 130, 121, 121))
        self.PrzepisyButton.setText("")
        self.PrzepisyButton.setObjectName("PrzepisyButton")
        self.PrzepisyButton.clicked.connect(self.otworz_przepisy)
        self.ProduktyButton = QPushButton(self)
        self.ProduktyButton.setGeometry(QtCore.QRect(0, 430, 121, 141))
        self.ProduktyButton.setText("")
        self.ProduktyButton.clicked.connect(self.otworz_produkty)
        self.ProduktyButton.setObjectName("ProduktyButton")
        self.UstawieniaButton = QPushButton(self)
        self.UstawieniaButton.setGeometry(QtCore.QRect(0, 590, 121, 141))
        self.UstawieniaButton.setText("")
        self.UstawieniaButton.setObjectName("UstawieniaButton")
        self.UstawieniaButton.clicked.connect(self.otworz_ustawienia)
        self.BialkoButton = QPushButton(self)
        self.BialkoButton.setGeometry(QtCore.QRect(250, 830, 291, 81))
        self.BialkoButton.setText("")
        self.BialkoButton.setObjectName("BialkoButton")
        self.KalorieButton = QPushButton(self)
        self.KalorieButton.setGeometry(QtCore.QRect(600, 830, 281, 81))
        self.KalorieButton.setText("")
        self.KalorieButton.setObjectName("KalorieButton")
        self.TluszczButton = QPushButton(self)
        self.TluszczButton.setGeometry(QtCore.QRect(940, 830, 291, 81))
        self.TluszczButton.setText("")
        self.TluszczButton.setObjectName("TluszczButton")
        self.WeglowodanyButton = QPushButton(self)
        self.WeglowodanyButton.setGeometry(QtCore.QRect(1280, 830, 291, 81))
        self.WeglowodanyButton.setText("")
        self.WeglowodanyButton.setObjectName("WeglowodanyButton")

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.placeholder = QWidget()
        self.placeholder.setGeometry(200,25,1500,800)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.placeholder.setLayout(layout)
        self.layout().addWidget(self.placeholder)
        self.KalorieButton.clicked.connect(lambda: generate_plot(self,"kalorie","cel_kcal", self.id_user))
        self.WeglowodanyButton.clicked.connect(lambda: generate_plot(self,"weglowodany","cel_wegle", self.id_user))
        self.TluszczButton.clicked.connect(lambda: generate_plot(self,"tluszcz","cel_tluszcz", self.id_user))
        self.BialkoButton.clicked.connect(lambda: generate_plot(self,"bialko","cel_bialko", self.id_user))
        generate_plot(self,"kalorie","cel_kcal", self.id_user)


    def otworz_przepisy(self):
        self.superObj.przepisy.show()
        self.hide()


    def otworz_ustawienia(self):
        self.superObj.konto.show()
        self.hide()


    def otworz_produkty(self):
        self.superObj.produkty.show()
        self.hide()

def generate_plot(self,_str, _str2, id_user):
    dates = [str((datetime.now() - timedelta(days=x)).strftime('%d-%m')) for x in range(6, -1, -1)]
    values_list = []
    values_cel = []
    self.nazwa_kolekcji = "users_daily_"+str(self.id_user)
    self.client = MongoClient('localhost', 27017)
    self.db = self.client['Fitatu']
    if self.nazwa_kolekcji not in self.db.list_collection_names():
            print("nie ma kolekcji to ja tworze")
            self.db.create_collection(self.nazwa_kolekcji)
    self.collection = self.db[self.nazwa_kolekcji]
    cel = self.db["users"].find_one({"id_app":id_user})[_str2]
    print(cel)
    data_sprzed_7_dni = datetime.now() - timedelta(days=6)
    for i in range((datetime.now() - data_sprzed_7_dni).days +1):
        values_cel.append(cel)
        suma_kalorie = 0
        aktualna_data = data_sprzed_7_dni + timedelta(days=i)
        dane = self.collection.find({"id_user":self.id_user, 
        "data":str(aktualna_data.strftime("%Y-%m-%d"))})
        for single in dane:
            suma_kalorie += int(single[_str])
        values_list.append(suma_kalorie)
    self.figure.clear()
    values = np.array(values_list)
    ax = self.figure.add_subplot(111)
    ax.plot(dates, values, label = "twoj wynik")
    ax.plot(dates, values_cel, label = "twoj cel") 
    ax.legend()
    ax.set_title('Twój progres w tym tygodniu')
    ax.set_xlabel('Data')
    ax.set_ylabel('Spożyte makro')
    self.canvas.draw()
    self.client.close()

