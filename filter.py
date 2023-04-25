import cv2
import numpy as np

def get_contourn_external_withBord(brain):
    brain = cv2.cvtColor(brain, cv2.COLOR_BGR2GRAY)
    j = brain.copy()
    #v2.imshow('brain',j)
    j[j == 255]  = 0 
    j[j <=4]  = 0
    for i in range(0,brain.shape[0]):
        for y in range(0,brain.shape[1]):
            if j[i][y] != 0:
                j[i][y] = 255

    #find contours
    contours, hierarchy = cv2.findContours(j,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #disegno il piu grande contorno
    countour = max(contours, key=cv2.contourArea)
    #disegno contorno
    #cv2.imshow('contorno_esterno',countour)
    return countour

#elimina bordo:ritorno l'immagine iniziale
def remove_border(immagine_iniziale):
    return immagine_iniziale

#modificare luce del contorno
def modify_light_contorno(immagine_iniziale,contorno,percentuale,segno):
    immagine_iniziale = cv2.cvtColor(immagine_iniziale, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('immagine_iniziale',immagine_iniziale)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    copia = immagine_iniziale.copy()
    lista_pixel = []
    cv2.drawContours(copia, [contorno], -1, 255, -1)
    for i in range(0,immagine_iniziale.shape[0]):
        for y in range(0,immagine_iniziale.shape[1]):
            if copia[i][y] == 255:
                lista_pixel.append((i,y))
    #tutto quello dentro il contorno lo auemtno/abbassiamo di percentuale
    if segno == 1:
        #tutti i pixel dentro lista_pixel li aumentiamo di percentuale
        for pixel in lista_pixel:
            #aumento del percnetuale percento
            immagine_iniziale[pixel[0]][pixel[1]]=min(immagine_iniziale[pixel[0]][pixel[1]] + (immagine_iniziale[pixel[0]][pixel[1]]*percentuale)/100,255)
        # cv2.imshow('moidificata',immagine_iniziale)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    else:
        #tutti i pixel dentro lista_pixel li aumentiamo di percentuale
        for pixel in lista_pixel:
            immagine_iniziale[pixel[0]][pixel[1]] = max(immagine_iniziale[pixel[0]][pixel[1]] - (immagine_iniziale[pixel[0]][pixel[1]]*percentuale)/100,0)
        # cv2.imshow('moidificata',immagine_iniziale)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    return immagine_iniziale

def get_only_contorno(immagine_iniziale,contorno):
    immagine_iniziale = cv2.cvtColor(immagine_iniziale, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(immagine_iniziale.shape[:2], np.uint8)
    cv2.drawContours(mask, [contorno], -1, 255, -1)
    result = cv2.bitwise_and(immagine_iniziale, immagine_iniziale, mask=mask)
    return result


def save_image(immagine_iniziale,nome):
    nome=nome+'.png'
    cv2.imwrite(nome,immagine_iniziale)
    return 0

def main(data,path):

    if data[0] != 0:
        contorno = get_contourn_external_withBord(cv2.imread(path))
        check = int(data[0])
        if check>0: 
            segno = 1 
        else: segno = -1
        result = modify_light_contorno(cv2.imread(path),contorno,check,segno)
        if data[1] and data[2] == 'Pass':
            #TODO: salvare l'immagine e ritorna il path 
            return result
            pass
        else:
            pass
    print("devo fare altre cose")

# if __name__=='__main__':
#     contorno = get_contourn_external_withBord(cv2.imread('/Users/lucian/Documents/GitHub/BrainCancerDetection/10:59:09.png'))
#     print(contorno)
#     #modify_light_contorno(cv2.imread('/Users/lucian/Documents/GitHub/BrainCancerDetection/10:59:09.png'),contorno,100,1)
#     #r = get_only_contorno(cv2.imread('/Users/lucian/Documents/GitHub/BrainCancerDetection/10:59:09.png'),contorno)
#     #cv2.imshow('r',r)
#     #cv2.waitKey(0)
#     #cv2.destroyAllWindows()
#     pass