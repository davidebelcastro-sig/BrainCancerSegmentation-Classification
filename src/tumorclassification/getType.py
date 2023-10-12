import pickle

def get_tumor_type(tumor_feautures):
    # Caricamento del modello
    directory = "/Users/lucian/GitHub/BrainCancerSegmentation-Classification/src/tumorclassification/modello_rf.pkl"
    #path = "./src/tumorclassification/modello_rf.pkl"
    try:
        with open(directory, 'rb') as file:
            model = pickle.load(file)
            prediction = model.predict(tumor_feautures)
            return prediction[0]
    except:
        return "error"