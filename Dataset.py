#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import os
import shutil
from Cache import Cache
from Download import Download


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
        _copy_files(src_paths=self.get_paths(test=False),
                        dst_dir=train_dir,
                        class_numbers=self.class_numbers)

        print("- Copied training-set to:", train_dir)

        # Copy the files for the test-set.
        _copy_files(src_paths=self.get_paths(test=True),
                        dst_dir=test_dir,
                        class_numbers=self.class_numbers_test)

        print("- Copied test-set to:", test_dir)












class DatasetManagement:



    def __init__(self):
        self.data_dir="/Users/Eric/Desktop/eric/Programmazione/python/DeepLearning/data/knifey-spoony"
        self.data_url="https://github.com/Hvass-Labs/knifey-spoony/raw/master/knifey-spoony.tar.gz"
        self.train_dir=os.path.join(self.data_dir,"train/")
        self.test_dir=os.path.join(self.data_dir,"test/")
        self.image_size=200
        self.num_channels=3
        self.img_shape=[self.image_size,self.image_size,self.num_channels]
        self.img_size_flat=self.image_size*self.image_size*self.num_channels
        self.num_classes=3
        self.download=Download()

    def load(self):
       pass

    def execute(self):

        #scarica il dataset da internet se non è presente
        self.download.maybe_downlaod_and_extract(url=self.data_url,download_dir=self.data_dir)

        # crea l'istanza del dataset
        cache_path = os.path.join(self.data_dir, "knifey-spoony.pkl")

        self.dataset = load_cached(cache_path=cache_path, in_dir=self.data_dir)

        #divide i dati in test e train secondo le classi pronti per essere processati

        self.dataset.copy_files(train_dir=self.train_dir,test_dir=self.test_dir)








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