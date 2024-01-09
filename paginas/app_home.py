import streamlit as st
from dotenv import load_dotenv 
import os
import pymongo
import pandas as pd
import mysql
import sqlalchemy as sql
##from sqlalchemy import create_engine, text
import pandas as pd
import MySQLdb

def home():
    
    ##mkdir .streamlit; cp /etc/secrets/secrets.toml ./.streamlit/; pip install -r requirements.txt
    
    st.title('Bem Vindo ao Quant analysis of financial - QAF')

    col1, col2, col3 = st.columns([0.7,1,0.7])
    #col2.image('./imagen/analisequant_logo-removebg.png')
    
   
    
    # load_dotenv()
    
    # try:
      
    #   client = pymongo.MongoClient(st.secrets["mongo"]["url"])  
    #   db = client["libraryDB"]
    #   stock = db["stocks"]

    #   dados = stock.find_one({"index":'PETR4'})
    #   if dados:
    #         df = pd.DataFrame(dados["data"])
    #         print(df.dtypes)
    #         df['Date'] = pd.to_datetime(df['Date']).dt.date
    #         ##df['Volume'] =  df['Volume'].astype(str)
    #         df.set_index("Date",inplace=True)
             
    #         st.write( df)
      
    # except :
    #     print('erro conectar monngo')
    
    # try:
  
    #     client = pymongo.MongoClient(st.secrets["mongo"]["url"])  
    #     db = client["libraryDB"]
    #     stock = db["stocks"]

    #     dados = stock.find_one({"index":'PETR4'})
    #     if dados:
    #         df = pd.DataFrame(dados["data"])
    #         print(df.dtypes)
    #         df['Date'] = pd.to_datetime(df['Date']).dt.date
    #         ##df['Volume'] =  df['Volume'].astype(str)
    #         df.set_index("Date",inplace=True)
                
    #         st.write( df)
    
    # except:
    #     print('erro conectar monngo via env')
    
    
    # st.write( 'conexão mysql via conection') 
    
    
    # try:   
    #        st.write('Conexao via connection')
    #        query = 'SELECT * FROM ibov_b3'
    #        st.write( 'conexão mysql') 
    #        conn = st.connection("desenv_db", "sql")
    #        df = conn.query(query,ttl=600)
    #        st.write(df)
    # except:
    #      print('erro conectar bd via secrets')
        
        
    # st.write( 'testando com .env') 
    # desenv_db = os.environ.get("MYSQL_CONN") 
    # st.write( 'conexão mysql via conection '+desenv_db) 
   
        
    # st.write('testando outro meio mysql')
        
    # print('testand outro meio')
    
    # query = sql.text('SELECT * FROM desenv.ibov_b3')
    # sql_conn = sql.create_engine(desenv_db)
    # conn = sql_conn.connect()
    # df = pd.read_sql_query(query, conn)
    # st.write(df)



    st.markdown("<h2 style='text-align: center; color: rgb(74, 113, 152);'> Portal de Análises Quant financeira, onde você poderá simular e análisar diversos ativos</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: rgb(74, 113, 152)'>ATENÇÃO - Análises feitas através de APIs públicas</h4>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: rgb(74, 113, 152)'>Não são recomendações de venda/compra de ativos</h5>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: rgb(74, 113, 152);'>Funcionalidade do Portal:</h3>", unsafe_allow_html=True)
    st.markdown("***")
    st.markdown("<h4 style='text-align: center; color: rgb(74, 113, 152)'>Análise de Ativo(s) nos anos de eleições presidencias</h4>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5  = st.columns([0.1,1,0.01,1,0.1])
    col2.image('eleicoes.jpg')
    # col4.markdown("")
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Inserir os ativos da sua carteira.</h5>", unsafe_allow_html=True)
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Calcular o BETA e ver as informações sobre Hedge.</h5>", unsafe_allow_html=True)
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Analisar as correlações entre os ativos da sua carteira e principais indices.</h5>", unsafe_allow_html=True)
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Verificar a distribuição Setorial.</h5>", unsafe_allow_html=True)
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Análise de Risco x Retorno de cada Ativo.</h5>", unsafe_allow_html=True)
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Simulação da Rentabilidade da sua Carteira.</h5>", unsafe_allow_html=True)
    # st.markdown("***")
    # st.markdown("<h4 style='text-align: center; color: black;'>Correlações</h4>", unsafe_allow_html=True)
    # st.markdown("")
    # col1, col2, col3, col4, col5  = st.columns([0.1,1,0.01,1,0.1])
    # col2.image('./imagens/video_correlacao.gif')
    # col4.markdown("")
    # col4.markdown("")
    # col4.markdown("")
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Verificar as correlações entre os ativos.</h5>", unsafe_allow_html=True)
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Comparar a correlação com os principais indices.</h5>", unsafe_allow_html=True)
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Analisar a correlação no tempo.</h5>", unsafe_allow_html=True)
    # st.markdown("***")
    # st.markdown("<h4 style='text-align: center; color: black;'>Sazonalidade do Mercado</h4>", unsafe_allow_html=True)
    # st.markdown("")
    # col1, col2, col3, col4, col5  = st.columns([0.1,1,0.01,1,0.1])
    # col2.image('./imagens/video_sazonalidade.gif')
    # col4.markdown("")
    # col4.markdown("")
    # col4.markdown("")
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Analisar a sazonalidade de um deteminado ativo.</h5>", unsafe_allow_html=True)
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Ações e Indices Brasileiros e dos Estados Unidos.</h5>", unsafe_allow_html=True)
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Verificar a rentabilidade mensal.</h5>", unsafe_allow_html=True)
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Identificar padrões de comportamento ao longo do ano.</h5>", unsafe_allow_html=True)
    # st.markdown("***")
    # st.markdown("<h4 style='text-align: center; color: black;'>Raio-X do Mercado</h4>", unsafe_allow_html=True)
    # st.markdown("")
    # col1, col2, col3, col4, col5  = st.columns([0.1,1,0.01,1,0.1])
    # col2.image('./imagens/video_raiox.gif')
    # col4.markdown("")
    # col4.markdown("")
    # col4.markdown("")
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Verificar como estão as bolsas pelo mundo em tempo real.</h5>", unsafe_allow_html=True)
    # col4.markdown("<h5 style='text-align: left; color: black;'>- Dados e informações das principais bolsas.</h5>", unsafe_allow_html=True)
