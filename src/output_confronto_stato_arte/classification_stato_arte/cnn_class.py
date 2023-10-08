import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import cv2
import tensorflow as tf
from tqdm import tqdm
import os
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,confusion_matrix
import ipywidgets as widgets
import io
from PIL import Image
from IPython.display import display,clear_output
from warnings import filterwarnings


'''
effnet = tf.keras.applications.EfficientNetB0(weights='imagenet',include_top=False,input_shape=(image_size,image_size,3))
model = effnet.output
model = tf.keras.layers.GlobalAveragePooling2D()(model)
model = tf.keras.layers.Dropout(rate=0.5)(model)
model = tf.keras.layers.Dense(4,activation='softmax')(model)
model = tf.keras.models.Model(inputs=effnet.input, outputs = model)

model.summary()
model.compile(loss='categorical_crossentropy',optimizer = 'Adam', metrics= ['accuracy'])


tensorboard = tf.keras.callbacks.TensorBoard(log_dir = 'logs')
checkpoint = tf.keras.callbacks.ModelCheckpoint("effnet.h5",monitor="val_accuracy",save_best_only=True,mode="auto",verbose=1)
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor = 'val_accuracy', factor = 0.3, patience = 2, min_delta = 0.001,
                              mode='auto',verbose=1)




history = model.fit(X_train,y_train,validation_split=0.1, epochs =2, verbose=1, batch_size=32,
                   callbacks=[tensorboard,checkpoint,reduce_lr])



pred = model.predict(X_test)
pred = np.argmax(pred,axis=1)
y_test_new = np.argmax(y_test,axis=1)
print(classification_report(y_test_new,pred))


'''

for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
colors_dark = ["#1F1F1F", "#313131", '#636363', '#AEAEAE', '#DADADA']
colors_red = ["#331313", "#582626", '#9E1717', '#D35151', '#E9B4B4']
colors_green = ['#01411C','#4B6F44','#4F7942','#74C365','#D0F0C0']

sns.palplot(colors_dark)
sns.palplot(colors_green)
sns.palplot(colors_red)

labels = ['glioma_tumor','no_tumor','meningioma_tumor','pituitary_tumor']

X_train = []
y_train = []
image_size = 150
for i in labels:
    folderPath = os.path.join('.','Training',i)
    for j in tqdm(os.listdir(folderPath)):
        img = cv2.imread(os.path.join(folderPath,j))
        img = cv2.resize(img,(image_size, image_size))
        X_train.append(img)
        y_train.append(i)
        
for i in labels:
    folderPath = os.path.join('.','Testing',i)
    for j in tqdm(os.listdir(folderPath)):
        img = cv2.imread(os.path.join(folderPath,j))
        img = cv2.resize(img,(image_size,image_size))
        X_train.append(img)
        y_train.append(i)
        
X_train = np.array(X_train)
y_train = np.array(y_train)


X_train, y_train = shuffle(X_train,y_train, random_state=101)





X_train,X_test,y_train,y_test = train_test_split(X_train,y_train, test_size=0.1,random_state=101)





y_train_new = []
for i in y_train:
    y_train_new.append(labels.index(i))
y_train = y_train_new
y_train = tf.keras.utils.to_categorical(y_train)


y_test_new = []
for i in y_test:
    y_test_new.append(labels.index(i))
y_test = y_test_new
y_test = tf.keras.utils.to_categorical(y_test)



loaded_model = tf.keras.models.load_model('effnet.h5')

# Effettua previsioni su nuovi dati (ad esempio, X_test)
predictions = loaded_model.predict(X_test)

# Converti le previsioni in etichette di classe
predicted_labels = np.argmax(predictions, axis=1)

# Stampa il report di classificazione
print(classification_report(y_test_new, predicted_labels))

img = Image.open('Testing/glioma_tumor/gg (10).jpg')
opencvImage = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
img = cv2.resize(opencvImage,(150,150))
img = img.reshape(1,150,150,3)
p = loaded_model.predict(img)
p = np.argmax(p,axis=1)[0]
if p==0:
    p='Glioma Tumor'
elif p==2:
    p='Meningioma Tumor'
else:
    p='Pituitary Tumor'
predicted_class = p

print(predicted_class)
