import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB      #importo il modello
from sklearn.metrics import accuracy_score      #importo la metrica per calcolare l'accuratezza
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from tensorflow import keras
from sklearn.preprocessing import LabelBinarizer
from sklearn.neighbors import KNeighborsClassifier



def prepare():
    data = pd.read_csv('training_tumor_feature.csv')
    X_train = data.iloc[:, :-1].values #prendo tutte le righe e tutte le colonne tranne l'ultima
    y_train = data.iloc[:, -1].values # target
    data2 = pd.read_csv('testing_tumor_feature.csv')
    X_testing = data2.iloc[:, :-1].values #prendo tutte le righe e tutte le colonne tranne l'ultima
    y_testing = data2.iloc[:, -1].values # target
    return X_train, y_train, X_testing, y_testing


def SVM(X_train, y_train, X_testing, y_testing):
    model = SVC() #accuratezza del 67%
     #faccio il fit
    model.fit(X_train, y_train) #lo alleno
    #faccio la predizione
    y_model = model.predict(X_testing)
    #calcolo l'accuratezza
    accuratezza = accuracy_score(y_testing, y_model)
    ac_perc = accuratezza * 100.0
    return ac_perc
    #print(accuracy_score(y_testing, y_model)) 
    #file = pd.read_csv('testing_tumor_feature.csv')
    # Leggi una singola riga dal DataFrame
   # riga = file.iloc[50]  # Sostituisci 'n' con l'indice della riga da leggere (0 per la prima riga, 1 per la seconda, ecc.)
   # input_prova = [[riga[0],riga[1],riga[2],riga[3],riga[4],riga[5],riga[6],riga[7],riga[8],riga[9],riga[10],riga[11],riga[12],riga[13],riga[14],riga[15],
               #     riga[16],riga[17],riga[18],riga[19],riga[20],riga[21],riga[22],riga[23],riga[24],riga[25],riga[26],riga[27]]]

    # Effettua la previsione sull'input di prova
    #y_pred_prova = model.predict(input_prova)
    #print("Expected %s, Predicted %s" % (riga[28], y_pred_prova))

def GaussianNB_function(X_train, y_train, X_testing, y_testing):
    model = GaussianNB() #accuratezza del 61%
    #faccio il fit
    model.fit(X_train, y_train) #lo alleno
    #faccio la predizione
    y_model = model.predict(X_testing)
    #calcolo l'accuratezza
    accuratezza = accuracy_score(y_testing, y_model)
    ac_perc = accuratezza * 100.0
    return ac_perc
    file = pd.read_csv('testing_tumor_feature.csv')
    # Leggi una singola riga dal DataFrame
    riga = file.iloc[50]  # Sostituisci 'n' con l'indice della riga da leggere (0 per la prima riga, 1 per la seconda, ecc.)
    input_prova = [[riga[0],riga[1],riga[2],riga[3],riga[4],riga[5],riga[6],riga[7],riga[8],riga[9],riga[10],riga[11],riga[12],riga[13],riga[14],riga[15],
                    riga[16],riga[17],riga[18],riga[19],riga[20],riga[21],riga[22],riga[23],riga[24],riga[25],riga[26],riga[27]]]

    # Effettua la previsione sull'input di prova
    y_pred_prova = model.predict(input_prova)
    print("Expected %s, Predicted %s" % (riga[28], y_pred_prova))




def RF(X_train, y_train, X_testing, y_testing):
    model = RandomForestClassifier() #79% di accuratezza
    #faccio il fit
    model.fit(X_train, y_train) #lo alleno
    #faccio la predizione
    y_model = model.predict(X_testing)
    #calcolo l'accuratezza
    accuratezza = accuracy_score(y_testing, y_model)
    ac_perc = accuratezza * 100.0
    return ac_perc 
    file = pd.read_csv('testing_tumor_feature.csv')
    # Leggi una singola riga dal DataFrame
    riga = file.iloc[50]  # Sostituisci 'n' con l'indice della riga da leggere (0 per la prima riga, 1 per la seconda, ecc.)
    input_prova = [[riga[0],riga[1],riga[2],riga[3],riga[4],riga[5],riga[6],riga[7],riga[8],riga[9],riga[10],riga[11],riga[12],riga[13],riga[14],riga[15],
                    riga[16],riga[17],riga[18],riga[19],riga[20],riga[21],riga[22],riga[23],riga[24],riga[25],riga[26],riga[27]]]

    # Effettua la previsione sull'input di prova
    y_pred_prova = model.predict(input_prova)
    print("Expected %s, Predicted %s" % (riga[28], y_pred_prova))



