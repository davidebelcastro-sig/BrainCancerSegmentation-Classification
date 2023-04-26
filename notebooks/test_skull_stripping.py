import os
import matplotlib.pyplot as plt
import h5py
from skull_stripping import get_brain
from strong_skull_stripping import strong_skull
import csv
import cv2
import numpy as np




def test_nii(path,numb):
    totali = 0
    ok = 0
    maggiore = 0
    errata = 0
    dataset = os.listdir(path)
    for file in dataset:
        f = h5py.File(path + "/" + file, 'r')
        for el in f['cjdata']:
            if el == 'image':
                image = f['cjdata'][el]
        plt.imshow(image,cmap='gray')
        plt.axis('off')
        plt.savefig('brain'+numb+'.png')
        tupla = get_brain('brain'+numb+'.png')
        mask = tupla[0]
        foto = tupla[1]
        if mask == 1:
            ok += 1
        elif mask == 2:
            maggiore += 1
        elif mask == -1:
            tupla = strong_skull(foto)
            result = tupla[0]
            if result == 1:
                ok += 1
            else:
                 errata += 1
        totali += 1
        if totali % 50 == 0:
            print("Analizzati ", totali, " elementi")

    print("Analisi completata")
    perc_ok =       (ok / totali) * 100
    perc_maggiore = (maggiore / totali) * 100
    perc_errata =   (errata / totali) * 100
    #scrivo su file i valori trovati
    with open('./attendibilità_skull_stripping_'+ numb +'.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([path, str(ok), str(maggiore), str(errata), str(perc_ok) + "%", str(perc_maggiore) + "%", str(perc_errata) + "%", str(totali)])



def test_jpg(path):
    totali = 0
    ok = 0
    maggiore = 0
    errata = 0
    dataset = os.listdir(path)
    for file in dataset:
        tupla = get_brain(path + "/" + file)
        mask = tupla[0]
        foto = tupla[1]
        if mask == 1:
            ok += 1
        elif mask == 2:
            maggiore += 1
        elif mask == -1:
            tupla = strong_skull(foto)
            result = tupla[0]
            if result == 1:
                ok += 1
            else:
                 errata += 1
        totali += 1
        if totali % 50 == 0:
            print("Analizzati ", totali, " elementi")

    print("Analisi completata")
    perc_ok =       (ok / totali) * 100
    perc_maggiore = (maggiore / totali) * 100
    perc_errata =   (errata / totali) * 100
    #scrivo su file i valori trovati
    with open('./attendibilità_skull_stripping.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([path, str(ok), str(maggiore), str(errata), str(perc_ok) + "%", str(perc_maggiore) + "%", str(perc_errata) + "%", str(totali)])



if __name__ == '__main__':
    path = input("Inserisci il path del dataset: ")
    numb = input("Inserire numero cartella:")
    test_nii(path,numb)
    #test_jpg("../dataset_jpg/Testing/glioma_tumor")
