import cv2
import numpy as np



# Caricare l'immagine di input
img = cv2.imread("Y15.jpg")

# converte l'immagine in scala di grigi
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# applica un filtro di Canny per rilevare i bordi
edges = cv2.Canny(gray, 100, 200)

# trova i contorni nell'immagine
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#sorted
contours = sorted(contours, key=cv2.contourArea, reverse=True)

#brain contorn
brain = contours[0]
#come prendo tutto quello che è dentro il contorno?

# Ridurre il numero di colori nell'immagine
Z = img.reshape((-1,3))
Z = np.float32(Z)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 8
ret,label,center=cv2.kmeans(Z,K,None,criteria,200,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))



# Convertire l'immagine in scala di grigi
gray = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)

# Applicare il CLAHE all'immagine in scala di grigi
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl_img = clahe.apply(gray)


# applica una chiusura per unire regioni vicine
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
closed = cv2.morphologyEx(cl_img, cv2.MORPH_CLOSE, kernel)

# applica una apertura per eliminare le piccole regioni
#opening = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)

window_size = 60  # dimensione della finestra intorno al pixel di interesse
sigma_color = 90  # deviazione standard di intensità
sigma_space = 90  # deviazione standard spaziale
filtered = cv2.bilateralFilter(closed, window_size, sigma_color, sigma_space)


# Applica la soglia per binarizzare l'immagine
ret, thresh = cv2.threshold(filtered, 150, 255, cv2.THRESH_BINARY)

# Trova i contorni nell'immagine binarizzata
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# disegna solo i contorni con un'area maggiore di 100
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 500 and area < 10000: #se è abbasstante grande
        cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)




# Visualizzare l'immagine di output
cv2.imshow('Input', img)
cv2.imshow('Output', filtered)
cv2.waitKey(0)
cv2.destroyAllWindows()