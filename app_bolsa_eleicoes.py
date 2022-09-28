import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
#import numpy as np
#import pandas as pd
# import yfinance as yf
# #import time
# import matplotlib.pyplot as plt
# import plotly.express as px
# import seaborn as sns
# import cufflinks as cf
# #import datetime
# #from datetime import date
# import math
# import fundamentus


# st.set_page_config(  # Alternate names: setup_page, page, layout
# 	layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
# 	initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
# 	page_title="",  # String or None. Strings get appended with "• Streamlit". 
# 	page_icon=None,  # String, anything supported by st.image, or None.
# )

def bolsa():
         #código para ativar bootstrap css
    st.markdown(
"""
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""",unsafe_allow_html=True
    ) 
    st.title('Análise Bolsa de Valores nas ultimas eleições presidencias')

    df = puxar_dados('^BVSP','1998-01-01','2022-09-30')
    
    df['ano'] = df.index.year
    df['dia_do_ano'] = df.index.dayofyear
# nova coluna data e ano

    tb = df.pivot( index='dia_do_ano', columns='ano', values='Adj Close')
    tab = tb.fillna(method='bfill')

    tab.pct_change()

    tab = ( tab/tab.iloc[0] ) - 1

    #gerar grafico
    gerar_grafico(tab)
    

def gerar_grafico_unid(tab,ticker):
    #anos das eleições
    listano = tab.columns
    anosvalido = [1998,2002,2006,2014,2018] 
    
    anos = [s for s in listano if s in anosvalido ]
    
    tabf = tab[anos]
    
    fig = px.line(
        tabf,
        height=600,
        width=1000,
        labels={'Value':'retorno'}
    )
    fig.add_vline( x= pd.to_datetime('2022-10-01').dayofyear ,line_dash="dash",line_color="blue")
    fig.add_vline( x= pd.to_datetime('2022-10-31').dayofyear, line_dash="dash",line_color="blue")
    fig.update_traces(line=dict(width=1)
                      
    )
    
    fig.add_scatter(
        x=tab.index,
        y=tab[2022],
        name='2022',
        line=dict(width=3),
    )
    # fig.update_traces(hovertemplate='dia_ano: %{x} <br>Retorno: %{y}  ')
    
    fig.update_traces( hovertemplate='<b>Retorno: </b> %{y:.0%}'+
                                       '<br><b>Dia Ano:</b> %{x:}')
    
    fig.layout.yaxis.tickformat = '.0%'
    
    anos = anos + [2022]

    fig.update_layout(
        title='Performance do Ativo '+ ticker + ' nos anos eleitorais ' + str(anos),
        xaxis_title='Dia do Ano',
        yaxis_title='Retorno',
        template='plotly_dark',
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            showticklabels=True,
            tickformat = '.0%'
        )
        
    )
    
    st.plotly_chart(fig,use_container_width=True)   
    
@st.cache(allow_output_mutation=True)
def puxar_dados(ticker,dt_ini,dt_fim):
    precos = yf.download(ticker, start=dt_ini, end=dt_fim, progress=False)[['Adj Close']]
    #precos = precos.fillna(method='bfill')
    return precos

def gerar_grafico(tab):
    #anos das eleições
    listano = tab.columns
    anosvalido = [1998,2002,2006,2014,2018] 
    
    anos = [s for s in listano if s in anosvalido ]
    
    tabf = tab[anos]
    
    fig = px.line(
        tabf,
        height=600,
        width=1000,
        labels={'Value':'retorno'}
    )
    fig.add_vline( x= pd.to_datetime('2022-10-01').dayofyear ,line_dash="dash",line_color="blue")
    fig.add_vline( x= pd.to_datetime('2022-10-31').dayofyear, line_dash="dash",line_color="blue")
    fig.update_traces(line=dict(width=1)                
    )
    
    fig.add_scatter(
        x=tab.index,
        y=tab[2022],
        name='2022',
        line=dict(width=3),
    )
    # fig.update_traces(hovertemplate='dia_ano: %{x} <br>Retorno: %{y}  ')
    
    fig.update_traces( hovertemplate='<b>Retorno: </b> %{y:.0%}'+
                                       '<br><b>Dia Ano:</b> %{x:}')

    fig.update_layout(
        title='Performance Indice Bovespa (IBOV) no anos eleitorias [1998,2002,2006,2014,2018 e 2022]',
        xaxis_title='Dia do Ano',
        yaxis_title='Retorno',
        template='plotly_dark',
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=True,
            showticklabels=True,
            tickformat = '.0%'
        )
        
    )

    st.plotly_chart(fig,use_container_width=True)

    st.header('Análise da perfomance de um único ativo')

    st.write('')
    
    col1, col2 = st.columns(2)
    with col1:
        ticker = st.selectbox('Escolha o Ativo(Clique no campo e digite as iniciais do Ativo)',st.session_state.tabela_papeis['Ticker'])
    
    with col2:
        st.write('')
        st.write('')
        bt_calc = st.button('Buscar')

   
    if bt_calc:
        df = puxar_dados(ticker + '.SA','1998-01-01','2022-09-30')
        df['ano'] = df.index.year
        df['dia_do_ano'] = df.index.dayofyear

        tb = df.pivot( index='dia_do_ano', columns='ano', values='Adj Close')
        tab = tb.fillna(method='bfill')
        tab.pct_change()
        tab = ( tab/tab.iloc[0] ) - 1
    
        gerar_grafico_unid(tab,ticker)
        
