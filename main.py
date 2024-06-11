import streamlit as st
import requests
from bs4 import BeautifulSoup

#db = st.connection('postgres',type='sql')
st.title('Car Price Evaluation')

mode = st.selectbox('Choose your mode, Link or Manual entry?:',['Link','Manual entry'])

if mode == 'Link':
    link = st.text_input('Link')
    click = st.button('Enter')

    if click:
        car = requests.get(link)
        
        st.write(car.text)
        
        soup = BeautifulSoup(car.text, 'html.parser')
        
        f = soup.find_all('p', class_="at__sc-efqqw2-6 gIURrd")
        s = soup.find_all('span', class_="at__sc-1n64n0d-7 at__sc-6lr8b9-4 fcDnGr gJQNgz")
        
        st.write('first section: ' + str(len(f)))
        st.write('second section: ' + str(len(s)))
    
elif mode == 'Manual entry':
    st.write('Manual mode')