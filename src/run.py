import cv2
import numpy as np
import h5py
import matplotlib.pyplot as plt
import warnings
from datetime import datetime

#NOTE: import scripts from src folder for skull stripping and tumor detection
#from src.skullstripping import get_random_image
from src.skullstripping import skull_stripping
from src.skullstripping import strong_skull_stripping
from src.tumordetection import get_mean_color_tumor
from src.tumordetection import find_tumor

warnings.filterwarnings("ignore")

'''
#TODO:
'''
def get_contourn_external(brain):
    j = brain.copy()
    for i in range(0,brain.shape[0]):
        for y in range(0,brain.shape[1]):
            if j[i][y] != 0:
                j[i][y] = 255
    contours, hierarchy = cv2.findContours(j,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    countour = max(contours, key=cv2.contourArea)
    area_contorno_esterno = cv2.contourArea(countour)
    return area_contorno_esterno
'''
#TODO:
'''
def get_contourn_external_withBord(brain):
    j = brain.copy()
    j[j == 255]  = 0 
    j[j <=7] = 0
    for i in range(0,brain.shape[0]):
        for y in range(0,brain.shape[1]):
            if j[i][y] != 0:
                j[i][y] = 255
    contours, hierarchy = cv2.findContours(j,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    countour = max(contours, key=cv2.contourArea)
    area_contorno_esterno = cv2.contourArea(countour)
    return area_contorno_esterno
'''
#TODO:
'''
def get_perimetro_external(brain):
    j = brain.copy()
    for i in range(0,brain.shape[0]):
        for y in range(0,brain.shape[1]):
            if j[i][y] != 0:
                j[i][y] = 255
    contours, hierarchy = cv2.findContours(j,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    countour = max(contours, key=cv2.contourArea)
    perimetro_contorno_esterno = cv2.arcLength(countour,True)
    return perimetro_contorno_esterno
'''
#TODO:
#NOTE: update the path to the tmp folder
'''
def load_image_nii(input):
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
    dir = './tmp/input'
    #dir = '/Users/lucian/Documents/GitHub/BrainCancerSegmentation/tmp/input'
    now = datetime.now()
    file_name = now.strftime("%H:%M:%S")
    t = f"{file_name}.png"
    path = dir + "/" + t
    plt.imsave(path, image, cmap='gray')
    return path
'''
Main entry point for the brain cancer segmentation script
'''
def main(image):
    if image.endswith('.mat'):
        path = load_image_nii(image)
    else:
        path = image
    tupla_return = skull_stripping.get_brain(path)
    brain = tupla_return[1]
    value = tupla_return[0]
    indice_medio = tupla_return[2]
    color = -1
    if value == -1:
        #NOTE: First skull striping failed, try with strong skull stripping
        tupla_return = strong_skull_stripping.strong_skull(brain)
        brain = tupla_return[1]
        value = tupla_return[0]
        indice_medio = tupla_return[2]
        if value == -1:
            #NOTE: Second skull striping failed
            pass
        else:
            area_contorno_esterno = get_contourn_external(brain)
            perimetro_contorno_esterno = get_perimetro_external(brain)
            #NOTE: second skull stripping success, show the brain
            tup = get_mean_color_tumor.get_color(brain, indice_medio, area_contorno_esterno)
            color = tup[0]
            segm = tup[1]
            my_pixel = tup[2]
            area_contorno_esterno = tup[3]
            colore_cervello = tup[4]
    elif value == 1:
        area_contorno_esterno = get_contourn_external(brain)
        perimetro_contorno_esterno = get_perimetro_external(brain)
        #NOTE: First skull striping success, show the brain
        tup = get_mean_color_tumor.get_color(brain, indice_medio, area_contorno_esterno)
        color = tup[0]
        segm = tup[1]
        my_pixel = tup[2]
        area_contorno_esterno = tup[3]
        colore_cervello = tup[4]
    elif value == 2:
        area_contorno_esterno = get_contourn_external(brain)
        #NOTE: First skull stripping successs, show the brain, but there is a lot of border
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
            #NOTE: Tumor found!
            maschera  = np.zeros(img.shape, np.uint8)
            cv2.drawContours(img, [contorno], -1, (0, 255, 0), 3)
            area = cv2.contourArea(contorno)
            area_relativa = area/area_contorno_esterno
            maschera = cv2.cvtColor(maschera, cv2.COLOR_BGR2GRAY)
            cv2.drawContours(maschera, [contorno], -1, 255, -1)
            copia = cv2.cvtColor(copia, cv2.COLOR_BGR2GRAY)
            my_tumor = cv2.bitwise_and(copia, maschera) 
            return img, probabilita, area_relativa
        except:
            #NOTE: Tumor not found
            return copia

    else:
        #NOTE: Error in skull stripping
        copia = cv2.cvtColor(copia, cv2.COLOR_BGR2GRAY)
        area_contorno_esterno = get_contourn_external_withBord(copia)  
        perimetro_contorno_esterno = get_perimetro_external(copia)
        indice_medio=-1
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
            #NOTE: Tumor found!
            maschera  = np.zeros(img.shape, np.uint8)
            cv2.drawContours(img, [contorno], -1, (0, 255, 0), 3)
            area = cv2.contourArea(contorno)
            area_relativa = area/area_contorno_esterno
            return img, probabilita, area_relativa
        except:
            #NOTE: Tumor not found
            return copia
