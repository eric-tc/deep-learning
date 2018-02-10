#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import urllib
import tarfile
import zipfile

class Download:
    """
    classe per gestire i download del dataset
    
    """

    def __init__(self):

        pass

    def maybe_downlaod_and_extract(self,url,download_dir):

        """
        
        :param url: url per scaricare il dataset 
        :param download_dir: Cartella dove sono salvati i file scaricati
        :return: 
        """


        filename= url.split('/')[-1]
        #path alla cartella dove salverò il dataset
        file_path=os.path.join(download_dir,filename)

        if not os.path.exists(file_path):

            #verfico se esiste la cartella di download
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

        #downlaod the file from the internet

            file_path, =urllib.urlretrieve(url=url,
                                               filename=file_path,
                                               reporthook=self._print_download_progress)


            if file_path.endswith(".zip"):
                zipfile.ZipFile(file=file_path,mode="r").extractall(download_dir)
            elif file_path.endswith((".tar.gz",".tgz")):
                tarfile.open(name=file_path,mode="r:gz").extractall(download_dir)

        else:
            print ("I dati sembrano essere già stati scaricati")


    def _print_download_progress(self,count, block_size, total_size):
        """
        Function used for printing the download progress.
        Used as a call-back function in maybe_download_and_extract().
        """

        # Percentage completion.
        pct_complete = float(count * block_size) / total_size

        # Status-message. Note the \r which means the line should overwrite itself.
        msg = "\r- Download progress: {0:.1%}".format(pct_complete)

        # Print it.
        sys.stdout.write(msg)
        sys.stdout.flush()