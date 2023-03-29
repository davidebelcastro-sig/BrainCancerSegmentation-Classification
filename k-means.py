import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import cv2




def loadImage(path):
    img = cv2.imread(path)
    return img


def filter(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #applica piu filtri possibili
    return img


def convertInNpArray(img):
    data = np.float32(img.reshape((-1, 1)))
    return data


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
        if el  < media: #se la differenza è minore della media allora prendo il k precedente
            k = difference.index(el) + 1 #prendo il k prima
            break
    return k, inertias, ks


def KMeansClustering(data, k,img):
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(data)
    # crea un'immagine segmentata
    labels = kmeans.predict(data)
    segmented_data = np.uint8(kmeans.cluster_centers_[labels])
    segmented_img = segmented_data.reshape(img.shape)
    return segmented_img

def showImage(img):
        # visualizza l'immagine segmentata
    cv2.imshow("Segmented Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def showElbowMethod(ks,inertias):
    # plotta il grafico del gomito
    plt.plot(ks, inertias, '-o')
    plt.xlabel('Numero di cluster, k')
    plt.ylabel('Somma dei quadrati delle distanze intra-cluster')
    plt.title('Metodo del gomito per la scelta di K')
    plt.xticks(ks)
    plt.show()


#trovare se c'è il tumore
#0 se non c'è, 1 se c'è
def findTumor(img):
    pass
    return -1


def studyContour(img, segmented_img):
    pass


def main():
    path = ".image.jpg"
    iterations = 15  #numero di k da testare
    img = loadImage(path)
    img_copia = img.copy()
    img = filter(img)
    data = convertInNpArray(img)
    k, inertias, ks = findK(data, iterations)
    segmented_img = KMeansClustering(data, k, img)
    showImage(segmented_img)
    showElbowMethod(ks, inertias)
    #vedere se l'immagine segmentata ha un tumore o no
    #se ce l'ha allora studiare il contorno
    #generare file output con tutte le caratteristiche del tumore
    tumor = findTumor(segmented_img)
    if tumor == 1:
        studyContour(img_copia, segmented_img)
    else:
        print("Non ci sono tumori")



if __name__ == "__main__":
    main()


