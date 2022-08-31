import pandas as pd
import pickle
import numpy as np

MODEL_PATH = 'finalized_model.sav'

def predict(feature_df = pd.DataFrame()):
    loaded_model = pickle.load(open(MODEL_PATH, 'rb'))
    result = loaded_model.predict(feature_df)
    return np.argmax(result)
