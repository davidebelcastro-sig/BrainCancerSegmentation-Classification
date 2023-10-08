import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color
from sklearn.cluster import KMeans

# Carica l'immagine MRI del cervello
image_path = 'si3.jpg'
image = io.imread(image_path)
# Conversione in scala di grigi
gray_image = color.rgb2gray(image)

# Ridimensiona l'immagine per ridurre il tempo di esecuzione dell'algoritmo
# (Nota: potresti voler lavorare con immagini di dimensioni più grandi in pratica)
resized_image = gray_image[::2, ::2]

# Prepara i dati per l'algoritmo K-Means
rows, cols = resized_image.shape
X = resized_image.reshape(rows * cols, 1)

# Utilizza K-Means per la segmentazione in due cluster (sfondo e tumore)
num_clusters = 2
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(X)
segmented_image = kmeans.labels_.reshape(rows, cols)

# Visualizza l'immagine originale e la segmentazione
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(resized_image, cmap='gray')
plt.title('Immagine MRI originale')

plt.subplot(1, 2, 2)
plt.imshow(segmented_image, cmap='gray')
plt.title('Segmentazione del tumore')

plt.tight_layout()
plt.show()
