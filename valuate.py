import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd

#model
rf = joblib.load('RF_Model.joblib')

#encoders
make_enc = joblib.load('Encoders/make_classes.joblib')
model_enc = joblib.load('Encoders/model_classes.joblib')
vec_type_enc = joblib.load('Encoders/vec_type_classes.joblib')
tran_type_enc = joblib.load('Encoders/tran_type_classes.joblib')
fuel_type_enc = joblib.load('Encoders/fuel_type_classes.joblib')

def prediction(data):
    
    make = make_enc.transform([data[0]])
    model = model_enc.transform([data[1]])
    year = pd.to_numeric(data[3])
    vec = vec_type_enc.transform([data[4]])
    miles = pd.to_numeric(data[5])
    es = pd.to_numeric(data[6])
    hp = pd.to_numeric(data[7])
    tran = tran_type_enc.transform([data[8]])
    fuel = fuel_type_enc.transform([data[9]])
    
    v = [make,model,year,vec,miles,es,hp,tran,fuel]
    
    vehicle = np.array(v, dtype=object)
    
    p_price = rf.predict([vehicle])
    
    price_arr = [data[2],p_price]
    
    return price_arr