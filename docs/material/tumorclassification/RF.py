from sklearn.metrics import accuracy_score      #importo la metrica per calcolare l'accuratezza
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle





def prepare():
    data = pd.read_csv('training_tumor_feature.csv')
    X_train = data.iloc[:, :-1].values #prendo tutte le righe e tutte le colonne tranne l'ultima
    y_train = data.iloc[:, -1].values # target
    data2 = pd.read_csv('testing_tumor_feature.csv')
    X_testing = data2.iloc[:, :-1].values #prendo tutte le righe e tutte le colonne tranne l'ultima
    y_testing = data2.iloc[:, -1].values # target
    return X_train, y_train, X_testing, y_testing

def trainRF(X_train, y_train):
    # Salvataggio del modello
    model = RandomForestClassifier() #79% di accuratezza
    #faccio il fit
    model.fit(X_train, y_train) #lo alleno
    with open('modello_rf.pkl', 'wb') as file:
        pickle.dump(model, file)

def Testing(X_testing, y_testing):
    # Caricamento del modello
    with open('modello_rf.pkl', 'rb') as file:
        model = pickle.load(file)
    y_model = model.predict(X_testing)
    #calcolo l'accuratezza
    accuratezza = accuracy_score(y_testing, y_model)
    print("Accuratezza: %.2f%%" % (accuratezza * 100.0))













    
    #file = pd.read_csv('testing_tumor_feature.csv')
    # Leggi una singola riga dal DataFrame
    #riga = file.iloc[50]  # Sostituisci 'n' con l'indice della riga da leggere (0 per la prima riga, 1 per la seconda, ecc.)
    #input_prova = [[riga[0],riga[1],riga[2],riga[3],riga[4],riga[5],riga[6],riga[7],riga[8],riga[9],riga[10],riga[11],riga[12],riga[13],riga[14],riga[15],
                    #riga[16],riga[17],riga[18],riga[19],riga[20],riga[21],riga[22],riga[23],riga[24],riga[25],riga[26],riga[27]]]

    # Effettua la previsione sull'input di prova
    #y_pred_prova = model.predict(input_prova)
    #print("Expected %s, Predicted %s" % (riga[28], y_pred_prova))


if __name__ == '__main__':
    X_train, y_train, X_testing, y_testing = prepare()
    #trainRF(X_train, y_train)
    Testing(X_testing, y_testing)

