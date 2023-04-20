import cv2
import numpy as np
import matplotlib.pyplot as plt
import get_bordo
from matplotlib.colors import LightSource

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
lista_pixel = []
#trova il contorno del rettangolo
dist = 1
start = 100
for k in range(1,97):
        img = get_bordo.fun(str(k)+'.png')
        for i in range(len(img)):
            for j in range(len(img[i])):
                if img[i][j] == 255:
                    lista_pixel.append([i,j,start])
        start -= dist
for el in lista_pixel:
        ax.scatter(el[0],el[1],el[2],c='gray')
        

    
ax.set_xlabel('X Label')
#scrivo su assey
ax.set_ylabel('Y Label')
#scrivo su assez
ax.set_zlabel('Z Label')
#setto lunghezza asse z




plt.show()