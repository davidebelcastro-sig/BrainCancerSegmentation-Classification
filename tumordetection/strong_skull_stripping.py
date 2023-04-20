import cv2
import numpy as np
from sklearn.cluster import KMeans

def KMeansClustering(data, k,img):
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(data)
    # crea un'immagine segmentata
    labels = kmeans.predict(data)
    segmented_data = np.uint8(kmeans.cluster_centers_[labels])
    segmented_img = segmented_data.reshape(img.shape)
    return segmented_img


def kmean(img):
    iterations = 20  #numero di k da testare
    data = np.float32(img.reshape((-1, 1)))
    #k, inertias, ks = findK(data, iterations)
    segmented_img = KMeansClustering(data, 6, img)   #k = 6 perchè mi interessa trovare tanti contorni quanto più possibile
    #print("k trovato= "+str(k))
    #showImage(segmented_img)
    #showElbowMethod(ks, inertias)
    return segmented_img,6


def strong_skull(foto):
    f = kmean(foto)
    imm  = f[0]
    massimo = -1
    my_brain = -1
    colore_cervello = -1
    hist = cv2.calcHist([imm], [0], None, [256], [0, 256])
    #ciclo
    my_pixel = []
    for i in range(15, len(hist)):
        if hist[i] > 0:
            my_pixel.append(i)
    for intensità in my_pixel:
        #creo una maschera con solo i pixel di intensità intensità
        mask = np.zeros(imm.shape[:2], dtype="uint8")
        mask[imm == intensità] = 255
        #show
        #mi trovo i bordi
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for el in contours:
            el = cv2.convexHull(el)
            area = cv2.contourArea(el)
            circumference = cv2.arcLength(el, True)
            if circumference == 0:
                continue
            circularity = 4 * np.pi * (area / (circumference * circumference))
            if circularity > 0.60 and area >= imm.shape[0]*imm.shape[1]*0.10:
                mask2 = np.zeros(foto.shape[:2], dtype="uint8")
                diz = {}
                cv2.drawContours(mask2, [el], -1, 255, -1)
                for i in range(0, foto.shape[0]):
                    for j in range(0, foto.shape[1]):
                        if mask2[i][j] == 255:   #bordo in questione
                            if foto[i][j] in diz:
                                diz[foto[i][j]] += 1
                            else:
                                diz[foto[i][j]] = 1
                #diz contiene tutti i colori che ho trovato nel contorno
                #faccio la media
                somma = 0
                for k,v in diz.items():
                        somma+=k
                media = somma/len(diz)
                if circularity > massimo:
                    massimo = circularity
                    my_brain = el
                    colore_cervello = media

                       
                        
    try:   #se ho trovato un contorno 
        if massimo > 0.80:  #DA CAPIRE SE È UN BUON VALORE
            mask2 = np.zeros(foto.shape[:2], dtype="uint8")
            cv2.drawContours(mask2, [my_brain], -1, 255, -1)
            #prendo solo il mio brain 
            mask3 = np.zeros(foto.shape[:2], dtype="uint8")
            #dove mask2 è bianco, mask3 è foto
            for i in range(0, foto.shape[0]):
                for j in range(0, foto.shape[1]):
                    if mask2[i][j] == 255:
                        mask3[i][j] = foto[i][j]
            return 1,mask3,colore_cervello
        else:
            return -1,foto,0
    except:
            return -1,foto,0

       

