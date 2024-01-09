
import streamlit as st


# import sqlalchemy as sql
# from sqlalchemy import create_engine, text

@st.cache_data(show_spinner="Carregando dados mysql...", ttl=600)
def buscar_dados_bd(query):
        conn = st.connection("desenv_db", "sql")
        df = conn.query(query,ttl=600)
        return  df