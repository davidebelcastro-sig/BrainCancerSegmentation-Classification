import matplotlib.pyplot as plt
import numpy as np
import all_method




def get_graph():
    X_train, y_train, X_testing, y_testing = all_method.prepare()
    perc_giusteSVM =  all_method.SVM(X_train, y_train, X_testing, y_testing)
    perc_giusteNB =  all_method.GaussianNB_function(X_train, y_train, X_testing, y_testing)
    perc_giusteRF =  all_method.RF(X_train, y_train, X_testing, y_testing) #attualmente il migliore
    perc_giusteKNN =  all_method.KNN(X_train, y_train, X_testing, y_testing)
    
    perc_sbagliateSVM = 100 - perc_giusteSVM
    perc_sbagliateNB = 100 - perc_giusteNB
    perc_sbagliateRF = 100 - perc_giusteRF
    perc_sbagliateKNN = 100 - perc_giusteKNN

    #approssimo
    perc_giusteSVM = round(perc_giusteSVM, 2)
    perc_giusteNB = round(perc_giusteNB, 2)
    perc_giusteRF = round(perc_giusteRF, 2)
    perc_giusteKNN = round(perc_giusteKNN, 2)
    perc_sbagliateSVM = round(perc_sbagliateSVM, 2)
    perc_sbagliateNB = round(perc_sbagliateNB, 2)
    perc_sbagliateRF = round(perc_sbagliateRF, 2)
    perc_sbagliateKNN = round(perc_sbagliateKNN, 2)

    ySVM = np.array([perc_giusteSVM,perc_sbagliateSVM])
    mylabelsSVM = ["Giuste:"+str(perc_giusteSVM)+"%","Errate:"+str(perc_sbagliateSVM)+"%"]
    plt.pie(ySVM, labels = mylabelsSVM)
    plt.title("Attendibilità tumor classification\nGrafico totale")
    plt.savefig('attendibilità_tumor_classification_SVM.png')

    #svuoto il grafico
    plt.clf()

    yNB = np.array([perc_giusteNB,perc_sbagliateNB])
    mylabelsNB = ["Giuste:"+str(perc_giusteNB)+"%","Errate:"+str(perc_sbagliateNB)+"%"]
    plt.pie(yNB, labels = mylabelsNB)
    plt.title("Attendibilità tumor classification\nGrafico totale")
    plt.savefig('attendibilità_tumor_classification_NB.png')

    plt.clf()
    yRF = np.array([perc_giusteRF,perc_sbagliateRF])
    mylabelsRF = ["Giuste:"+str(perc_giusteRF)+"%","Errate:"+str(perc_sbagliateRF)+"%"]
    plt.pie(yRF, labels = mylabelsRF)
    plt.title("Attendibilità tumor classification\nGrafico totale")
    plt.savefig('attendibilità_tumor_classification_RF.png')

    plt.clf()
    yKNN = np.array([perc_giusteKNN,perc_sbagliateKNN])
    mylabelsKNN = ["Giuste:"+str(perc_giusteKNN)+"%","Errate:"+str(perc_sbagliateKNN)+"%"]
    plt.pie(yKNN, labels = mylabelsKNN)
    plt.title("Attendibilità tumor classification\nGrafico totale")
    plt.savefig('attendibilità_tumor_classification_KNN.png')
    #plt.show() 


if __name__ == "__main__":
    get_graph()

