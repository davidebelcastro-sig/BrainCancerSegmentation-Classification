import pickle




def get_tumor_type(tumor_feautures):
    # Caricamento del modello
    try:
        with open('./src/tumorclassification/modello_rf.pkl', 'rb') as file:
            model = pickle.load(file)
        prediction = model.predict(tumor_feautures)
        return prediction[0]
    except:
        return "error"

