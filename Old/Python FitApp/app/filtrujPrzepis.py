from PyQt5 import QtCore, QtGui, QtWidgets
from pymongo import MongoClient

class filtrujPrzepis(QtWidgets.QWidget):
    def __init__(self,przepisy):
        self.przepisy = przepisy
        super().__init__()
        self.setObjectName("self")
        self.resize(900, 600)
        self.setMinimumSize(QtCore.QSize(900, 600))
        self.setMaximumSize(QtCore.QSize(900, 600))
        self.setStyleSheet(
            """
            QPushButton{
            background-color: rgba(0,0,0,0);
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
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 901, 601))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Background/ZastosowanieZmian.png"))
        self.label.setObjectName("label")
        self.BialkoInput = QtWidgets.QLineEdit(self)
        self.BialkoInput.setGeometry(QtCore.QRect(290, 100, 341, 51))
        self.BialkoInput.setObjectName("BialkoInput")
        self.KalorieInput = QtWidgets.QLineEdit(self)
        self.KalorieInput.setGeometry(QtCore.QRect(290, 210, 341, 51))
        self.KalorieInput.setObjectName("KalorieInput")
        self.TluszczInput = QtWidgets.QLineEdit(self)
        self.TluszczInput.setGeometry(QtCore.QRect(290, 330, 341, 51))
        self.TluszczInput.setObjectName("TluszczInput")
        self.WegleInput = QtWidgets.QLineEdit(self)
        self.WegleInput.setGeometry(QtCore.QRect(290, 440, 341, 51))
        self.WegleInput.setObjectName("WegleInput")
        self.ZastosujButton = QtWidgets.QPushButton(self)
        self.ZastosujButton.setGeometry(QtCore.QRect(260, 510, 401, 71))
        self.ZastosujButton.setText("")
        self.ZastosujButton.setObjectName("ZastosujButton")
        self.ZastosujButton.clicked.connect(self.find_products)

    def find_products(self):
        kalorie = self.KalorieInput.text()
        tluszcz = self.TluszczInput.text()
        wegle = self.WegleInput.text()
        bialko = self.BialkoInput.text()
        if len(kalorie) == 0:
            kalorie = "0"
        if len(tluszcz) == 0:
            tluszcz = "0"
        if len(wegle) == 0:
            wegle = "0"
        if len(bialko) == 0:
            bialko = "0"
            
        if kalorie.isdigit() and tluszcz.isdigit() and wegle.isdigit() and bialko.isdigit(): 
            list_find = self.przepisy.findChildren(QtWidgets.QListWidget,"lista")[0]
            list_find.clear()   
            self.client = MongoClient('localhost', 27017)
            self.db = self.client['Fitatu']
            self.collection = self.db['przepisy']
            query = {
                '$and': [
                    {'bialko': {'$gt': int(bialko)}},
                    {'tluszcz': {'$gt': int(tluszcz)}},
                    {'kalorie': {'$gt': int(kalorie)}},
                    {'weglowodany': {'$gt': int(wegle)}}
                    
                ]
            }
            result = self.collection.find(query)
            for single in result:
                name = single["nazwa"]
                list_find.insertItem(0,name)
            self.przepisy.overlay.deleteLater()
            self.przepisy.setEnabled(True)
            self.client.close()
            self.close()




    def closeEvent(self,event):
        self.przepisy.overlay.deleteLater()
        self.przepisy.setEnabled(True)
        self.close()