def CNN(X_train, y_train, X_testing, y_testing):
    #faccio con CNN
    # Creo il modello
    model = keras.models.Sequential()

    # Aggiungo i layer completamente connessi
    model.add(keras.layers.Dense(64, activation='relu', input_shape=(28,)))
    model.add(keras.layers.Dense(32, activation='relu'))

    # Aggiungo il layer di output
    model.add(keras.layers.Dense(3, activation='softmax')) #3 perchè ho 3 classi:pituitary, meningioma, glioma

    # Compilo il modello
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    #pituary,glioma,meningioma



    # Crea un istanza di LabelBinarizer
    label_binarizer = LabelBinarizer()

    # Fit e trasforma le etichette in one-hot encoding
    y_train = label_binarizer.fit_transform(y_train)


    # Faccio il fit
    model.fit(X_train, y_train, epochs=10, batch_size=32)

    # Faccio la predizione
    y_model = model.predict(X_testing)

    y_testing = label_binarizer.fit_transform(y_testing)
    #calcolo l'accuratezza
    #print(accuracy_score(y_testing, y_model)) #stampo l'accuratezza
    #print(y_testing) #glioma meningioma pituitary
    file = pd.read_csv('testing_tumor_feature.csv')
    # Leggi una singola riga dal DataFrame
    riga = file.iloc[50]  # Sostituisci 'n' con l'indice della riga da leggere (0 per la prima riga, 1 per la seconda, ecc.)

    input_prova = [[riga[0],riga[1],riga[2],riga[3],riga[4],riga[5],riga[6],riga[7],riga[8],riga[9],riga[10],riga[11],riga[12],riga[13],riga[14],riga[15],
                    riga[16],riga[17],riga[18],riga[19],riga[20],riga[21],riga[22],riga[23],riga[24],riga[25],riga[26],riga[27]]]

    # Effettua la previsione sull'input di prova
    y_pred_prova = model.predict(input_prova)
    print("Expected %s, Predicted %s" % (riga[28], y_pred_prova))

def KNN(X_train, y_train, X_testing, y_testing):
    
    # Creazione del modello KNN
    model = KNeighborsClassifier(n_neighbors=3)  # Imposta il numero di vicini desiderato (k=3)
    #faccio il fit
    model.fit(X_train, y_train) #lo alleno
    #faccio la predizione
    y_model = model.predict(X_testing)
    #calcolo l'accuratezza
    accuratezza = accuracy_score(y_testing, y_model)
    ac_perc = accuratezza * 100.0
    return ac_perc 
   # file = pd.read_csv('testing_tumor_feature.csv')
    # Leggi una singola riga dal DataFrame
    #riga = file.iloc[50]  # Sostituisci 'n' con l'indice della riga da leggere (0 per la prima riga, 1 per la seconda, ecc.)
    #input_prova = [[riga[0],riga[1],riga[2],riga[3],riga[4],riga[5],riga[6],riga[7],riga[8],riga[9],riga[10],riga[11],riga[12],riga[13],riga[14],riga[15],
                    #riga[16],riga[17],riga[18],riga[19],riga[20],riga[21],riga[22],riga[23],riga[24],riga[25],riga[26],riga[27]]]

    # Effettua la previsione sull'input di prova
    #y_pred_prova = model.predict(input_prova)
    #print("Expected %s, Predicted %s" % (riga[28], y_pred_prova))


def start():
    X_train, y_train, X_testing, y_testing = prepare()
    ac = SVM(X_train, y_train, X_testing, y_testing)
    ac = GaussianNB_function(X_train, y_train, X_testing, y_testing)
    ac= RF(X_train, y_train, X_testing, y_testing) #attualmente il migliore
    ac = KNN(X_train, y_train, X_testing, y_testing)
    #CNN(X_train, y_train, X_testing, y_testing)





