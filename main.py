import streamlit as st
from link import retrive_data
from sklearn.preprocessing import LabelEncoder
import joblib
import psycopg2


db = st.connection('postgresql',type='sql')

st.title('Car Price Evaluation')

mode = st.selectbox('Choose your mode, Link or Manual entry?:',['No Selection','Link','Manual entry'])

if mode == 'Link':
    link = st.text_input('Link')
    click = st.button('Enter')

    if click:
        
        data = retrive_data(link)
        
        st.write(data)
    
elif mode == 'Manual entry':
    st.write('Manual mode')
    
    data = []
    
    makes = ['No selection']
    mks = joblib.load('Encoders/make_classes.joblib').classes_
    for m in mks:
        makes.append(m)
    
    make = st.selectbox('Make:',makes)
    
    mdls = db.query(f"SELECT DISTINCT Model FROM car_data WHERE Make = '{make}'")
    models = ['No selection']
    for m in mdls.itertuples():
        models.append(m.model)
    
    model = st.selectbox('Model:', models)
    
    m = st.number_input('Miles',0)
    miles = int(m)
    
    p = st.number_input('Price (For valuation leave at 0)',0)
    price = int(p)
    
    y = []
    tmp = []
    if make != 'No selection' and model != 'No selection':
        years = db.query(f"SELECT DISTINCT reg_year FROM car_data WHERE make = '{make}' AND model = '{model}'")
        for i in years.itertuples():
            tmp.append(i.reg_year)
        
        min,max = min(tmp),max(tmp)
        for j in range(min,max):
            y.append(j)
        
    year = st.selectbox('Registration Year',y)
    
    e = [0.0]
    if y != []:
        en = db.query(f"SELECT DISTINCT engine_size FROM car_data WHERE make = '{make}' AND model = '{model}' AND reg_year = {year}")
        for i in en.itertuples():
            e.append(i.engine_size)
        
    es = st.selectbox('Engine Size',e)
    
    f = ['No selection']
    if y != []:
        ft = db.query(f"SELECT DISTINCT fuel_type FROM car_data WHERE make = '{make}' AND model = '{model}' AND reg_year = {year}")
        for i in ft.itertuples():
            f.append(i.fuel_type)
            
    fuel = st.selectbox('Fuel Type',f)
    
    t = ['No selection']
    tt = db.query(f"SELECT DISTINCT trans_type FROM car_data WHERE make = '{make}' AND model = '{model}'")
    for i in tt.itertuples():
        t.append(i.trans_type)
        
    tran = st.selectbox('Transmission', t)
    
    v = ['No selection']
    vt = db.query(f"SELECT DISTINCT vehicle_type FROM car_data WHERE make = '{make}' AND model = '{model}'")
    for i in vt.itertuples():
        v.append(i.vehicle_type)
        
    vec = st.selectbox('Body Type',v)
    
    hp = st.number_input('Horsepower (for electric vehicles leave at 0)',0)
    
    #appending all in order to make array for program use
    data.append(make)
    data.append(model)
    data.append(price)
    data.append(year)
    data.append(vec)
    data.append(miles)
    data.append(es)
    data.append(hp)
    data.append(tran)
    data.append(fuel)
    
    