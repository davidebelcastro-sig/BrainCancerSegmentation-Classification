import cv2
import math
import numpy as np
import os


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
    circunference = cv2.arcLength(countour,True)
    if circunference == 0:
        circ = 0
    else:
        circ = 4*np.pi*(area_contorno_esterno/(circunference**2))

    return area_contorno_esterno,circ

def get_brain(path):
    tupla = analize(path)
    mask = tupla[0]
    foto = tupla[1]
    if mask == 1 or mask == 2:
        res = get_contourn_external(foto)
        if res[1] < 0.7 or res[0] < foto.shape[0]*foto.shape[1]*0.10:
            mask = -1
            foto  = cv2.imread(path)
            foto = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY)
    return mask,foto,tupla[2]



def analize(path):

    img = cv2.imread(path)
    #resize
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    start = img.copy()
    #histogram
    img[img <= 15] = 255
    #mi prendo il contorno esteno
    thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #find contours
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #draw contours
    #ordino
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    #prendo il contorno più grande
    external = contours[0]
    
    hist = cv2.calcHist([img],[0],None,[256],[0,256])
    massimo = -1
    for i in range(20,190): #levo i primi 20 valori(0,19) e mi fermo a 189(gli altri troppo chiari)
        if hist[i] > massimo:
            massimo = hist[i]
            indice = i
    #print(indice) #è il valore del pixel che più si ripete
    #faccio un range di 20 pixel(+10 e -10) attorno a quello che più si ripete
    #e gli assegno il valore 0 a tutti gli altri pixel
    #canny
    edges = cv2.Canny(img,indice-10,indice+10)
    edges = cv2.dilate(edges, None, iterations=1)
    edges = cv2.erode(edges, None, iterations=1)
    #find contours
    c = 0
    contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros((img.shape[0],img.shape[1]), np.uint8)
    #draw
    for el in contours:
        cv2.drawContours(mask, [el], -1, 255, 2)
    #show
    for el in contours:
        #if cv2.contourArea(el) < 500:  #elimino i contorni troppo piccoli
        x = (500*img.shape[0]*img.shape[1]) / (480*640)
        #come posso calcolare 500 in base alla dimensione dell'immagine?
        if cv2.contourArea(el) < x:
            cv2.drawContours(edges, [el], -1, 255, -1)       
    #inverto
    edges = cv2.bitwise_not(edges)
    #find contours
    contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #draw contours
    for el in contours:
        x = (500*img.shape[0]*img.shape[1]) / (480*640)
        if cv2.contourArea(el) < x:
        #if cv2.contourArea(el) < 500:  #elimino i contorni troppo piccoli
            cv2.drawContours(edges, [el], -1, 255, -1)
    #inverto
    edges = cv2.bitwise_not(edges)
    #convex hull
    #tutti i pixel non dentro external li metto a 255
    #creo immagine tutta nera
    black = np.zeros((img.shape[0],img.shape[1]), np.uint8)
    cv2.drawContours(black, [external], -1, 255, -1)
    #inverto black
    black = cv2.bitwise_not(black)
    #tutti i pixel bianchi dentro black vadano bianchi dentro edges
    for i in range(0,edges.shape[0]):
        for j in range(0,edges.shape[1]):
            if black[i][j] == 255:
                edges[i][j] = 255
    contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #ordino i contorni in base alla loro area
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    #prendo il contorno più grande
    c = contours[0] #devo vedere se è troppo grande allora prendo il secondo
    external = cv2.convexHull(external)
    #print("Dimensioni cervello esterno: " + str(cv2.contourArea(external)))
    if cv2.contourArea(c) > cv2.contourArea(external):
        c = contours[1]
        #print("Contorno 1:" + str(cv2.contourArea(c)))
    else:
        #vedere se è comunque troppo grande
        value = cv2.contourArea(external) - 10000
        x = (value*img.shape[0]*img.shape[1]) / (480*640)
        if cv2.contourArea(c) > x:
        #if cv2.contourArea(c) > value:
            c = contours[1]
            #print("Contorno 1:" + str(cv2.contourArea(c)))
        else:
            c = contours[0]

    value = 5000
    x = (value*img.shape[0]*img.shape[1]) / (480*640)
    if cv2.contourArea(c) < x: # prima era 5000
    #if cv2.contourArea(c) < img.shape[0] * img.shape[1]*0.016:
        if cv2.contourArea(contours[0]) > cv2.contourArea(external):
            #print("Probabilmente c'è un errore")
            return -1,start,indice  #ho un errore e quindi prendo la foto iniziale
        else:
            c = contours[0]
            #print("Contorno 0:" + str(cv2.contourArea(c)))

    #disegno
    #RIPETO I PASSI DUE VOLTE PERÒ CON IL CONTORNO CONVEX E NON..QUELLO 'NON' ,LO SALVO PER RITORNARLO QUANDO TROVO UN CONTORNO TROPPO GRANDE
    contorno_appoggio = c
    hull = cv2.convexHull(c)
    start2 = start.copy()
    start22 = start.copy()
    edges2 = edges.copy()
    cv2.drawContours(edges, [hull], -1, 127, -1)
    cv2.drawContours(edges2, [contorno_appoggio], -1, 127, -1)
    edges[edges == 255] = 0
    edges[edges == 127] = 255
    edges2[edges2 == 255] = 0
    edges2[edges2 == 127] = 255
    for i in range(0,edges.shape[0]):
        for j in range(0,edges.shape[1]):
            if edges[i][j]!= 255:
                start[i][j] = 0
    for i in range(0,edges2.shape[0]):
        for j in range(0,edges2.shape[1]):
            if edges2[i][j]!= 255:
                start22[i][j] = 0
    #tutti quelli vicino al bianoc li porto a nero
    start[start >= indice+15] = 0
    start[start <= indice-15] = 0
    start22[start22 >= indice+15] = 0
    start22[start22 <= indice-15] = 0
    #find contours
    contours, hierarchy = cv2.findContours(start,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #order
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    #prendo il contorno più grande
    if len(contours) == 0:
        return -1,start2,indice
    c = contours[0]
    #disegno
    hull = cv2.convexHull(c)
    cv2.drawContours(start, [hull], -1, 127, -1)
    start3 = start2.copy()
    for i in range(0,start.shape[0]):
        for j in range(0,start.shape[1]):
            if start[i][j] != 127:
                start3[i][j] = 0


      #find contours
    contours22, hierarchy2 = cv2.findContours(start22,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #order
    contours22 = sorted(contours22, key=cv2.contourArea, reverse=True)
    #prendo il contorno più grande
    if len(contours22) == 0:
        return -1,start2,indice
    c22 = contours22[0]
    #disegno
    hull22 = cv2.convexHull(c22)
    cv2.drawContours(start22, [hull22], -1, 127, -1)
    start33 = start2.copy()
    for i in range(0,start.shape[0]):
        for j in range(0,start.shape[1]):
            if start22[i][j] != 127:
                start33[i][j] = 0
    #cv2.imshow("start",start2)
    #cv2.imshow("final",start3)
    #colore medio=indice
    #se trovo tanti pixel maggiori del colore medio +15 allora ho trovat piu del previsgto
    trovato = 0

    for i  in range(0,start.shape[0]):
        for j in range(0,start.shape[1]):
            if start3[i][j] > indice+15:
                trovato +=1
    vl = 4500
    x = (vl*img.shape[0]*img.shape[1]) / (480*640)

    if trovato > x:  #prima vl = 4500
        #print("Maggiore")
        #posso rprendere il contorno non convex hull-> c
        trovato = 0
        for i  in range(0,start22.shape[0]):
            for j in range(0,start22.shape[1]):
                if start33[i][j] > indice+20:
                    trovato +=1
        #if trovato > img.shape[1] * img.shape[0] *0.01:
        vl = 3000
        x = (vl*img.shape[0]*img.shape[1]) / (480*640)
        if trovato > x:
            return 2,start33,indice #ho maggiore(forse)
        else:
            #draw contour
            area = cv2.contourArea(hull22)
            arcLength = cv2.arcLength(hull22,True)
            circularity = 4*math.pi*area/(arcLength*arcLength)
            if circularity >= 0.88:
                return 1,start33,indice  #foto finale
            else:
                return 2,start3,indice #ritorno quella che dovevo tornare inizialmente maggiore
    else:
        #come posso vedere se un segmento è circolare?
        #se è circolare allora ha un raggio medio
        #raggio medio = area/pi greco
        area = cv2.contourArea(hull)
        arcLength = cv2.arcLength(hull,True)
        circularity = 4*math.pi*area/(arcLength*arcLength)
        if circularity >= 0.90:
            return 1,start3,indice  #foto finale
        else:
            return -1,start2,indice #non prendo il bordo perche ho un errore

    


