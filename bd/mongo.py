
import pymongo
import streamlit as st
import pandas as pd

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["url"])  

@st.cache_data(ttl=600)
def find_one(collecion,ticker):
    
    client = init_connection()
    db = client["libraryDB"]
    stock = db["stocks"]
    
    dados = stock.find_one({"index":ticker})
    if dados:
        df = pd.DataFrame(dados["data"])
        print(df.dtypes)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        ##df['Volume'] =  df['Volume'].astype(str)
        df.set_index("Date",inplace=True)
        
    else:
        df = pd.DataFrame()
    
    return df
    