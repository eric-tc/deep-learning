#!/usr/bin/python
# -*- coding: utf-8 -*-

import PIL
import tensorflow as tf
import numpy as np
import os

from tensorflow.python.keras.models import Model,Sequential
from tensorflow.python.keras.layers import Dense,Flatten,Dropout
from tensorflow.python.keras.applications import VGG16
from tensorflow.python.keras.applications.vgg16 import preprocess_input,decode_predictions
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.optimizers import Adam,RMSprop

from Dataset import DatasetManagement


from sklearn.utils.class_weight import compute_class_weight


class TransferLearning:


   # def __init__(self,model,training,train_dir,test_dir,save_to_dir,batch_size,loss,metrics,epochs,step_per_epoch):
    def __init__(self,training,batch_size,optimizer,loss,epochs,step_per_epoch,directory_output):


        #decido se voglio il transfer learning o il fine tuning 2 opzioni 'transfer_learning' 'fine_tuning'
        self.training=training

        self.model = VGG16(include_top=True, weights='imagenet')


        self.class_weights=None

        self.batch_size=batch_size
        if(isinstance(self.batch_size,int)):
            #originale= self.batch_size=self.batch_size
            pass
        else:
            self.error="Batch Size non è un numero"

        if optimizer=="Adam":

            self.optimizer = Adam(lr=1e-5)


        self.loss = 'categorical_crossentropy'

        print self.loss

        self.save_to_dir=directory_output

        self.metrics = ['{}'.format('categorical_accuracy')]

        #numero di epoche *steps_per_epoca=batch_size*numero_training
        self.epochs=epochs
        #numero di training per epoca
        self.step_per_epoch=step_per_epoch







    def path_join(self,dirname,filenames):

        return [os.path.join(dirname, filename) for filename in filenames]

    def execute(self):


        #imposto il dataset
        self.datasetManagement= DatasetManagement()

        self.datasetManagement.execute()

        #setto le path corrette per il Generator di Keras
        self.train_dir=self.datasetManagement.train_dir

        self.test_dir=self.datasetManagement.test_dir



        self.model=VGG16(include_top=True,weights='imagenet')
        #dimensione immagine che richiede il modello utilizzato
        input_shape=self.model.layers[0].output_shape[1:3]

        datagen_train = ImageDataGenerator(
            rescale=1. / 255,
            rotation_range=180,
            width_shift_range=0.1,
            height_shift_range=0.1,
            shear_range=0.1,
            zoom_range=[0.9, 1.5],
            horizontal_flip=True,
            vertical_flip=True,
            fill_mode='nearest'
        )

        datagen_test = ImageDataGenerator(rescale=1. / 255)



        generator_train = datagen_train.flow_from_directory(directory=self.train_dir,
                                                            target_size=input_shape,
                                                            batch_size=20,
                                                            shuffle=True,
                                                            save_to_dir=self.save_to_dir)

        generator_test = datagen_test.flow_from_directory(directory=self.test_dir,
                                                          target_size=input_shape,
                                                          batch_size=self.batch_size,
                                                          shuffle=False)

        step_test = generator_test.n / self.batch_size


        image_paths_train = self.path_join(self.train_dir, generator_train.filenames)
        image_paths_test = self.path_join(self.test_dir, generator_test.filenames)

        # prendo tutte le classi delle immagini presenti nel train e test set
        cls_train = generator_train.classes
        cls_test = generator_test.classes

        # nomi delle classi
        class_names = list(generator_train.class_indices.keys())

        num_classes = generator_train.num_class

        # class weights

        self.class_weight = compute_class_weight(class_weight='balanced',
                                            classes=np.unique(cls_train),
                                            y=cls_train)

        transfer_layer = self.model.get_layer('block5_pool')

        # create a new model in keras
        conv_model = Model(inputs=self.model.input,
                           outputs=transfer_layer.output)

        new_model = Sequential()

        new_model.add(conv_model)

        new_model.add(Flatten())

        new_model.add(Dense(1024, activation='relu'))

        new_model.add(Dropout(0.5))

        new_model.add(Dense(num_classes, activation='softmax'))







        if (self.training == 'transfer_learning'):
            for layer in conv_model.layers:
                layer.trainable = False
        elif (self.training == 'fine_tuning'):
            for layer in conv_model.layers:
                # eseguo il training su tutti i layer del modello
                layer.trainable = True

                # compilazione del modello
        new_model.compile(optimizer=self.optimizer,
                          loss=self.loss,
                          metrics=self.metrics)

        history = new_model.fit_generator(generator=generator_train,
                                          epochs=self.epochs,
                                          steps_per_epoch=self.step_per_epoch,
                                          class_weight=self.class_weight,
                                          validation_data=generator_test,
                                          validation_steps=step_test)



