import cv2
import numpy as np
import mahotas as mh



def calculate_characteristics(contour, original_image):
    # Crea una maschera vuota
    mask = np.zeros(original_image.shape[:2], dtype=np.uint8)

    # Disegna il contorno sulla maschera
    cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

    # Estrai il tumore dalla maschera
    tumor = cv2.bitwise_and(original_image, original_image, mask=mask)

    # Calcola le caratteristiche per il tumore

    # Calcola l'area e il perimetro
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)

    # Calcola la solidità
    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    solidity = area / hull_area

    # Calcola il rettangolo delimitante
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(w) / h

    # Calcola l'eccentricità
    (cx, cy), (major_axis, minor_axis), angle = cv2.fitEllipse(contour)
    eccentricity = major_axis / minor_axis

    # Calcola i momenti di Hu
    moments = cv2.moments(contour)
    hu_moments = cv2.HuMoments(moments).flatten()
    #divido in 7 momenti
    hu_moment1 = hu_moments[0]
    hu_moment2 = hu_moments[1]
    hu_moment3 = hu_moments[2]
    hu_moment4 = hu_moments[3]
    hu_moment5 = hu_moments[4]
    hu_moment6 = hu_moments[5]
    hu_moment7 = hu_moments[6]

    # Calcola l'intensità media
    mean_intensity = np.mean(tumor)

    # Calcola il gradiente di intensità
    gradient_image = cv2.cvtColor(tumor, cv2.COLOR_BGR2GRAY)
    gradient_x = cv2.Sobel(gradient_image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(gradient_image, cv2.CV_64F, 0, 1, ksize=3)
    intensity_gradient = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
    mean_intensity_gradient = np.mean(intensity_gradient)

    gray_tumor = cv2.cvtColor(tumor, cv2.COLOR_BGR2GRAY)
  

    # Calcola il rapporto delle frequenze spettrali
    fft = np.fft.fft2(gray_tumor)
    spectrum = np.abs(fft) ** 2
    spectral_ratio = np.sum(spectrum[8:40, 8:40]) / np.sum(spectrum[40:, 40:])

    #caratteristiche texture
    texture_features = getTexture(tumor)
    out = [[area, perimeter, solidity, aspect_ratio, eccentricity, hu_moment1, hu_moment2, hu_moment3, hu_moment4,
             hu_moment5, hu_moment6, hu_moment7, mean_intensity, mean_intensity_gradient, spectral_ratio,
                         texture_features[0], texture_features[1], texture_features[2], texture_features[3], 
                         texture_features[4], texture_features[5], texture_features[6], texture_features[7], texture_features[8], 
                         texture_features[9], texture_features[10], texture_features[11], texture_features[12]]]

    return out

def getTexture(image):
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Calcola la matrice di co-occorrenza dei livelli di grigio
    
# Calcola la texture utilizzando la funzione haralick di mahotas
    texture_features = mh.features.haralick(image_gray)
    mean_texture_features = np.mean(texture_features, axis=0)
    #calcolo la media delle 13 features
    return mean_texture_features

