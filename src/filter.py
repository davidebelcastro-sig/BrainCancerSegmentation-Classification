import cv2
import random
import numpy as np




def get_contourn(immagine_segmentata):

    for x in range(len(immagine_segmentata)):
        for y in range(len(immagine_segmentata)):
            try:
                if immagine_segmentata[x][y][0] == 0 and  immagine_segmentata[x][y][1] == 255  and  immagine_segmentata[x][y][2] == 0:
                    immagine_segmentata[x][y][0] = 255
                    immagine_segmentata[x][y][1] = 255
                    immagine_segmentata[x][y][2] = 255
                else:
                    immagine_segmentata[x][y][0] = 0
                    immagine_segmentata[x][y][1] = 0
                    immagine_segmentata[x][y][2] = 0
            except:
                pass

    immagine_segmentata =  cv2.cvtColor(immagine_segmentata, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(immagine_segmentata,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours[0]



#elimina bordo:ritorno l'immagine iniziale
def remove_border(immagine_iniziale):
    return immagine_iniziale


#modificare luce del contorno
def modify_light_contorno(immagine_iniziale,contorno,percentuale,segno):
    immagine_iniziale = cv2.cvtColor(immagine_iniziale, cv2.COLOR_BGR2GRAY)
    cv2.imshow('immagine_iniziale',immagine_iniziale)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    copia = immagine_iniziale.copy()
    lista_pixel = []
    cv2.drawContours(copia, [contorno], -1, 255, -1)
    for i in range(0,immagine_iniziale.shape[0]):
        for y in range(0,immagine_iniziale.shape[1]):
            try:
                if copia[i][y] == 255:
                    lista_pixel.append((i,y))
            except:
                pass
    #tutto quello dentro il contorno lo auemtno/abbassiamo di percentuale
    if segno == 1:
        for pixel in lista_pixel:
            immagine_iniziale[pixel[0]][pixel[1]]=min(immagine_iniziale[pixel[0]][pixel[1]] + (immagine_iniziale[pixel[0]][pixel[1]]*percentuale)/100,255)
        cv2.imshow('moidificata',immagine_iniziale)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        for pixel in lista_pixel:
            immagine_iniziale[pixel[0]][pixel[1]] = max(immagine_iniziale[pixel[0]][pixel[1]] - (immagine_iniziale[pixel[0]][pixel[1]]*percentuale)/100,0)
        cv2.imshow('moidificata',immagine_iniziale)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return immagine_iniziale







def get_only_contorno(immagine_iniziale,contorno):
    immagine_iniziale = cv2.cvtColor(immagine_iniziale, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(immagine_iniziale.shape[:2], np.uint8)
    cv2.drawContours(mask, [contorno], -1, 255, -1)
    result = cv2.bitwise_and(immagine_iniziale, immagine_iniziale, mask=mask)
    return result
'''
Main entry point for the filter script
'''
def main(data,path):
    print(data)
    # if data[0] != 0:
    #     contorno = get_contourn(cv2.imread(path))
    #     check = int(data[0])
    #     if check>0: 
    #         segno = 1 
    #     else: segno = -1
    #     result = modify_light_contorno(cv2.imread(path),contorno,check,segno)
    #     if data[1] and data[2] and data[3]== 'Pass': 
    #         return result
    #     else:
    #         pass
    if data[2] == 'Yes':
        print('voglio il contorno')
        contorno = get_contourn(cv2.imread(path))
        result = get_only_contorno(cv2.imread(path),contorno)
        return []
    else:
        print('non voglio il contorno')



#inserire SOLO NOME
def save_image(immagine_iniziale,nome):
    nome=nome+'.png'
    cv2.imwrite(nome,immagine_iniziale)
    return 0
    

def get_colore(img,x,y):
    #prendo quello il piu scuro tra quello a sx e dx,se entrambi = a 150 continuo
    i = 0
    while 1:
        i+=1
        try:
            cl_sx = img[x-i][y]
            cl_dx = img[x+i][y]
            if cl_sx == 150:
                if cl_dx != 150:
                    return cl_dx
            else:
                if cl_dx == 150:
                    return cl_sx
                else:
                    return min(cl_sx,cl_dx)
        except:
            pass

def leva_contorno(immagine_iniziale,contorno):
    #voglio eliminare il contorno e colorare con i pixel interni al contorno
    immagine_iniziale = cv2.cvtColor(immagine_iniziale, cv2.COLOR_BGR2GRAY)
    #ogni pixel di immagine iniziale == 150 deve prendere il valore che hail pixe piu vicino a lui  != 150

    for x in range(len(immagine_iniziale)):
        for y in range(len(immagine_iniziale)):
            try:
                if immagine_iniziale[x][y] == 150:
                    colore = get_colore(immagine_iniziale,x,y)
                    immagine_iniziale[x][y] = colore
            except:
                pass
    return immagine_iniziale



def color_contourn(immagine_iniziale,contorno):
    #coloro il contorno con un colore che fa vedere il colore originale(una specie di trasparenza)
    im_copy = immagine_iniziale.copy()
    im_copy = cv2.drawContours(im_copy, [contorno], -1, (0, 0, 255), -1)
    im = cv2.addWeighted(im_copy, 0.4, immagine_iniziale, 1 - 0.2, 0)
    im = cv2.drawContours(im, [contorno], -1, (0, 0, 255), 0)
    return im
    




if __name__=='__main__':
    contorno = get_contourn(cv2.imread('brain.png'))
    #pass
    cv2.imshow("initial",cv2.imread('brain.png'))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    img = color_contourn(cv2.imread('brain.png'),contorno)
    cv2.imshow("finale",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   # modify_light_contorno(cv2.imread('brain.png'),contorno,50,1)
   # r = get_only_contorno(cv2.imread('brain.png'),contorno)
    #cv2.imshow('r',r)
    #cv2.waitKey(0)
   # cv2.destroyAllWindows()
