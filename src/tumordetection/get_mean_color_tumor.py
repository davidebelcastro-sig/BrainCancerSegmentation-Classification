import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans



'''
#convert the image in a numpy array
'''
def convertInNpArray(img):
    data = np.float32(img.reshape((-1, 1)))
    return data


'''
#find the best value of k using the elbow method
'''
def findK(data,num_range):
    point = {}
    inertias = []
    ks = range(2, num_range)
    for k in ks:
        model = KMeans(n_clusters=k, random_state=0)
        model.fit(data)
        inertias.append(model.inertia_)
        point[k] = model.inertia_
    difference = []
    for i in range(2, num_range-1): 
        diff = point[i] - point[i+1]
        difference.append(diff)
    media = np.average(difference)
    for el in difference:
        if el  < media: 
            k = difference.index(el) + 1 
            break
    return k, inertias, ks



'''
this function is used to segment the image using K-Means Clustering.
'''
def KMeansClustering(data, k,img):
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(data)
    labels = kmeans.predict(data)
    segmented_data = np.uint8(kmeans.cluster_centers_[labels])
    segmented_img = segmented_data.reshape(img.shape)
    return segmented_img


'''
show the image
'''
def showImage(img):
    cv2.imshow("Segmented Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


'''
show the elbow method
'''
def showElbowMethod(ks,inertias):
    plt.plot(ks, inertias, '-o')
    plt.xlabel('Numero di cluster, k')
    plt.ylabel('Somma dei quadrati delle distanze intra-cluster')
    plt.title('Metodo del gomito per la scelta di K')
    plt.xticks(ks)
    plt.axis('on')
    plt.show()


'''
call the function KMeansClustering
'''
def kmean(img):
    iterations = 20  
    data = convertInNpArray(img)
    segmented_img = KMeansClustering(data, 6, img)  
    return segmented_img,6


'''
return the value of the priority of the tumor
'''
def get_priority(tup,colore_cervello,area_contorno_esterno):
    colore_tumore = tup[0]
    circularity = tup[1]
    area = tup[2]
    if colore_tumore >= 120:
        prio1 = 6
    elif colore_tumore >= 110:
        prio1 = 5.5
    elif colore_tumore >= 100:
        prio1 = 5
    elif colore_tumore >= 90:
        prio1 = 4.5
    elif colore_tumore >= 85:
        prio1 = 4
    elif colore_tumore >= 80:
        prio1 = 3.5
    elif colore_tumore >= 75 and abs(colore_tumore-colore_cervello) >10:
        prio1 = 3
    elif colore_tumore >= 60 and abs(colore_tumore-colore_cervello) >10: 
        prio1 = 2.5
    elif colore_tumore >= 55 and abs(colore_tumore-colore_cervello) >10:
        prio1 = 2
    elif colore_tumore >= 50 and abs(colore_tumore-colore_cervello) >10:
        prio1 = 1.5
    else:
        prio1 = 1
    prio1 = prio1*10
    prio2 = circularity*70
    if area >= area_contorno_esterno*0.005 and area <= area_contorno_esterno*0.02:
        if circularity >= 0.65 and colore_tumore >= 80:  
            a = 1.3
        elif circularity >= 0.65 and colore_tumore >= 70:
            a = 0.7
        else:
            a = 0
    elif area > area_contorno_esterno*0.02 and area <= area_contorno_esterno*0.06:
        if circularity > 0.40:
            a = 1.7
        else:
            a = 0
    elif area > area_contorno_esterno*0.06 and area <= area_contorno_esterno*0.12:
        if circularity >= 0.40:
            a = 2
        elif circularity >= 0.45:
            a = 2.5
        else:
            a = 0
    elif area > area_contorno_esterno*0.12 and area <= area_contorno_esterno*0.15 and circularity >= 0.65:
        a=  1.9
    elif area > area_contorno_esterno*0.15 and area <= area_contorno_esterno*0.20 and circularity >= 0.70:
        a=  1.9
    else:
        a = 0
    prio3 = a*20
    diff = abs(colore_tumore-colore_cervello)
    if diff > 15:
        prio4 = 1
    else:
        prio4 = 0
    prio4 = prio4*20
    media_prio = (prio1+prio2+prio3+prio4)/120
    return media_prio

'''
return the mean color of the tumor
'''
def get_color(img,colore_cervello,area_contorno_esterno):
        img = cv2.GaussianBlur(img, (5, 5), 0)
        img = cv2.medianBlur(img, 5)
        my_possibili_tumori = []
        tup = kmean(img)
        segm = tup[0]
        k = tup[1]
        hist = cv2.calcHist([segm], [0], None, [256], [0, 256])
        my_pixel = []
        for i in range(15, len(hist)):
            if hist[i] > 0:
                 my_pixel.append(i)
        for intensità in my_pixel:
            mask = np.zeros(segm.shape[:2], dtype="uint8")
            mask[segm == intensità] = 255
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for el in contours:
                el = cv2.convexHull(el)
                area = cv2.contourArea(el)
                circumference = cv2.arcLength(el, True)
                if circumference == 0:
                    continue
                circularity = 4 * np.pi * (area / (circumference * circumference))
                if (circularity >= 0.3 and area >= 0.005*area_contorno_esterno and area <= 0.15*area_contorno_esterno) or(circularity >= 0.45 and area > 0.15 * area_contorno_esterno and area <= 0.20 * area_contorno_esterno) or (circularity >= 0.55 and area > 0.20 * area_contorno_esterno and area <= 0.22 * area_contorno_esterno) :
                    mask2 = np.zeros(img.shape[:2], dtype="uint8")
                    diz = {}
                    cv2.drawContours(mask2, [el], -1, 255, -1)
                    for i in range(0, img.shape[0]):
                        for j in range(0, img.shape[1]):
                            if mask2[i][j] == 255:   
                                if img[i][j] in diz:
                                    diz[img[i][j]] += 1
                                else:
                                    diz[img[i][j]] = 1
                    somma = 0
                    for k,v in diz.items():
                        somma+=k
                    media = somma/len(diz)
                    my_possibili_tumori.append((media,circularity,area))
        if len(my_possibili_tumori) == 0:
            return 0,segm,my_pixel,area_contorno_esterno,colore_cervello
        lista_priorita = []
        for el in my_possibili_tumori:
            priority = get_priority(el,colore_cervello,area_contorno_esterno)
            lista_priorita.append((priority,el[0]))
        lista_priorita.sort(key=lambda tup: tup[0], reverse=True)
        colore = lista_priorita[0][1]
        return colore,segm,my_pixel,area_contorno_esterno,colore_cervello