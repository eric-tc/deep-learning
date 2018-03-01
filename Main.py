#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui,QtCore
import tensorflow as tf
import sys
from FineTuning import TransferLearning
from Dataset import DatasetCreate



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

        #attraverso il parent, il widget è agganciato alla MainWindow
        super(Tabs,self).__init__(parent)
        self.create_tabs()
        #directory contenente il dataset
        self.directory=None
        self.dataset_create=None




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



        #nome del dataset

        dataset_name_label=QtGui.QLabel("nome dataset")
        self.dataset_name=QtGui.QLineEdit()


        # crop_size

        crop_size_label = QtGui.QLabel("crop size")
        self.crop_size = QtGui.QLineEdit()
        self.crop_size.setValidator(QtGui.QIntValidator())
        self.crop_size.setMaxLength(3)


        # output size

        output_size_label = QtGui.QLabel("dimensione output video")
        self.output_size = QtGui.QLineEdit()
        self.output_size.setValidator(QtGui.QIntValidator())
        self.output_size.setMaxLength(3)


        # COMBOBOX

        video_ext_label=QtGui.QLabel("estensione video")
        self.video_extension = QtGui.QComboBox()

        self.video_extension.addItem(".mov")
        self.video_extension.addItem(".avi")
        self.video_extension.addItem(".mp4")


        # cartella video
        carica_cartella_video = QtGui.QLabel("cartella video")
        self.cartella_video = QtGui.QPushButton('seleziona cartella video')
        self.cartella_video.clicked.connect(self.load_directory_video)



        #framerate dataset
        framerate_label=QtGui.QLabel("framerate")
        self.framerate = QtGui.QLineEdit()
        self.framerate.setValidator(QtGui.QIntValidator())
        self.framerate.setMaxLength(3)

        # button crea dataset
        self.create_dataset_button=QtGui.QPushButton("Crea Dataset")
        self.create_dataset_button.clicked.connect(self.dataset_create_event)





        grid_dataset = QtGui.QGridLayout()

        grid_dataset.setSpacing(20)
        grid_dataset.setAlignment(QtCore.Qt.AlignLeft)



        grid_dataset.addWidget(dataset_name_label,1,0)
        grid_dataset.addWidget(self.dataset_name,1,1)
        grid_dataset.addWidget(crop_size_label,2,0)
        grid_dataset.addWidget(self.crop_size,2,1)

        grid_dataset.addWidget(output_size_label, 3, 0)
        grid_dataset.addWidget(self.output_size, 3, 1)

        grid_dataset.addWidget(video_ext_label, 4, 0)
        grid_dataset.addWidget(self.video_extension, 4, 1)

        grid_dataset.addWidget(carica_cartella_video,5,0)
        grid_dataset.addWidget(self.cartella_video, 5, 1)

        grid_dataset.addWidget(framerate_label, 6, 0)
        grid_dataset.addWidget(self.framerate, 6, 1)

        grid_dataset.addWidget(self.create_dataset_button, 7, 0)


        #self perchè tab1 appartiene alla classe
        self.tab1.setLayout(grid_dataset)

    def training_layout(self):
        """
        
        layout per eseguire il training
        
        :return: 
        """
        #Ottimizzatore
        optimizer_label=QtGui.QLabel('ottimizzatore')

        self.optimizer_cb= QtGui.QComboBox()

        self.optimizer_cb.addItem("Adam")
        self.optimizer_cb.addItem("RmsProp")

        #batch_size
        batch_size_label=QtGui.QLabel('batch_size')
        self.optimizer_cb.setSizePolicy(200,100)

        self.batch_size_validator=QtGui.QLineEdit()
        self.batch_size_validator.setValidator(QtGui.QIntValidator())
        self.batch_size_validator.setMaxLength(3)
        #setta le dimensioni per il widget
        self.batch_size_validator.setSizePolicy(200,100)





        #funzione di loss
        loss_label=QtGui.QLabel('loss')

        self.loss_cb=QtGui.QComboBox()



        self.loss_cb.addItem('categorical_crossentropy')
        self.loss_cb.addItem('binary_crossentropy')
        self.loss_cb.addItem('mean_squared_error')
        self.loss_cb.setSizePolicy(200,100)


        #tipo di training

        training_type_label=QtGui.QLabel('Tipo training')

        self.training_type_cb=QtGui.QComboBox()


        self.training_type_cb.addItem('Transefer Learning')
        self.training_type_cb.addItem('Fine Tuning')
        self.training_type_cb.setSizePolicy(200,100)

        # steps_per_epoch

        steps_per_epoch_label=QtGui.QLabel("numero di steps per epoca")

        self.steps_per_epoch_validator=QtGui.QLineEdit()
        self.steps_per_epoch_validator.setValidator(QtGui.QIntValidator())
        self.steps_per_epoch_validator.setMaxLength(3)
        self.steps_per_epoch_validator.setSizePolicy(200,100)

        #numero di epoche

        epochs_label = QtGui.QLabel("numero di epoche")

        self.number_epoch_validator = QtGui.QLineEdit()
        self.number_epoch_validator.setValidator(QtGui.QIntValidator())
        self.number_epoch_validator.setMaxLength(3)
        self.number_epoch_validator.setSizePolicy(200,100)

        #carica cartella di salvataggio
        carica_cartella_label=QtGui.QLabel("cartella output")
        self.carica_cartella=QtGui.QPushButton('carica cartella')
        self.carica_cartella.clicked.connect(self.load_images)

        #pulsante esegui deep learning

        self.execute_algorithm= QtGui.QPushButton('Esegui')
        self.execute_algorithm.clicked.connect(self.button_event_execute)



        #metrica da visualizzare







        #vertical_box.addStretch(0)


        #layout griglia
        grid =QtGui.QGridLayout()

        grid.setSpacing(20)
        grid.setAlignment(QtCore.Qt.AlignLeft)





        grid.addWidget(optimizer_label,1,0)
        grid.addWidget(self.optimizer_cb,1,1)

        grid.addWidget(batch_size_label,2,0)
        grid.addWidget(self.batch_size_validator,2,1)


        grid.addWidget(loss_label,3,0)
        grid.addWidget(self.loss_cb,3,1)

        grid.addWidget(training_type_label,4,0)
        grid.addWidget(self.training_type_cb,4,1)

        grid.addWidget(steps_per_epoch_label,5,0)
        grid.addWidget(self.steps_per_epoch_validator,5,1)

        grid.addWidget(epochs_label,6,0)
        grid.addWidget(self.number_epoch_validator,6,1)

        grid.addWidget(carica_cartella_label,7,0)
        grid.addWidget(self.carica_cartella,7,1)

        grid.addWidget(self.execute_algorithm)






        #aggiungo il layout alla tabella
        self.tab2.setLayout(grid)




    def button_event_execute(self):
        """
        Inizia il training con i parametri indicati
        
        :return: 
        """
        deep_learning=TransferLearning(training=self.training_type_cb.currentText(),batch_size=int(self.batch_size_validator.text()),
                                       loss=self.loss_cb.currentText(),epochs=int(self.number_epoch_validator.text()),step_per_epoch=int(self.steps_per_epoch_validator.text()),
                                       directory_output=self.directory,optimizer=self.optimizer_cb.currentText())

        #devo eseguire il training in un thread differente altrimenti blocca la GUI
        deep_learning.execute()





    def load_images(self):

        """
        evento pulsante self.load_dataset 
        
        self.directory =  cartella con tutte le immagini da usare per la generazione della rete
        
        :return: 
        """
        self.directory_output=str(QtGui.QFileDialog.getExistingDirectory(self,"Select Directory"))

        print self.directory

    def load_directory_video(self):
        #cartella input video
        self.directory_video=str(QtGui.QFileDialog.getExistingDirectory(self,"Select Directory"))

    def dataset_create_event(self):
        """
        funzione per generare il dataset dai video
        :return: 
        """
        self.dataset_create=DatasetCreate()

        #crea il dataset dai video forniti
        self.dataset_create.create_dataset_from_video(self.directory_video,str(self.dataset_name.text()),int(self.crop_size.text()),int(self.output_size.text()),
                                                      int(self.framerate.text()),self.video_extension.currentText())




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