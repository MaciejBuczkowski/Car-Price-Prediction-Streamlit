import streamlit as st
from link import retrive_data
from sklearn.preprocessing import LabelEncoder
import joblib
import psycopg2
import pandas as pd
from valuate import prediction
import plotly.figure_factory as ff
import numpy as np
import plotly.express as px


def vis(price_array,car_data):
    cars = db.query(f"SELECT * FROM car_data WHERE make = '{car_data[0]}' AND model = '{car_data[1]}' AND vehicle_type = '{car_data[4]}' AND fuel_type = '{car_data[9]}' AND engine_size = {car_data[6]} AND trans_type = '{car_data[8]}'")
        
    #get low and high price for range based off model accuracy (using MAPE from notebook which was 0.11)
    l_price,h_price = int(round(int(price_array[1])*0.89)), int(round(int(price_array[1])*1.11))
    
    if price_array[0] > 0:
        if price_array[0] in range(l_price,h_price):
            st.success(f'The car is in the correct price range. The estimated value is between £{l_price} and £{h_price}')
        elif price_array[0] > h_price:
            st.error(f'The car is above the predicted price range. The estimated value is between £{l_price} and £{h_price}')
        elif price_array[0] < l_price:
            st.warning(f'The car is below the predicted price range. The estimated value is between £{l_price} and £{h_price}')
    else:
        st.info(f'The estimated value for this car is between {l_price} and {h_price}')
        
    '''based off feature importance graph when all variables are the same the only differenciator 
    between prices is reg year and milage. so we will do a plot for each showing the car vs 
    the market data'''
    
    reg_points = [np.array(cars['price'], cars['reg_year']), np.array([price_array[0],car_data[3]]), np.array([int(price_array[1]),car_data[3]])]
    reg_labels = ['Market', 'Actual', 'Predicted']
    
    fig = ff.create_distplot(reg_points,reg_labels)
    sc = px.area(reg_points)
    
    st.plotly_chart(fig)
    st.plotly_chart(sc)
    
    mil_points = [np.array(cars['price'], cars['reg_year']), np.array([price_array[0],car_data[5]]), np.array([int(price_array[1]),car_data[5]])]
    mil_labels = ['Market', 'Actual', 'Predicted']
    
    fig = ff.create_distplot(mil_points,mil_labels)
    
    st.plotly_chart(fig)
    
    
    

db = st.connection('postgresql',type='sql')

st.title('Car Price Evaluation')

mode = st.selectbox('Choose your mode, Link or Manual entry?:',['No Selection','Link','Manual entry'])

pred = []

if mode == 'Link':
    link = st.text_input('Link')
    click = st.button('Enter')

    if click:
        
        data = retrive_data(link)
        
        pred = prediction(data)
        
        #st.write(data)
        
        vis(pred,data)
    
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
    
    p = st.number_input('Price (For personal valuation leave at 0)',0)
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
    
    hp = st.number_input('Horsepower (For electric vehicles leave at 0. \nFor all other fuel types the modal power for that type will be chosen)',0)
    
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
    
    click = st.button('Enter')
    
    if click:
        if data[9] != 'Electric' and data[7] == 0:
            q = db.query(f"""SELECT Horsepower, COUNT(*) as num
	                        FROM (SELECT Horsepower 
	                            FROM car_data 
	                            WHERE make = '{data[0]}' 
	                            AND model = '{data[1]}' 
	                            AND engine_size = {data[6]} 
	                            AND fuel_type = '{data[9]}')
                            GROUP BY Horsepower
                            ORDER BY num DESC
                            LIMIT 1""")
            data[7] = int(q.iloc[0]['horsepower'])
            
        '''to avoid any potential issues with my university i will not be doing all of the 
        validation as i believe this should be enough to avoid any problems
        if you want it to be more robust then u will need to implement the rest. its very simple
        to do and you have an example one above. Finding the mode is the easiest way without needing
        re-input'''
        
        pred = prediction(data)
        
        #st.write(data)