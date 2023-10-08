import cv2
import numpy as np
from skimage.metrics import structural_similarity 
from ..src.skullstripping.skull_stripping import get_brain
from ..src.skullstripping.strong_skull_stripping import strong_skull
from ..src.tumordetection import get_mean_color_tumor
from ..src.tumordetection  import find_tumor
import h5py
import matplotlib.pyplot as plt
import os
import csv



'''
return the difference between two images
'''
def confronta_img(img1,img2):
   (p,d) = structural_similarity(img1, img2, full=True) #p è la percentuale di somiglianza, d è la matrice di differenza
   return p


'''
return the countourn of the brain with border
'''
def get_contourn_external_withBord(brain):
    j = brain.copy()
    j[j == 255]  = 0 
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


'''
return the countorn of the brain without border
'''
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


'''
return the perimeter of the brain
'''
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


'''
start the test
'''
def run(percorso):
    totali = 0
    ok = 0
    errata = 0
    dataset = os.listdir(percorso)
    fatte = 0
    for file in dataset:
        totali += 1
        if fatte == 200:
            break
        if fatte % 10 == 0:
            print("fatte",fatte)
        fatte += 1
        f = h5py.File(percorso + "/" + file, 'r')
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
            elif el  == 'tumorBorder':
                tumore_maschera = f['cjdata'][el]
        plt.imshow(image,cmap='gray')
        plt.axis('off')
        plt.savefig('brain.png')
        #show tumor on brain
        plt.imshow(border,cmap='gray')
        plt.axis('off')
        plt.savefig('tumor.png')

        #show tumor on brain
        plt.imshow(image,cmap='gray')
        plt.imshow(border,cmap='jet',alpha=0.5)  
        plt.savefig('tumor_on_brain.png')
        plt.axis('on')
        bord = cv2.imread('tumor.png')
        img = cv2.imread('brain.png')  #3 canali

        bord = cv2.cvtColor(bord, cv2.COLOR_BGR2GRAY)
        #find contours
        contours, hierarchy = cv2.findContours(bord,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #sorted
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        #terzo
        cnt = contours[2]
        mask_appo = np.zeros_like(bord)
        cv2.drawContours(mask_appo, [cnt], -1, 255, -1)
        bord = mask_appo
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        only_tumor = cv2.bitwise_and(img, bord)  #prendo solo il tumore,sfondo nero
        path = 'brain.png'
        tupla_return = get_brain(path)
        brain = tupla_return[1]
        value = tupla_return[0]
        indice_medio = tupla_return[2]

        #show image
        color = -1


        if value == -1:
            print("FIRST SKULL STRIPPING FAILED:   try with strong skull stripping")
            tupla_return = strong_skull(brain)
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
        appo = copia.copy()
        if color != -1:
            result = find_tumor.get_tumor(color,brain,segm,my_pixel,area_contorno_esterno,colore_cervello)
            contorno = result[0]
            probabilita = result[1]
            try:
                maschera  = np.zeros(img.shape, np.uint8)
                maschera = cv2.cvtColor(maschera, cv2.COLOR_BGR2GRAY)
                cv2.drawContours(maschera, [contorno], -1, 255, -1)
                appo = cv2.cvtColor(appo, cv2.COLOR_BGR2GRAY)
                my_tumor = cv2.bitwise_and(appo, maschera)  #prendo solo il tumore,sfondo nero
                p = confronta_img(only_tumor,my_tumor)
                if p >= 0.97:
                    ok+=1
                else:
                    errata += 1
                    cv2.imwrite('./tumori_errati/brain'+str(errata)+'.png',img)
                    tumor_mask = cv2.imread("tumor_on_brain.png")
                    cv2.imwrite('./tumori_errati/tumor_mask'+str(errata)+'.png',tumor_mask)
                

            except:
               errata += 1
               cv2.imwrite('./tumori_errati/brain'+str(errata)+'.png',img)
               tumor_mask = cv2.imread("tumor_on_brain.png")
               cv2.imwrite('./tumori_errati/tumor_mask'+str(errata)+'.png',tumor_mask)

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
            probabilita = result[1]
            try:

                maschera  = np.zeros(img.shape, np.uint8)
                maschera = cv2.cvtColor(maschera, cv2.COLOR_BGR2GRAY)
                cv2.drawContours(maschera, [contorno], -1, 255, -1)
                appo = cv2.cvtColor(appo, cv2.COLOR_BGR2GRAY)
                my_tumor = cv2.bitwise_and(appo, maschera)  #prendo solo il tumore,sfondo nero
                p = confronta_img(only_tumor,my_tumor)
                if p >= 0.97:
                    ok+=1
                else:
                    errata += 1
                    cv2.imwrite('./tumori_errati/brain'+str(errata)+'.png',img)
                    tumor_mask = cv2.imread("tumor_on_brain.png")
                    cv2.imwrite('./tumori_errati/tumor_mask'+str(errata)+'.png',tumor_mask)
            except:
               errata += 1
               cv2.imwrite('./tumori_errati/brain'+str(errata)+'.png',img)
               tumor_mask = cv2.imread("tumor_on_brain.png")
               cv2.imwrite('./tumori_errati/tumor_mask'+str(errata)+'.png',tumor_mask)
    
    #scrivo su file csv
    perc_ok = (ok/totali)*100
    perc_errata = (errata/totali)*100
    with open('./test_tumor_detection_forma/attendibilità_tumor_detection.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([percorso, str(ok), str(errata), str(perc_ok) + "%", str(perc_errata) + "%", str(totali)])







if __name__ == '__main__':
    run("./dataset_nii/dataset/brainTumorDataPublic_1-766")