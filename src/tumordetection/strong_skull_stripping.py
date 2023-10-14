import cv2
import numpy as np
from sklearn.cluster import KMeans

def KMeansClustering(data, k,img):
    """This function is used to segment the image using K-Means Clustering."""
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(data)
    labels = kmeans.predict(data)
    segmented_data = np.uint8(kmeans.cluster_centers_[labels])
    segmented_img = segmented_data.reshape(img.shape)
    return segmented_img

def kmean(img):
    """Call the function KMeansClustering."""
    iterations = 20 
    data = np.float32(img.reshape((-1, 1)))
    segmented_img = KMeansClustering(data, 6, img)  
    return segmented_img,6

def strong_skull(foto):
    """Return the contour of the brain."""
    f = kmean(foto)
    imm  = f[0]
    massimo = -1
    my_brain = -1
    colore_cervello = -1
    hist = cv2.calcHist([imm], [0], None, [256], [0, 256])
    my_pixel = []
    for i in range(15, len(hist)):
        if hist[i] > 0:
            my_pixel.append(i)
    for intensità in my_pixel:
        mask = np.zeros(imm.shape[:2], dtype="uint8")
        mask[imm == intensità] = 255
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
                        if mask2[i][j] == 255:  
                            if foto[i][j] in diz:
                                diz[foto[i][j]] += 1
                            else:
                                diz[foto[i][j]] = 1
                somma = 0
                for k,v in diz.items():
                        somma+=k
                media = somma/len(diz)
                if circularity > massimo:
                    massimo = circularity
                    my_brain = el
                    colore_cervello = media
    try:   
        if massimo > 0.80:  
            mask2 = np.zeros(foto.shape[:2], dtype="uint8")
            cv2.drawContours(mask2, [my_brain], -1, 255, -1)
            mask3 = np.zeros(foto.shape[:2], dtype="uint8")
            for i in range(0, foto.shape[0]):
                for j in range(0, foto.shape[1]):
                    if mask2[i][j] == 255:
                        mask3[i][j] = foto[i][j]
            return 1,mask3,colore_cervello
        else:
            return -1,foto,0
    except:
            return -1,foto,0