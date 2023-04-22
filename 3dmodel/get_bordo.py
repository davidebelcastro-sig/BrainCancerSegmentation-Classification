import cv2
import numpy as np
import matplotlib.pyplot as plt



def fun(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img[img > 50] = 255
    img[img <= 50] = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    copia = img.copy()
    ls_contorni = []
    for cnt in contours:
        cnt = cv2.convexHull(cnt)
        if cv2.contourArea(cnt) > 60:
            ls_contorni.append(cnt)
    
    ls_contorni = np.concatenate(ls_contorni)
    #convex
    ls_contorni = cv2.convexHull(ls_contorni)
    cv2.drawContours(copia, [ls_contorni], -1, 127, -1)
    copia[copia != 127] = 0
    copia[copia == 127] = 255
    #find contours
    contours, hierarchy = cv2.findContours(copia, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(img.shape, np.uint8)
    cv2.drawContours(mask, contours, -1, 255, 1)
    return mask

if __name__ == '__main__':
    fun('/Users/lucian/Documents/GitHub/BrainCancerDetection/3dmodel/40.png')