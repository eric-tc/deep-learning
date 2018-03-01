#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import os
import shutil
from Cache import Cache
from Download import Download
import subprocess
import argparse



def one_hot_encoded(class_numbers, num_classes=None):
    """
    Generate the One-Hot encoded class-labels from an array of integers.
    For example, if class_number=2 and num_classes=4 then
    the one-hot encoded label is the float array: [0. 0. 1. 0.]
    :param class_numbers:
        Array of integers with class-numbers.
        Assume the integers are from zero to num_classes-1 inclusive.
    :param num_classes:
        Number of classes. If None then use max(class_numbers)+1.
    :return:
        2-dim array of shape: [len(class_numbers), num_classes]
    """

    # Find the number of classes if None is provided.
    # Assumes the lowest class-number is zero.
    if num_classes is None:
        num_classes = np.max(class_numbers) + 1

    return np.eye(num_classes, dtype=float)[class_numbers]


class Dataset:

    def __init__(self,in_dir,exts='.jpg'):

        # full-path della cartella di input
        in_dir=os.path.abspath(in_dir)

        self.in_dir=in_dir

        # converto tutte le estensioni al carattere minuscolo
        self.exts=tuple(ext.lower() for ext in exts)

        # Nomi per le classi
        self.class_names= []

        # tutti i nomi dei file nel training set
        self.filenames=[]

        # nomi dei file nel test set
        self.filenames_test=[]

        # classe di ogni elemento nel training set
        self.class_numbers=[]

        # classe di ogni elemento nel test set
        self.class_numbers_test=[]

        # numero totale di classi nel data-set
        self.num_classes=0

        # istanza per il downlaod
        self.download=Download()


        #ritorna tutti i nomi dentro alla cartella
        for name in os.listdir(in_dir):

            current_dir= os.path.join(in_dir,name)

            if os.path.isdir(current_dir):

                self.class_names.append(name)

                #training set

                filenames=self._get_filenames(current_dir)

                self.filenames.extend(filenames)

                class_number=self.num_classes

                class_numbers=[class_number]*len(filenames)

                self.class_numbers.extend(class_numbers)

                #test-set

                filenames_test=self._get_filenames(os.path.join(current_dir,'test'))

                self.filenames_test.extend(filenames_test)

                class_numbers=[class_number]*len(filenames_test)

                self.class_numbers_test.extend(class_numbers)

                self.num_classes += 1




    def _get_filenames(self,dir):
        """
        
        :param dir:cartella di input immagini 
        :return: ritorna tutti i file che finiscono con self.exts
        """
        filenames=[]

        if os.path.isdir(dir):
            for filename in os.listdir(dir):
                if filename.lower().endswith(self.exts):
                    filenames.append(filename)

        return filenames


    def get_paths(self,test=False):
        """
        Funzione per trovare la full path per i file
        :param test: 
        :return: 
        """

        if test:

            filenames= self.filenames_test
            class_numbers=self.class_numbers_test

            test_dir='test/'

        else:
            filenames=self.filenames
            class_numbers=self.class_numbers

            test_dir=''

        for filename,cls in zip(filenames,class_numbers):

            #sto creando un generatore variabile(val1,val2,val3,val4)
            path=os.path.join(self.in_dir,self.class_names[cls],test_dir,filename)

            #yield è utilizzato quando una funzione ritorna un generatore
            yield path


    def get_training_dataset(self):

        return list(self.get_paths()),\
               np.asarray(self.class_numbers),\
               one_hot_encoded(class_numbers=self.class_numbers,num_classes=self.num_classes)


    def get_test_dataset(self):

        return list(self.get_paths(test=True)), \
               np.asarray(self.class_numbers_test), \
               one_hot_encoded(class_numbers=self.class_numbers_test,
                               num_classes=self.num_classes)


    def copy_files(self,train_dir,test_dir):

        """
    
        Copy all the files in the training-set to train_dir
        and copy all the files in the test-set to test_dir.
        :param train_dir: directory dove si trovano le immagini di training
        :param test_dir: directory dove si trovano le immagini di test
        :return: 
        """

        def _copy_files(src_paths,dst_dir,class_numbers):

            """
            Creo una lista di directory per ogni classe
            (knify-spoony/test/class1)
            (knify-spoony/test/class2)
            
            
            :param src_paths: 
            :param dst_dir: 
            :param class_numbers: 
            :return: 
            """

            class_dirs=[os.path.join(dst_dir,class_name+"/")for class_name in self.class_names]

            for dir in class_dirs:
                if not os.path.exists(dir):
                    os.makedirs(dir)

            for src,cls in zip(src_paths,class_numbers):
                shutil.copy(src=src,dst=class_dirs[cls])

        # Copy the files for the training-set.
        #self.get_paths ritorna i path delle immagini da copiare nel training set test=False
        _copy_files(src_paths=self.get_paths(test=False),
                        dst_dir=train_dir,
                        class_numbers=self.class_numbers)

        print("- Copied training-set to:", train_dir)

        # Copy the files for the test-set.
        #test=True ritorna tutte le path del test
        _copy_files(src_paths=self.get_paths(test=True),
                        dst_dir=test_dir,
                        class_numbers=self.class_numbers_test)

        print("- Copied test-set to:", test_dir)












