import numpy as np
import h5py
import matplotlib.pyplot as plt
import os
import cv2

def run(dir):
        fatte = 0
        glioma_number = 663
        meningioma_number = 705
        pituitary_number = 926
        for file in os.listdir(dir):
            f = h5py.File(dir+'/'+file,'r')
            for el in f['cjdata']:
                if el == 'image':
                    image = f['cjdata'][el]
                elif el == 'label':
                    label = f['cjdata'][el]
                    label = label[0][0]
                    label = int(label)
                    label = str(label)
                elif el == 'tumorMask':
                    border = f['cjdata'][el]

            plt.imshow(image,cmap='gray')
            plt.axis('off')
            plt.savefig('brain.png')
            #show tumor on brain
            plt.imshow(border,cmap='gray')
            plt.axis('off')
            plt.savefig('tumor.png')

            #show tumor on brain
            plt.imshow(image,cmap='gray')
            plt.imshow(border,cmap='jet',alpha=0.5)  
            plt.savefig('tumor_on_brain.png')
            plt.axis('on')
            bord = cv2.imread('tumor.png')
            img = cv2.imread('brain.png')  #3 canali

            bord = cv2.cvtColor(bord, cv2.COLOR_BGR2GRAY)
            #find contours
            contours, hierarchy = cv2.findContours(bord,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            #sorted
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            #terzo
            cnt = contours[2]
            mask_appo = np.zeros_like(bord)
            cv2.drawContours(mask_appo, [cnt], -1, 255, -1)
            bord = mask_appo
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            only_tumor = cv2.bitwise_and(img, bord)  #prendo solo il tumore,sfondo nero
            
            if label == "1":
                cv2.imwrite('./dataset_creato/meningioma/'+str(meningioma_number)+'.png',only_tumor)
                meningioma_number += 1
            elif label == "2":
                cv2.imwrite('./dataset_creato/glioma/'+str(glioma_number)+'.png',only_tumor)
                glioma_number += 1
            elif label == "3":
                cv2.imwrite('./dataset_creato/pituitary/'+str(pituitary_number)+'.png',only_tumor)
                pituitary_number += 1
            print("label: ",label)
            fatte += 1
            if fatte % 100 == 0:
                print("fatto: ",fatte)
if __name__ == "__main__":
    run("./dataset/brainTumorDataPublic_2299-3064")