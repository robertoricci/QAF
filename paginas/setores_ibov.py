import streamlit as st
import bd.mysql as conn_msysql

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def conserta_setores(setor):
    
  if setor == "Cons N  Básico" or setor == "Cons N Cíclico" or setor == "Cons N Ciclico": return "Consumo Não-Cíclico"
  if setor == "Financ e Outros" or setor == "Financeiro e Outros": return "Financeiro"
  if setor == "Bens Indls": return "Bens Industriais"
  if setor == "Utilidade Públ": return "Utilidade Pública"
  if setor == "Diverso": return "Diversos"
  
  else: return setor
  
# def conserta_subsetores(subsetor):
    
#   if subsetor == "Cons N  Básico" or subsetor == "Cons N Cíclico" or subsetor == "Cons N Ciclico": return "Consumo Não-Cíclico"
#   if subsetor == "Financ e Outros" or subsetor == "Financeiro e Outros": return "Financeiro"
#   else: return subsetor

def main():
        #código para ativar bootstrap css
        # st.markdown(
        # """
        # <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        # <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        # """,unsafe_allow_html=True
        # )  

        col1,col2 = st.columns([12,1]) 
          
        with col1:  
                                      
            st.title('Análise por Setores do IBOVESPA')
            
            st.subheader('Dados extraido da B3')
            st.write('__________')
            
            query = 'SELECT * FROM ibov_b3'
            df_ibov = conn_msysql.buscar_dados_bd(query=query)
            
            
            df_ibov['SubSetor'] = df_ibov['segmento'].apply(lambda s: s[s.rfind("/")+1:].strip())
            df_ibov['Setor']    = df_ibov['segmento'].apply(lambda s: s[:s.rfind("/")].strip())
            
            df_ibov['Setor'] = df_ibov['Setor'].apply(conserta_setores)
            #df_ibov['SubSetor'] = df_ibov['SubSetor'].apply(conserta_subsetores)
            
            query = "select  ticker, dy from ticker_sinv"
            
            df_ticker =  conn_msysql.buscar_dados_bd(query=query)
            
            df_ticker_ibov = pd.merge(df_ibov, df_ticker, how='left', left_on=['ticker'], right_on = ['ticker'])
            
            df_ticker_ibov.fillna(0)
            
            df_ticker_ibov['ticker_dy'] = df_ticker_ibov.apply(lambda x:  (x['ticker']+' - '+str(x['dy'])+'%' ), axis=1)
        
            st.markdown("<h2 style='text-align: center; color: grey;'>DY - Por Setor do IBOV</h2>", unsafe_allow_html=True)

            fig = px.sunburst(df_ticker_ibov, path=['Setor', 'SubSetor', 'ticker_dy'], values='dy', height=900,width=1300)

            fig.update_traces(textfont_color='white',
                textfont_size=14,
                ##hovertemplate='<b>%{label}:</b> %{value:.2f}%')
                hovertemplate='<b>%{label}:</b>')
            
            st.plotly_chart(fig)
            
            st.markdown("<h1 style='text-align: center; color: grey;'>Participação do IBOV</h1>", unsafe_allow_html=True)
            
            fig = px.treemap(df_ibov, path=['Setor', 'SubSetor', 'ticker'], values='part', height=900,width=1300)

            fig.update_traces(textfont_color='white',
            textfont_size=14,
            hovertemplate='<b>%{label}:</b> %{value:.2f}%')
            st.plotly_chart(fig)
            
            
            
            
            