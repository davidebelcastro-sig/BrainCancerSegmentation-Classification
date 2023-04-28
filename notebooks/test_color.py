import os
import matplotlib.pyplot as plt
import h5py
from src.skull_stripping import get_brain
from strong_skull_stripping import strong_skull
import csv
import get_mean_color_tumor
import cv2



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


def test_nii(path):
    cont = 0
    totale = 0
    corretti = 0
    errate_dame = 0
    corrette2 = 0
    errate2 = 0
    dataset = os.listdir(path)
    for file in dataset:
        cont += 1
        if cont == 200:
            break
        f = h5py.File(path + "/" + file, 'r')
        for el in f['cjdata']:
            if el == 'image':
                image = f['cjdata'][el]
            elif el == 'tumorMask':
                mask = f['cjdata'][el]
        plt.imshow(image,cmap='gray')
        plt.axis('off')
        plt.savefig('brain.png')

        plt.imshow(mask,cmap='gray')
        plt.axis('off')
        plt.savefig('brain_mask.png')
        mask = cv2.imread('brain_mask.png')
        img = cv2.imread('brain.png')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        diz_medi = {}
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if mask[i][j] == 255:
                    if img[i][j] in diz_medi:
                        diz_medi[img[i][j]] += 1
                    else:
                        diz_medi[img[i][j]] = 1
        #media 
        lunghezza = len(diz_medi)
        media = 0
        for k,v in diz_medi.items():
            media += k
        media = media/lunghezza
        tupla = get_brain('brain.png')
        mask = tupla[0]
        foto = tupla[1]
        area_contorno_esterno = get_contourn_external(foto)
        cervello_color = tupla[2]
        if mask == 1 or mask == 2:
            color = get_mean_color_tumor.get_color(foto, cervello_color, area_contorno_esterno)[0]
            totale += 1
            diff = abs(color - media)
            if diff <= 25:
                with open('./test_color_diff.csv', 'a') as csvfile2:
                    writer = csv.writer(csvfile2)
                    writer.writerow([str(media),str(color),str(diff),1])
                    corretti += 1
            else:
                with open('./test_color_diff.csv', 'a') as csvfile2:
                    writer = csv.writer(csvfile2)
                    writer.writerow([str(media),str(color),str(diff),0])
                    errate_dame += 1
            if color >= cervello_color:
                if media >= cervello_color:
                    corrette2 += 1
                    with open('./test_color_magg.csv', 'a') as csvfile2:
                        writer = csv.writer(csvfile2)
                        writer.writerow([str(cervello_color),str(color),str(media),1])
                else:
                    errate2 += 1
                    with open('./test_color_magg.csv', 'a') as csvfile2:
                        writer = csv.writer(csvfile2)
                        writer.writerow([str(cervello_color),str(color),str(media),0])
            else:
                if media < cervello_color:
                    corrette2 += 1
                    with open('./test_color_magg.csv', 'a') as csvfile2:
                        writer = csv.writer(csvfile2)
                        writer.writerow([str(cervello_color),str(color),str(media),1])
                else:
                    errate2 += 1
                    with open('./test_color_magg.csv', 'a') as csvfile2:
                        writer = csv.writer(csvfile2)
                        writer.writerow([str(cervello_color),str(color),str(media),0])
        else:
            tupla = strong_skull(foto)
            mask = tupla[0]
            foto = tupla[1]
            area_contorno_esterno = get_contourn_external(foto)
            cervello_color = tupla[2]
            if mask == 1:
                color = get_mean_color_tumor.get_color(foto, cervello_color, area_contorno_esterno)[0]
                totale += 1
                diff = abs(color - media)
                if diff <= 25:
                    with open('./test_color_diff.csv', 'a') as csvfile2:
                        writer = csv.writer(csvfile2)
                        writer.writerow([str(media),str(color),str(diff),1])
                        corretti += 1
                else:
                    with open('./test_color_diff.csv', 'a') as csvfile2:
                        writer = csv.writer(csvfile2)
                        writer.writerow([str(media),str(color),str(diff),0])
                        errate_dame += 1
                if color >= cervello_color:
                    if media >= cervello_color:
                        corrette2 += 1
                        with open('./test_color_magg.csv', 'a') as csvfile2:
                            writer = csv.writer(csvfile2)
                            writer.writerow([str(cervello_color),str(color),str(media),1])
                    else:
                        errate2 += 1
                        with open('./test_color_magg.csv', 'a') as csvfile2:
                            writer = csv.writer(csvfile2)
                            writer.writerow([str(cervello_color),str(color),str(media),0])
                else:
                    if media < cervello_color:
                        corrette2 += 1
                        with open('./test_color_magg.csv', 'a') as csvfile2:
                            writer = csv.writer(csvfile2)
                            writer.writerow([str(cervello_color),str(color),str(media),1])
                    else:
                        errate2 += 1
                        with open('./test_color_magg.csv', 'a') as csvfile2:
                            writer = csv.writer(csvfile2)
                            writer.writerow([str(cervello_color),str(color),str(media),0])
        if cont % 10 == 0:
            print("Analizzati " + str(cont) + " file")
        # Dico che è giusto quando sia colore mio che colore media sono maggiori o minimi del colore del cervello



    print("Analisi completata")
    perc_ok =       (corretti / totale) * 100
    perc_errata =   (errate_dame/ totale) * 100
    perc_ok2 =      (corrette2 / totale) * 100
    perc_errata2 =  (errate2 / totale) * 100
    #scrivo su file i valori trovati
    with open('./attendibilità_tumor_color.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([path, str(corretti), str(errate_dame), str(perc_ok) + "%", str(perc_errata) + "%", str(totale)])
    with open('./attendibilità_tumor_color_brain_magg.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([path, str(corrette2), str(errate2), str(perc_ok2) + "%", str(perc_errata2) + "%", str(totale)])






if __name__ == '__main__':
    test_nii('../dataset_nii/dataset/brainTumorDataPublic_1-766')