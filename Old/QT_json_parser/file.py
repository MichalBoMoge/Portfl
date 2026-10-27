import json
import urllib.request
from PyQt5 import QtCore, QtGui, QtWidgets


listaStacji = []
with urllib.request.urlopen("https://danepubliczne.imgw.pl/api/data/synop") as file:
    dane = json.load(file)

for stacja in dane:
    listaStacji.append({stacja["id_stacji"]: stacja["stacja"]})




class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Stacja = QtWidgets.QLabel(self.centralwidget)
        self.Stacja.setGeometry(QtCore.QRect(300, 10, 400, 50))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(False)
        self.Stacja.setFont(font)
        self.Stacja.setAlignment(QtCore.Qt.AlignCenter)
        self.Stacja.setObjectName("Stacja")
        self.Data = QtWidgets.QLabel(self.centralwidget)
        self.Data.setGeometry(QtCore.QRect(150, 70, 300, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.Data.setFont(font)
        self.Data.setObjectName("Data")
        self.Godzina = QtWidgets.QLabel(self.centralwidget)
        self.Godzina.setGeometry(QtCore.QRect(600, 70, 200, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.Godzina.setFont(font)
        self.Godzina.setObjectName("Godzina")
        self.temperatura = QtWidgets.QLabel(self.centralwidget)
        self.temperatura.setGeometry(QtCore.QRect(100, 170, 500, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.temperatura.setFont(font)
        self.temperatura.setObjectName("temperatura")
        self.Predkosc_wiatru = QtWidgets.QLabel(self.centralwidget)
        self.Predkosc_wiatru.setGeometry(QtCore.QRect(100, 270, 500, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Predkosc_wiatru.setFont(font)
        self.Predkosc_wiatru.setObjectName("Predkosc_wiatru")
        self.kierunek_wiatru = QtWidgets.QLabel(self.centralwidget)
        self.kierunek_wiatru.setGeometry(QtCore.QRect(100, 370, 500, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.kierunek_wiatru.setFont(font)
        self.kierunek_wiatru.setObjectName("kierunek_wiatru")
        self.Wilgotnosc = QtWidgets.QLabel(self.centralwidget)
        self.Wilgotnosc.setGeometry(QtCore.QRect(100, 470, 500, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Wilgotnosc.setFont(font)
        self.Wilgotnosc.setObjectName("Wilgotnosc")
        self.Cisnienie = QtWidgets.QLabel(self.centralwidget)
        self.Cisnienie.setGeometry(QtCore.QRect(100, 570, 500, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.Cisnienie.setFont(font)
        self.Cisnienie.setObjectName("Cisnienie")
        self.Lista = QtWidgets.QListWidget(self.centralwidget)
        self.Lista.setGeometry(QtCore.QRect(640, 120, 331, 521))
        self.Lista.setObjectName("Lista")
        i = 0
        for obiekt in listaStacji:
            self.Lista.insertItem(i, str(list(obiekt.values())[0]))
        self.Lista.clicked.connect(self.zmienStacje)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Stacja.setText(_translate("MainWindow", "STACJA : "))
        self.Data.setText(_translate("MainWindow", "Data Pomiaru: "))
        self.Godzina.setText(_translate("MainWindow", "Godzina Pomiaru:"))
        self.temperatura.setText(_translate("MainWindow", "Temperatura: "))
        self.Predkosc_wiatru.setText(_translate("MainWindow", "Prędkość Wiatru:"))
        self.kierunek_wiatru.setText(_translate("MainWindow", "Kierunek Wiatru:"))
        self.Wilgotnosc.setText(_translate("MainWindow", "Wilgotność Powietrza:"))
        self.Cisnienie.setText(_translate("MainWindow", "Ciśnienie Atmosferyczne:"))
        
    def zmienStacje(self):
        item = self.Lista.currentItem()
        szukana = item.text()
        for find in dane:
            if find['stacja'] == szukana:
                bufor = find 
                self.Stacja.setText("STACJA: "+bufor["stacja"])
                self.Data.setText("Data pomiaru: "+bufor["data_pomiaru"])
                self.Godzina.setText("Godzina pomiaru: "+ bufor["godzina_pomiaru"])
                self.temperatura.setText("Temperatura : "+bufor["temperatura"] + u'\N{DEGREE SIGN}'+"C")
                self.Predkosc_wiatru.setText("Prędkość wiatru: "+bufor["predkosc_wiatru"]+"km/h")
                self.kierunek_wiatru.setText("Kierunek wiatru: "+bufor["kierunek_wiatru"]+u'\N{DEGREE SIGN}')
                self.Wilgotnosc.setText("Wilgotność powietrza: "+bufor["wilgotnosc_wzgledna"]+"%")
                self.Cisnienie.setText("Ciśnienie atmosferyczne: "+str(bufor["cisnienie"])+(" "if str(bufor["cisnienie"]) == "None" else "hPa"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
