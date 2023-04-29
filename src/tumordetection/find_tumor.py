import cv2
import numpy as np

'''
return the probability that an area is a tumor
'''
def get_probability_of_tumor(area,circularity,colore_tumore,colore_cervello,area_esterna):
    if circularity >= 0.90 and area <= area_esterna*0.20  and abs(colore_tumore-colore_cervello) >= 10:
        return 0.90
    elif circularity >= 0.90 and area <= area_esterna*0.20  and abs(colore_tumore-colore_cervello) < 10:
        return 0.70
    elif circularity >= 0.80 and area <= area_esterna*0.20  and abs(colore_tumore-colore_cervello) >= 10:
        return 0.75
    elif circularity >= 0.80 and area <= area_esterna*0.20  and abs(colore_tumore-colore_cervello) < 10:
        return 0.65
    elif circularity >= 0.75 and area <= area_esterna*0.20  and colore_tumore >= 80 and abs(colore_tumore-colore_cervello) >= 10:
        return 0.70
    elif circularity >= 0.75 and area <= area_esterna*0.20 and colore_tumore >= 80 and abs(colore_tumore-colore_cervello) < 10:
        return 0.50
    else:
        return 0.30
    

'''
return an value that represent the priority of a tumor
'''
def get_media_pesata(tup,color_tumor,area_contorno_esterno,colore_cervello):
    media = tup[1]  
    area = tup[2]  
    circularity = tup[3] 
    if media >= 120:
        prio1 = 6
    elif media >= 110:
        prio1 = 5.5
    elif media >= 100:
        prio1 = 5
    elif media >= 90:
        prio1 = 4.5
    elif media >= 85:
        prio1 = 4
    elif media >= 80:
        prio1 = 3.5
    elif media >= 75 and abs(media-colore_cervello) >10:
        prio1 = 3
    elif media >= 60 and abs(media-colore_cervello) >10: 
        prio1 = 2.5
    elif media >= 55 and abs(media-colore_cervello) >10:
        prio1 = 2
    elif media >= 50 and abs(media-colore_cervello) >10:
        prio1 = 1.5
    else:
        prio1 = 1
    prio1 = prio1*10
    prio2 = circularity*70
    if area >= area_contorno_esterno*0.005 and area <= area_contorno_esterno*0.02:
        if circularity >= 0.65 and media >= 80:  
            a = 1.3
        elif circularity >= 0.65 and media >= 70:
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
    diff = abs(media-color_tumor)
    if diff <= 15:
        prio4 = 1.4
    elif diff > 15 and diff <= 25:
        prio4 = 1
    else:
        prio4 = 0
    prio4 = prio4*20
    media_prio = (prio1+prio2+prio3+prio4)/120
    return media_prio



'''
return the tumor with your priority
'''
def get_tumor(color_tumor,brain,segm,mylist,area_contorno_esterno,colore_cervello):
    lista_contorni = []
    for value in mylist:
        mask = np.zeros(brain.shape[:2], np.uint8)
        mask[segm == value] = 255
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for el in contours:
            el = cv2.convexHull(el)
            area = cv2.contourArea(el)
            circumference = cv2.arcLength(el, True)
            if circumference == 0:
                continue
            circularity = 4 * np.pi * (area / (circumference * circumference))
            if (circularity >= 0.3 and area >= 0.005*area_contorno_esterno and area <= 0.15*area_contorno_esterno) or(circularity >= 0.45 and area > 0.15 * area_contorno_esterno and area <= 0.20 * area_contorno_esterno) or (circularity >= 0.55 and area > 0.20 * area_contorno_esterno and area <= 0.22 * area_contorno_esterno) :
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
                lista_contorni.append((el, media,area,circularity))
    diz_contorni = []
    for tup in lista_contorni:
        media_pesata = get_media_pesata(tup,color_tumor,area_contorno_esterno,colore_cervello)
        diz_contorni.append(media_pesata)
    brain = cv2.cvtColor(brain, cv2.COLOR_GRAY2BGR)
    index = 0
    diz_appoggio = {}
    for el in lista_contorni:
        r_random = np.random.randint(0, 255)
        g_random = np.random.randint(0, 255)
        b_random = np.random.randint(0, 255)
        cl = (r_random, g_random, b_random)
        diz_appoggio[(diz_contorni[index],cl)] = (el[0],el[1])
        cv2.drawContours(brain, [el[0]], -1, cl, 2)
        index+=1
    dizionario_2 = {}
    for k,v in diz_appoggio.items():
        if k[0] >= 1.15:
            dizionario_2[k] = v
    diz_appoggio = dizionario_2
    diz_appoggio = dict(sorted(diz_appoggio.items(), key=lambda item: item[0][0]))
    diz_appoggio = dict(reversed(list(diz_appoggio.items())))
    if len(diz_appoggio) == 0:
        return "no tumor",0
    my_tumor = diz_appoggio[list(diz_appoggio.keys())[0]][0]
    color = diz_appoggio[list(diz_appoggio.keys())[0]][1]
    area = cv2.contourArea(my_tumor)
    circumference = cv2.arcLength(my_tumor, True)
    if circumference == 0:
        return "no tumor",0
    circularity = 4 * np.pi * (area / (circumference * circumference))
    percentuale_area_tumore = (area / area_contorno_esterno) * 100
    if circularity >=0.75: 
        probability = get_probability_of_tumor(area,circularity,color,colore_cervello,area_contorno_esterno)
        return my_tumor,probability
    else:
        return "no tumor",0