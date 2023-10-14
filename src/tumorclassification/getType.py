import pickle
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings


def get_tumor_type(tumor_feautures):
    directory = settings.path_to_model
    try:
        with open(directory, 'rb') as file:
            model = pickle.load(file)
            prediction = model.predict(tumor_feautures)
            return prediction[0]
    except:
        return "error"