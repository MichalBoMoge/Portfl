from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit,QPushButton, QTextBrowser
from datetime import date
from pymongo import MongoClient
from PyQt5 import QtCore, QtGui
from Wykres import generate_plot

class Nastepne(QWidget):
    def __init__(self,superObj,wyszukiwarka, dane):
        super().__init__()
        self.setStyleSheet(
            """
            QPushButton{
            background-color: rgba(125,125,125,0);
            }

            QTextBrowser{
            border: none;
            background-color: rgba(125,125,125,0);
            font-size: 25px;
            text-align: center;
            }
            QLineEdit{
            border: none;
            background-color: rgba(125,125,125,0);
            font-size: 35px;
            }

            """
        )
        self.id_user = dane["id_user"]
        self.login = dane["login"]
        self.superObj = superObj
        self.wyszukiwarka = wyszukiwarka
        self.resize(900, 600)
        self.setMinimumSize(QtCore.QSize(900, 600))
        self.setMaximumSize(QtCore.QSize(900, 600))
        self.Background = QLabel(self)
        self.Background.setGeometry(QtCore.QRect(0, -10, 911, 621))
        self.Background.setText("")
        self.Background.setPixmap(QtGui.QPixmap("background/tabelka.png"))
        self.Background.setObjectName("Background")

        self.NazwaDisplay = QTextBrowser(self)
        self.NazwaDisplay.setGeometry(QtCore.QRect(450, 26, 381, 41))
        self.NazwaDisplay.setObjectName("NazwaDisplay")
        self.RodzajDisplay = QTextBrowser(self)
        self.RodzajDisplay.setGeometry(QtCore.QRect(450, 74, 381, 41))
        self.RodzajDisplay.setObjectName("RodzajDisplay")
        self.KalorieDisplay = QTextBrowser(self)
        self.KalorieDisplay.setGeometry(QtCore.QRect(450, 121, 381, 41))
        self.KalorieDisplay.setObjectName("KalorieDisplay")
        self.TluszczDisplay = QTextBrowser(self)
        self.TluszczDisplay.setGeometry(QtCore.QRect(450, 170, 381, 41))
        self.TluszczDisplay.setObjectName("TluszczDisplay")
        self.WegleDisplay = QTextBrowser(self)
        self.WegleDisplay.setGeometry(QtCore.QRect(450, 217, 381, 41))
        self.WegleDisplay.setObjectName("WegleDisplay")
        self.BialkoDisplay = QTextBrowser(self)
        self.BialkoDisplay.setGeometry(QtCore.QRect(450, 263, 381, 41))
        self.BialkoDisplay.setObjectName("BialkoDisplay")

        self.GramyText = QLineEdit(self)
        self.GramyText.setGeometry(QtCore.QRect(170, 356, 561, 71))
        self.GramyText.setObjectName("GramyText")

        self.ObliczButton = QPushButton(self)
        self.ObliczButton.setGeometry(QtCore.QRect(130, 440, 641, 91))
        self.ObliczButton.setText("")
        self.ObliczButton.setObjectName("ObliczButton")
        self.ObliczButton.clicked.connect(self.oblicz)
        self.czc = QtGui.QFont()
        self.czc.setPointSize(40)
        self.ErrorLabel = QLabel(self)
        self.ErrorLabel.setStyleSheet("color:red;")
        self.ErrorLabel.setGeometry(QtCore.QRect(200,530,500,70))
        self.ErrorLabel.setFont(self.czc)

        self.ErrorLabel.setAlignment(QtCore.Qt.AlignCenter)

    def closeEvent(self,event):
        self.wyszukiwarka.overlay.deleteLater()
        self.wyszukiwarka.setEnabled(True)



    def oblicz(self):
        if self.GramyText.text().isdigit():
            wartosci = {
                "kalorie":float(self.KalorieDisplay.toPlainText()),
                "tluszcz":float(self.TluszczDisplay.toPlainText()),
                "weglowodany":float(self.WegleDisplay.toPlainText()),
                "bialko":float(self.BialkoDisplay.toPlainText())        }
            ilosc = float(float(self.GramyText.text())/100)
            wartosci["kalorie"] = int(wartosci["kalorie"] *ilosc)
            wartosci["tluszcz"] = int(wartosci["tluszcz"] *ilosc)
            wartosci["weglowodany"] = int(wartosci["weglowodany"] *ilosc)
            wartosci["bialko"] = int(wartosci["bialko"] *ilosc)
            self.client = MongoClient('localhost', 27017)
            self.db = self.client['Fitatu']
            self.collection = self.db[('users_daily_'+str(self.id_user))]
            if self.collection.insert_one({"id_user":self.id_user,"data":str(date.today()),"kalorie":wartosci["kalorie"],
                    "tluszcz":wartosci["tluszcz"],"weglowodany":wartosci["weglowodany"],
                    "bialko":wartosci["bialko"]}):
                self.client.close()
                generate_plot(self.superObj.wykres,"kalorie","cel_kcal", self.id_user)
                self.superObj.wykres.show()
                self.client.close()
                self.close()
                self.wyszukiwarka.close()                 
        else:
            self.ErrorLabel.setText("niepoprawny wpis")

