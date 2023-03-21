







import cv2
import numpy as np



def findContour(img):
    #¢rea una copia dell'immagine di input
    img2 = img.copy()

    # Convertire l'immagine in scala di grigi
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        # Applica un filtro di smoothing all'immagine RM per ridurre il rumore
    img2 = cv2.GaussianBlur(img2, (5, 5), 0)

    # Applica una soglia binaria all'immagine per separare i pixel del cervello dallo sfondo
    _, img_bin = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Utilizza la funzione cv2.findContours() di OpenCV per trovare i contorni degli oggetti bianchi nell'immagine binarizzata
    contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours








# Caricare l'immagine di input
img = cv2.imread("Y13.jpg") #copia su sui disegno il tumore

copia = img.copy()   #copia da lavoro
copia2 = img.copy() #copia che non toco



c = findContour(img)

contours_sorted = sorted(c, key=lambda c: cv2.contourArea(c), reverse=True)

brain = contours_sorted[0]



cv2.drawContours(copia, [brain], 0, (0, 0, 0), 25)  #mi levo il contorno del cervello


#step1:
# Ridurre il numero di colori nell'immagine:rendo tutti i colori o grigi o bianchi o neri
Z = copia.reshape((-1,3))
Z = np.float32(Z)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 8
ret,label,center=cv2.kmeans(Z,K,None,criteria,200,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((copia.shape))


#step2:
# Convertire l'immagine in scala di grigi
gray = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
# Definisci la dimensione del kernel
kernel_size = 3
# Crea un kernel quadrato di dimensione 3x3
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
dilated_img = cv2.dilate(gray, kernel, iterations=2)   #aumenta il numero di pixel bianchi facendo un espansione ripetuta iterations volte

#step3:
# Applica l'equalizzazione dell'istogramma
eq_img = cv2.equalizeHist(dilated_img)   #aumenta il contrasto dell'immagine

#step4:
# applica una chiusura per unire regioni vicine
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
closed = cv2.morphologyEx(eq_img, cv2.MORPH_CLOSE, kernel)

#step5:
# applica una apertura per eliminare le piccole regioni
opening = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)

#step6:
# Applicare il CLAHE all'immagine in scala di grigi
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl_img = clahe.apply(opening)

#step7:
window_size = 10  # dimensione della finestra intorno al pixel di interesse
sigma_color = 20  # deviazione standard di intensità
sigma_space = 20  # deviazione standard spaziale
filtered = cv2.bilateralFilter(cl_img, window_size, sigma_color, sigma_space)


#step8:
# Applica la soglia per binarizzare l'immagine,tutti i pixel maggiori di 180 diventano bianchi
ret, thresh = cv2.threshold(filtered, 220, 255, cv2.THRESH_BINARY)

# Trova i contorni nell'immagine binarizzata
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#fine
# disegna solo i contorni con un'area maggiore di 100
for cnt in contours:
    area = cv2.contourArea(cnt)
    is_inner_contour = False
    a = tuple(brain[0][0])
    #dist = cv2.pointPolygonTest(cnt, (int(a[0]),int(a[1])), False)
    #if dist < 0:
        # Se il contorno corrente è interno ad un altro contorno, esegui l'analisi appropriata
    if area > 900 and area < 22000: #se è abbasstante grande ma non quanto il cervello
        print("Area: ", area)
        cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
       
cv2.imshow('inizio', copia2)
cv2.imshow('step1', res2)
cv2.imshow('step2', dilated_img)
cv2.imshow('step3', eq_img)
cv2.imshow('step4', closed)
cv2.imshow('step5', opening)
cv2.imshow('step6', cl_img)
cv2.imshow('step7', filtered)
cv2.imshow('step8', thresh)
cv2.imshow('out', img)
cv2.waitKey(0)
cv2.destroyAllWindows()




















