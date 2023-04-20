from random import randint
import os


def get_random_image():

    numb_photo = randint(0,765)
    numb_dir = randint(0,3)
    percorso = os.listdir("./dataset_nii/dataset")
    diry = percorso[numb_dir]
    inter = os.listdir("./dataset_nii/dataset/"+diry)
    photo = inter[numb_photo]
    pat_abs = os.getcwd()+"/dataset_nii/dataset/"+diry+"/"+photo
    return pat_abs


def random_jpg():
    numb_dir = randint(0,3)
    percorso = os.listdir("./dataset_jpg/Testing")
    diry = percorso[numb_dir]
    inter = os.listdir("./dataset_jpg/Testing/"+diry)
    lunghezza = len(inter)
    numb_photo = randint(0,lunghezza)
    photo = inter[numb_photo]
    pat_abs = os.getcwd()+"/dataset_jpg/Testing/"+diry+"/"+photo
    return pat_abs





