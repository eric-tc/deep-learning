#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui,QtCore
import tensorflow as tf
import sys
from FineTuning import TransferLearning



class Example(QtGui.QWidget):

    def __init__(self):
        #richiama il metodo init della classe QtGui.QWidget
        super(Example,self).__init__()
        self.init_UI()

    def init_UI(self):


        btn=QtGui.QPushButton("Quit",self)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.resize(btn.sizeHint())
        self.resize(200,300)
        self.move(300,100)
        self.setWindowTitle("prova")
        self.show()

    def closeEvent(self,event):

        reply=QtGui.QMessageBox.question(self,'Message',"are you sure to quit?",QtGui.QMessageBox.Yes|
                                         QtGui.QMessageBox.No,QtGui.QMessageBox.No)

        if reply==QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class MainWindowStatusBar(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindowStatusBar,self).__init__()
        self.initMenuBar()
        self.initStatusBar()
        self.initGeometry()

    def initStatusBar(self):



        self.statusBar().showMessage('Ready')

    def initMenuBar(self):

        exitAction=QtGui.QAction(QtGui.QIcon(""),'&Exit',self)
        exitAction.setStatusTip("Exit Application")
        exitAction.triggered.connect(QtGui.qApp.quit)

        menu_bar=self.menuBar()
        menu_bar.setNativeMenuBar(False)
        fileMenu=menu_bar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def initGeometry(self):
        self.setGeometry(200, 300, 250, 100)
        self.setWindowTitle("Deep Learning")
        self.show()

class LayoutManagement(QtGui.QWidget):

    def __init__(self):

        super(LayoutManagement,self).__init__()
        self.initButton()
        self.initGeometry()

    def initButton(self):

        ok= QtGui.QPushButton('ok',self)
        ok.resize(ok.sizeHint())
        cancel=QtGui.QPushButton('Cancel',self)
        cancel.resize(cancel.sizeHint())

        hbox=QtGui.QHBoxLayout()
        #addStretch aggiunge una separazione fisica dal bordo 1=sposto l'oggetto a destra se ho un box orizzontale
        hbox.addStretch(1)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)

        vbox=QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def initGeometry(self):
        self.setGeometry(200, 300, 250, 100)
        self.setWindowTitle("Deep Learning")
        self.show()

class CustomSignal(QtCore.QObject):

    #definizione di un Custom signal
    closeapp=QtCore.pyqtSignal()

class CustomWindow(QtGui.QMainWindow):

    def __init__(self):
        super(CustomWindow,self).__init__()
        self.initLayout()

    def initLayout(self):

        self.c=CustomSignal()
        #closeapp è il mio custom slot a cui è collegato un evento
        self.c.closeapp.connect(self.close)

        self.setGeometry(200, 300, 250, 100)
        self.setWindowTitle("Deep Learning")
        self.show()

    def mousePressEvent(self, event):

        #closeapp.emit() manda l'evento che è catturato da closeapp.connect(Azione) ed esegue l'azione
        self.c.closeapp.emit()

class DeepLearning(QtGui.QMainWindow):

    def __init__(self):

        super(DeepLearning,self).__init__()
        self.tabs=Tabs(self)

        self.initLayout()

    def initLayout(self):

        self.setGeometry(200, 200, 1366, 768)
        self.setWindowTitle("Deep Learning")
        self.show()


class Tabs(QtGui.QTabWidget):

    def __init__(self,parent):

        #attraverso il parent il widget è agganciato alla MainWindow
        super(Tabs,self).__init__(parent)
        self.create_tabs()
        #directory contenente il dataset
        self.directory=None




    def create_tabs(self):

        """
        Funzione per gestire le caselle di tabs dell'interfaccia
        :return: 
        """
        self.tab1= QtGui.QWidget()
        self.tab2=QtGui.QWidget()
        self.tab3= QtGui.QWidget()
        self.tab4= QtGui.QWidget()

        self.resize(1366,768)

        #Tab 1
        self.dataset_layout()

        #Tab 2
        self.training_layout()




        self.addTab(self.tab1,"Dataset")
        self.addTab(self.tab2,"Training")
        self.addTab(self.tab3,"Results")

    def dataset_layout(self):

        #layout propri del singolo tab
        vBoxLayout = QtGui.QVBoxLayout()

        load_dataset = QtGui.QPushButton("Load")

        # gestione evento pulsante load
        load_dataset.clicked.connect(self.load_images)

        # COMBOBOX

        self.cb = QtGui.QComboBox()

        self.cb.addItem("Inception")
        self.cb.addItem("Vgg16")
        self.cb.addItem("InceptionV3")

        self.cb.currentIndexChanged.connect(self.comboBoxSelection)

        vBoxLayout.addWidget(cb)
        vBoxLayout.addWidget(load_dataset)

        #self perchè tab1 appartiene alla classe
        self.tab1.setLayout(vBoxLayout)

    def training_layout(self):


        optimizer=QtGui.QLabel('ottimizzatore')



        VBoxLayout= QtGui.QVBoxLayout()

        e1= QtGui.QLineEdit()

        e1.setValidator(QtGui.QIntValidator())
        e1.setMaxLength(2)



        VBoxLayout.addWidget(e1)

        self.tab2.setLayout(VBoxLayout)






    def comboBoxSelection(self):
        """
        evento per elemento cliccato dall'utente sulla comboBox
        :return: 
        """
        #architettura selezionata
        self.architecture= self.cb.currentText()

        print self.architecture

    def load_images(self):

        """
        evento pulsante self.load_dataset 
        
        self.directory =  cartella con tutte le immagini da usare per la generazione della rete
        
        :return: 
        """


        self.directory=str(QtGui.QFileDialog.getExistingDirectory(self,"Select Directory"))

        print self.directory




def main():

    app=QtGui.QApplication(sys.argv)

    #ex=Example()
    #status_bar=MainWindowStatusBar()
    #layout_managemnt=LayoutManagement()

    #event=CustomWindow()

    DeepView= DeepLearning()

    #fine_tuning=TransferLearning()

    #fine_tuning.execute()

    sys.exit(app.exec_())

if __name__ == "__main__":

    main()