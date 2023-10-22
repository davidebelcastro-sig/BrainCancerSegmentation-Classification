import cv2
import math
import numpy as np

def get_contourn_external(brain):
    """Return the contour of the brain."""
    j = brain.copy()
    for i in range(0,brain.shape[0]):
        for y in range(0,brain.shape[1]):
            if j[i][y] != 0:
                j[i][y] = 255
    contours, hierarchy = cv2.findContours(j,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    countour = max(contours, key=cv2.contourArea)
    area_contorno_esterno = cv2.contourArea(countour)
    circunference = cv2.arcLength(countour,True)
    if circunference == 0:
        circ = 0
    else:
        circ = 4*np.pi*(area_contorno_esterno/(circunference**2))
    return area_contorno_esterno,circ

def get_brain(path):
    """Return the mask of the brain and the mean color of the brain."""
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
    """This function is used to find the brain in the image and the mean color of the brain."""
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    start = img.copy()
    img[img <= 15] = 255
    thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    external = contours[0]
    hist = cv2.calcHist([img],[0],None,[256],[0,256])
    massimo = -1
    for i in range(20,190): 
        if hist[i] > massimo:
            massimo = hist[i]
            indice = i
    edges = cv2.Canny(img,indice-10,indice+10)
    edges = cv2.dilate(edges, None, iterations=1)
    edges = cv2.erode(edges, None, iterations=1)
    c = 0
    contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros((img.shape[0],img.shape[1]), np.uint8)
    for el in contours:
        cv2.drawContours(mask, [el], -1, 255, 2)
    for el in contours:
        x = (500*img.shape[0]*img.shape[1]) / (480*640)
        if cv2.contourArea(el) < x:
            cv2.drawContours(edges, [el], -1, 255, -1)       
    edges = cv2.bitwise_not(edges)
    contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for el in contours:
        x = (500*img.shape[0]*img.shape[1]) / (480*640)
        if cv2.contourArea(el) < x:
            cv2.drawContours(edges, [el], -1, 255, -1)
    edges = cv2.bitwise_not(edges)
    black = np.zeros((img.shape[0],img.shape[1]), np.uint8)
    cv2.drawContours(black, [external], -1, 255, -1)
    black = cv2.bitwise_not(black)
    for i in range(0,edges.shape[0]):
        for j in range(0,edges.shape[1]):
            if black[i][j] == 255:
                edges[i][j] = 255
    contours, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    c = contours[0] 
    external = cv2.convexHull(external)
    if cv2.contourArea(c) > cv2.contourArea(external):
        c = contours[1]
    else:
        value = cv2.contourArea(external) - 10000
        x = (value*img.shape[0]*img.shape[1]) / (480*640)
        if cv2.contourArea(c) > x:
            c = contours[1]
        else:
            c = contours[0]
    value = 5000
    x = (value*img.shape[0]*img.shape[1]) / (480*640)
    if cv2.contourArea(c) < x: 
        if cv2.contourArea(contours[0]) > cv2.contourArea(external):
            return -1,start,indice 
        else:
            c = contours[0]
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
    start[start >= indice+15] = 0
    start[start <= indice-15] = 0
    start22[start22 >= indice+15] = 0
    start22[start22 <= indice-15] = 0
    contours, hierarchy = cv2.findContours(start,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    if len(contours) == 0:
        return -1,start2,indice
    c = contours[0]
    hull = cv2.convexHull(c)
    cv2.drawContours(start, [hull], -1, 127, -1)
    start3 = start2.copy()
    for i in range(0,start.shape[0]):
        for j in range(0,start.shape[1]):
            if start[i][j] != 127:
                start3[i][j] = 0
    contours22, hierarchy2 = cv2.findContours(start22,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours22 = sorted(contours22, key=cv2.contourArea, reverse=True)
    if len(contours22) == 0:
        return -1,start2,indice
    c22 = contours22[0]
    hull22 = cv2.convexHull(c22)
    cv2.drawContours(start22, [hull22], -1, 127, -1)
    start33 = start2.copy()
    for i in range(0,start.shape[0]):
        for j in range(0,start.shape[1]):
            if start22[i][j] != 127:
                start33[i][j] = 0
    trovato = 0
    for i  in range(0,start.shape[0]):
        for j in range(0,start.shape[1]):
            if start3[i][j] > indice+15:
                trovato +=1
    vl = 4500
    x = (vl*img.shape[0]*img.shape[1]) / (480*640)
    if trovato > x:  
        trovato = 0
        for i  in range(0,start22.shape[0]):
            for j in range(0,start22.shape[1]):
                if start33[i][j] > indice+20:
                    trovato +=1
        vl = 3000
        x = (vl*img.shape[0]*img.shape[1]) / (480*640)
        if trovato > x:
            return 2,start33,indice 
        else:
            area = cv2.contourArea(hull22)
            arcLength = cv2.arcLength(hull22,True)
            circularity = 4*math.pi*area/(arcLength*arcLength)
            if circularity >= 0.88:
                return 1,start33,indice  
            else:
                return 2,start3,indice 
    else:
        area = cv2.contourArea(hull)
        arcLength = cv2.arcLength(hull,True)
        circularity = 4*math.pi*area/(arcLength*arcLength)
        if circularity >= 0.90:
            return 1,start3,indice  
        else:
            return -1,start2,indice 