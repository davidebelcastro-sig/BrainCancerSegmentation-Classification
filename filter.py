import cv2
import numpy as np




def get_contourn(immagine_segmentata):
    for x in range(len(immagine_segmentata)):
        for y in range(len(immagine_segmentata)):
            if immagine_segmentata[x][y][0] == 0 and  immagine_segmentata[x][y][1] == 255  and  immagine_segmentata[x][y][2] == 0:
                immagine_segmentata[x][y][0] = 255
                immagine_segmentata[x][y][1] = 255
                immagine_segmentata[x][y][2] = 255
            else:
                immagine_segmentata[x][y][0] = 0
                immagine_segmentata[x][y][1] = 0
                immagine_segmentata[x][y][2] = 0
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
    else:
        #tutti i pixel dentro lista_pixel li aumentiamo di percentuale
        for pixel in lista_pixel:
            immagine_iniziale[pixel[0]][pixel[1]] = max(immagine_iniziale[pixel[0]][pixel[1]] - (immagine_iniziale[pixel[0]][pixel[1]]*percentuale)/100,0)
    return immagine_iniziale







def get_only_contorno(immagine_iniziale,contorno):
    #immagine_iniziale = cv2.cvtColor(immagine_iniziale, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(immagine_iniziale.shape[:2], np.uint8)
    cv2.drawContours(mask, [contorno], -1, 255, -1)
    result = cv2.bitwise_and(immagine_iniziale, immagine_iniziale, mask=mask)
    return result



#inserire SOLO NOME
def save_image(immagine_iniziale,nome):
    nome=nome+'.png'
    cv2.imwrite(nome,immagine_iniziale)
    return 0
    
if __name__=='__main__':
    contorno = get_contourn(cv2.imread('/Users/lucian/Documents/GitHub/BrainCancerSegmentation/dev/12_46_47.png'))
    output = modify_light_contorno(cv2.imread('/Users/lucian/Documents/GitHub/BrainCancerSegmentation/dev/12_46_47.png'),contorno,150,1)
    r = get_only_contorno(output,contorno)
    cv2.imshow('r',r)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
