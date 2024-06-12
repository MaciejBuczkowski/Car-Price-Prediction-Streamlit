import streamlit as st
from link import retrive_data


#db = st.connection('postgres',type='sql')
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