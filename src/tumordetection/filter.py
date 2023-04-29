import cv2
import numpy as np

'''
    This function is used to find the tumor in the image.
'''
def find_tumor(color_tumor,color_brain,brain,vetto,segm,mylist):
    my_interesed = []
    lista_riserva = []
    for value in mylist:
        mask = np.zeros(brain.shape[:2], np.uint8)
        mask[segm == value] = 255
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for el in contours:
            area = cv2.contourArea(el)
            circumference = cv2.arcLength(el, True)
            if circumference == 0:
                continue
            circularity = 4 * np.pi * (area / (circumference * circumference))
            if area > 300 and area < 20000 and circularity > 0.3:
                mask2 = np.zeros(brain.shape[:2], dtype="uint8")
                diz = {}
                cv2.drawContours(mask2, [el], -1, 255, -1)
                for i in range(0, brain.shape[0]):
                    for j in range(0, brain.shape[1]):
                        if mask2[i][j] == 255:
                            if brain[i][j] in diz:
                                diz[brain[i][j]] += 1
                            else:
                                diz[brain[i][j]] = 1
                somma = 0
                for k,v in diz.items():
                    somma+=k
                media = somma/len(diz)
                lista_riserva.append((el, media))
                if color_tumor > color_brain:
                    if media > color_brain:
                        my_interesed.append((el, media))
                else:
                    if media < color_brain:
                        my_interesed.append((el, media))
    my_contourn = 9999999
    my_cont = None
    enter = False
    for cc in my_interesed:
        cont = cc[0]
        perime  = cv2.arcLength(cont, True)
        circ = 4 * np.pi * (cv2.contourArea(cont) / (perime * perime))
        diff = abs(abs(color_tumor-cc[1]) - circ)
        if diff < my_contourn:
            my_contourn = diff
            my_cont = cont
            enter = True
    if enter == False:
        my_contourn = 9999999
        my_cont = None
        for cc in lista_riserva:
            cont = cc[0]
            perime  = cv2.arcLength(cont, True)
            circ = 4 * np.pi * (cv2.contourArea(cont) / (perime * perime))
            diff = abs(abs(color_tumor-cc[1]) - circ)
            if diff < my_contourn:
                my_contourn = diff
                my_cont = cont
    return my_cont