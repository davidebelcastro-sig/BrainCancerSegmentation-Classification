import cv2
import numpy as np
from skullstripping import get_random_image
from skullstripping import skull_stripping
from skullstripping import strong_skull_stripping
from tumordetection import get_mean_color_tumor
from tumordetection import find_tumor
import h5py
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import os 
from PIL import Image
from datetime import datetime

def get_contourn_external(brain):
    j = brain.copy()
    for i in range(0,brain.shape[0]):
        for y in range(0,brain.shape[1]):
            if j[i][y] != 0:
                j[i][y] = 255

    #find contours
    contours, hierarchy = cv2.findContours(j,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #disegno il piu grande contorno
    countour = max(contours, key=cv2.contourArea)
    #disegno contorno
    area_contorno_esterno = cv2.contourArea(countour)
    return area_contorno_esterno

def get_contourn_external_withBord(brain):
    j = brain.copy()
    j[j == 255]  = 0 
    j[j <=7] = 0
    for i in range(0,brain.shape[0]):
        for y in range(0,brain.shape[1]):
            if j[i][y] != 0:
                j[i][y] = 255

    #find contours
    contours, hierarchy = cv2.findContours(j,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #disegno il piu grande contorno
    countour = max(contours, key=cv2.contourArea)
    #disegno contorno
    area_contorno_esterno = cv2.contourArea(countour)
    return area_contorno_esterno

def get_perimetro_external(brain):
    j = brain.copy()
    for i in range(0,brain.shape[0]):
        for y in range(0,brain.shape[1]):
            if j[i][y] != 0:
                j[i][y] = 255

    #find contours
    contours, hierarchy = cv2.findContours(j,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #disegno il piu grande contorno
    countour = max(contours, key=cv2.contourArea)
    #disegno contorno
    perimetro_contorno_esterno = cv2.arcLength(countour,True)
    return perimetro_contorno_esterno

def load_image_nii(input):
    #path = get_random_image.get_random_image()  #load an random image
    #ls = path.split("/")
    #nome_imma = ls[-1]
    #nome_dir  = ls[-2]
    #variable = "./dataset_nii/dataset/"+nome_dir+"/"+nome_imma
    f = h5py.File(input, 'r')
    for el in f['cjdata']:
        if el == 'image':
            image = f['cjdata'][el]
        elif el == 'label':
            label = f['cjdata'][el]
            label = label[0][0]
            label = int(label)
            label = str(label)
        elif el == 'tumorMask':
            border = f['cjdata'][el]
    # /Users/lucian/Documents/GitHub/BrainCancerDetection/tmp/input

    dir = '/Users/lucian/Documents/GitHub/BrainCancerDetection/tmp/input'
    now = datetime.now()
    file_name = now.strftime("%H:%M:%S")
    t = f"{file_name}.png"
    path = dir + "/" + t

    plt.imsave(path, image, cmap='gray')
  
    return path

def load_image_jpg():
    path = get_random_image.random_jpg()  #load an random image
    ls = path.split("/")
    nome_imma = ls[-1]
    nome_dir  = ls[-2]
    variable = "./dataset_jpg/Testing/"+nome_dir+"/"+nome_imma
    return variable


def main(image):
    input = image
    path = load_image_nii(input)
    tupla_return = skull_stripping.get_brain(path)
    brain = tupla_return[1]
    value = tupla_return[0]
    indice_medio = tupla_return[2]

    #show image
    color = -1

    if value == -1:
        print("FIRST SKULL STRIPPING FAILED:   try with strong skull stripping")
        tupla_return = strong_skull_stripping.strong_skull(brain)
        brain = tupla_return[1]
        value = tupla_return[0]
        indice_medio = tupla_return[2]
        if value == -1:
            print("SECOND SKULL STRIPPING FAILED")
        else:
            area_contorno_esterno = get_contourn_external(brain)
            perimetro_contorno_esterno = get_perimetro_external(brain)
            print("SECOND SKULL STRIPPING SUCCESS: show the brain")
            tup = get_mean_color_tumor.get_color(brain, indice_medio, area_contorno_esterno)
            color = tup[0]
            segm = tup[1]
            my_pixel = tup[2]
            area_contorno_esterno = tup[3]
            colore_cervello = tup[4]
    elif value == 1:
        area_contorno_esterno = get_contourn_external(brain)
        perimetro_contorno_esterno = get_perimetro_external(brain)
        print("FIRST SKULL STRIPPING SUCCESS: show the brain")
        #ho solo il cervello
        tup = get_mean_color_tumor.get_color(brain, indice_medio, area_contorno_esterno)
        color = tup[0]
        segm = tup[1]
        my_pixel = tup[2]
        area_contorno_esterno = tup[3]
        colore_cervello = tup[4]
    elif value == 2:
        area_contorno_esterno = get_contourn_external(brain)
        print("FIRST SKULL STRIPPING SUCCESS: show the brain, but there is a lot of border:   show the brain with a lot of border")
        #ho cervello + bordo
        tup = get_mean_color_tumor.get_color(brain, indice_medio, area_contorno_esterno)
        color = tup[0]
        segm = tup[1]
        my_pixel = tup[2]
        area_contorno_esterno = tup[3]
        colore_cervello = tup[4]

    img = cv2.imread(path)
    copia = img.copy()
    if color != -1:
        result = find_tumor.get_tumor(color,brain,segm,my_pixel,area_contorno_esterno,colore_cervello)
        contorno = result[0]
        probabilita = result[1]*100
        try:
            maschera  = np.zeros(img.shape, np.uint8)
            cv2.drawContours(img, [contorno], -1, (0, 255, 0), 3)
            print("TUMOR FOUND")
            #download_image(copia, img)
            #cv2.imshow("initial", copia)
            #cv2.imshow("tumor", img)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            print("PROBABILITA' TUMORE: ",str(probabilita),"%")
            #area rispetto alla foto
            area = cv2.contourArea(contorno)
            #area rispetto al contorno esterno
            area_relativa = area/area_contorno_esterno
            print("AREA TUMORE: ",str(area_relativa*100),"%")
            maschera = cv2.cvtColor(maschera, cv2.COLOR_BGR2GRAY)
            cv2.drawContours(maschera, [contorno], -1, 255, -1)
            copia = cv2.cvtColor(copia, cv2.COLOR_BGR2GRAY)
            my_tumor = cv2.bitwise_and(copia, maschera)  #prendo solo il tumore,sfondo nero
            #cv2.imshow("tumor", my_tumor)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            return img, probabilita, area_relativa

        except:
            print("NO TUMOR FOUND")
            return copia
            #cv2.imshow("initial", copia)
            #cv2.imshow("no tumor", copia)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()

    else:
        print("Putroppo non riuscito a estrapolare il cervello eliminando i bordi,provo comunque ad effettuare l'analisi")
        #scala di grio
        copia = cv2.cvtColor(copia, cv2.COLOR_BGR2GRAY)
        area_contorno_esterno = get_contourn_external_withBord(copia)  #immagine originale
        perimetro_contorno_esterno = get_perimetro_external(copia)
        indice_medio=-1
        #devo trovare indice medio-> prendo i pixel con maggior frequenza che non siano sotto 30 e non siano sopra 200
        histo = cv2.calcHist([copia], [0], None, [256], [0, 256])
        mass = -1
        for i in range(0, 256):
            if i > 30 and i < 200:
                if histo[i] > mass:
                    mass = histo[i]
                    indice_medio = i
        
        tup = get_mean_color_tumor.get_color(copia, indice_medio, area_contorno_esterno)
        color = tup[0]
        segm = tup[1]
        my_pixel = tup[2]
        area_contorno_esterno = tup[3]
        colore_cervello = tup[4]
        result = find_tumor.get_tumor(color,copia,segm,my_pixel,area_contorno_esterno,colore_cervello)
        contorno = result[0]
        probabilita = result[1]*100
        copia = cv2.cvtColor(copia, cv2.COLOR_GRAY2BGR)
        try:
            maschera  = np.zeros(img.shape, np.uint8)
            cv2.drawContours(img, [contorno], -1, (0, 255, 0), 3)
            print("TUMOR FOUND")
            print("PROBABILITA' TUMORE: ",str(probabilita),"%")
            #area rispetto alla foto
            area = cv2.contourArea(contorno)
            #area rispetto al contorno esterno
            area_relativa = area/area_contorno_esterno
            print("AREA TUMORE: ",str(area_relativa*100),"%")
            return img, probabilita, area_relativa
        except:
            print("NO TUMOR FOUND")
            return copia