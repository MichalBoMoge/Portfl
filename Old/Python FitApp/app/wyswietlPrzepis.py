from PyQt5 import QtCore, QtGui, QtWidgets
from Wykres import generate_plot
from datetime import date
from pymongo import MongoClient

class wyswietlPrzepis(QtWidgets.QWidget):
    def __init__(self, przepisy, superObj,dane):
        self.przepisy = przepisy
        self.superObj = superObj
        self.dane = dane
        super().__init__()
        self.setObjectName("self")
        self.resize(900, 600)
        self.setMinimumSize(QtCore.QSize(900, 600))
        self.setMaximumSize(QtCore.QSize(900, 600))
        self.setStyleSheet(
            """
            QPushButton{
            background-color: rgba(125,125,125,0);
            }


            QLabel{
            font-size: 20px;
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
        self.Background.setGeometry(QtCore.QRect(0, 0, 900, 600))
        self.Background.setMinimumSize(QtCore.QSize(900, 600))
        self.Background.setMaximumSize(QtCore.QSize(900, 600))
        self.Background.setText("")
        self.Background.setPixmap(QtGui.QPixmap("Background/PrzepisyWyswietl3.png"))
        self.Background.setObjectName("Background")
        self.NazwaPrzepisu = QtWidgets.QLabel(self)
        self.NazwaPrzepisu.setGeometry(QtCore.QRect(94, 20, 741, 51))
        self.NazwaPrzepisu.setText("")
        self.NazwaPrzepisu.setObjectName("NazwaPrzepisu")
        self.TrescPrzepisu = QtWidgets.QLabel(self)
        self.TrescPrzepisu.setText("")
        self.TrescPrzepisu.setObjectName("TrescPrzepisu")
        self.TrescPrzepisu.setWordWrap(True)
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidget(self.TrescPrzepisu)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setGeometry(QtCore.QRect(20, 110, 871, 400))
        self.BialkoWPrzepisie = QtWidgets.QLabel(self)
        self.BialkoWPrzepisie.setGeometry(QtCore.QRect(204, 68, 61, 31))
        self.BialkoWPrzepisie.setText("")
        self.BialkoWPrzepisie.setObjectName("BialkoWPrzepisie")
        self.KalorieWPrzepisie = QtWidgets.QLabel(self)
        self.KalorieWPrzepisie.setGeometry(QtCore.QRect(335, 68, 51, 31))
        self.KalorieWPrzepisie.setText("")
        self.KalorieWPrzepisie.setObjectName("KalorieWPrzepisie")
        self.TluszczWPrzepisie = QtWidgets.QLabel(self)
        self.TluszczWPrzepisie.setGeometry(QtCore.QRect(452, 68, 51, 31))
        self.TluszczWPrzepisie.setText("")
        self.TluszczWPrzepisie.setObjectName("TluszczWPrzepisie")
        self.WegleWPrzepisie = QtWidgets.QLabel(self)
        self.WegleWPrzepisie.setGeometry(QtCore.QRect(630, 68, 71, 31))
        self.WegleWPrzepisie.setText("")
        self.WegleWPrzepisie.setObjectName("WegleWPrzepisie")
        self.XButton = QtWidgets.QPushButton(self)
        self.XButton.setGeometry(QtCore.QRect(850, 10, 41, 41))
        self.XButton.setText("")
        self.XButton.setObjectName("XButton")
        self.XButton.clicked.connect(self.closeEvent)
        self.ZastosujButton = QtWidgets.QPushButton(self)
        self.ZastosujButton.setGeometry(QtCore.QRect(540, 540, 261, 61))
        self.ZastosujButton.setText("")
        self.ZastosujButton.setObjectName("ZastosujButton")
        self.ZastosujButton.clicked.connect(self.oblicz)
        self.GramyInput = QtWidgets.QLineEdit(self)
        self.GramyInput.setGeometry(QtCore.QRect(120, 540, 381, 51))
        self.GramyInput.setObjectName("GramyInput")



    def closeEvent(self,event):
        self.przepisy.overlay.deleteLater()
        self.przepisy.setEnabled(True)
        self.close()


    def oblicz(self):
        if self.GramyInput.text().isdigit():
            wartosci = {
                "kalorie":float(self.KalorieWPrzepisie.text()),
                "tluszcz":float(self.TluszczWPrzepisie.text()),
                "weglowodany":float(self.WegleWPrzepisie.text()),
                "bialko":float(self.BialkoWPrzepisie.text())        
                }
            ilosc = float(float(self.GramyInput.text())/100)
            wartosci["kalorie"] = int(wartosci["kalorie"] *ilosc)
            wartosci["tluszcz"] = int(wartosci["tluszcz"] *ilosc)
            wartosci["weglowodany"] = int(wartosci["weglowodany"] *ilosc)
            wartosci["bialko"] = int(wartosci["bialko"] *ilosc)
            print(wartosci)
            self.client = MongoClient('localhost', 27017)
            self.db = self.client['Fitatu']
            self.collection = self.db[('users_daily_'+str(self.dane["id_user"]))]
            if self.collection.insert_one({"id_user":self.dane["id_user"],"data":str(date.today()),"kalorie":wartosci["kalorie"],
                    "tluszcz":wartosci["tluszcz"],"weglowodany":wartosci["weglowodany"],
                    "bialko":wartosci["bialko"]}):
                self.client.close()
                generate_plot(self.superObj.wykres,"kalorie","cel_kcal", self.dane["id_user"])
                self.superObj.wykres.show()
                self.client.close()
                self.close()
                self.przepisy.close()