class DatasetManagement:



    def __init__(self):

        """
        Classe per gestire la copia dei dati da una forma
        /dataset/class1/
        /dataset/class1/test
        To
        /train/class1
        test/class2
        """
        #variabile dove si trova il dataset
        self.data_dir="/Users/Eric/Desktop/eric/Programmazione/python/DeepLearning/data/knifey-spoony"
        #Url dove posso scaricare un dataset
        self.data_url="https://github.com/Hvass-Labs/knifey-spoony/raw/master/knifey-spoony.tar.gz"
        #path della cartella di train
        self.train_dir=os.path.join(self.data_dir,"train/")
        #path della cartella di test
        self.test_dir=os.path.join(self.data_dir,"test/")
        #dimensione immagine
        self.image_size=200
        #canali immagine
        self.num_channels=3
        self.img_shape=[self.image_size,self.image_size,self.num_channels]
        self.img_size_flat=self.image_size*self.image_size*self.num_channels
        #numero di classi del dataset
        self.num_classes=3
        self.download=Download()

    def load(self):
       pass

    def execute(self):

        #gestione caricamento dataset da internet o da locale

        #scarica il dataset da internet se non è presente
        self.download.maybe_downlaod_and_extract(url=self.data_url,download_dir=self.data_dir)

        # crea l'istanza del dataset
        cache_path = os.path.join(self.data_dir, "knifey-spoony.pkl")

        self.dataset = load_cached(cache_path=cache_path, in_dir=self.data_dir)

        #divide i dati in test e train secondo le classi pronti per essere processati

        self.dataset.copy_files(train_dir=self.train_dir,test_dir=self.test_dir)



class DatasetCreate:
    """
    classe utilizzata per creare dai singoli video una struttura
    
    dataset_name/class1
    dataset_name/class1/test
    
    che verrà utilizzata dalla classe DatasetManagement per creare la struttura 
    test/class1
    train/class1
    necessaria per il training con Keras e i generator
    
    """


    def __init__(self):
        """
        
        :param output_dir:cartella di output del dataset 
        """
        pass

    def create_dataset_from_video(self, in_dir,output_dir, crop_size, out_size, framerate, video_exts):

        """

        :param in_dir: cartella dove sono contenuti i video
        :param crop_size: ridimensionamento dei frame del video
        :param out_size: dimensione del video dopo il ridimensionamento
        :param framerate: Numero di frame da prendere per secondo
        :param video_exts: tipo di estensione del video
        :return:
         
         
        """

        # converte le estensione dei video con minuscole
        #posso evitare di mettere il controllo se i valori li seleziono io da menù a tendina
        #video_exts = tuple(ext.lower() for ext in video_exts)

        in_dir=in_dir+"/"
        video_counts = 0
        print "cartella input"
        print in_dir

        for current_dir, dir_names, file_names in os.walk(in_dir):

            relative_path = os.path.relpath(current_dir,in_dir)
            print relative_path
            print output_dir

            new_dir = os.path.join(output_dir, relative_path)

            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

            for file_name in file_names:
                if file_name.lower().endswith(video_exts):
                    in_file = os.path.join(current_dir, file_name)

                    file_root, file_ext = os.path.splitext(file_name)

                    new_file_name = file_root + "-%4d.jpg"

                    new_file_path = os.path.join(new_dir, new_file_name)

                    new_file_path = os.path.normpath(new_file_path)

                    cmd = "avconv -i {0} -r {1} -vf crop={2}:{2} -vf scale={3}:{3} -qscale 2 {4}"

                    cmd = cmd.format(in_file, framerate, crop_size, out_size, new_file_path)
                    subprocess.call(cmd, shell=True)
                    video_counts += 1
        print ("Number of videos converted: {0}".format(video_counts))



def load_cached(cache_path, in_dir):
    """
    Wrapper-function for creating a DataSet-object, which will be
    loaded from a cache-file if it already exists, otherwise a new
    object will be created and saved to the cache-file.
    This is useful if you need to ensure the ordering of the
    filenames is consistent every time you load the data-set,
    for example if you use the DataSet-object in combination
    with Transfer Values saved to another cache-file, see e.g.
    Tutorial #09 for an example of this.
    :param cache_path:
        File-path for the cache-file.
    :param in_dir:
        Root-dir for the files in the data-set.
        This is an argument for the DataSet-init function.
    :return:
        The DataSet-object.
    """

    print("Creating dataset from the files in: " + in_dir)

    # If the object-instance for DataSet(in_dir=data_dir) already
    # exists in the cache-file then reload it, otherwise create
    # an object instance and save it to the cache-file for next time.

    cache=Cache()
    dataset = cache.cache_data(cache_path=cache_path,
                    fn=Dataset, in_dir=in_dir)

    return dataset