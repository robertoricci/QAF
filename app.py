import streamlit as st
import html_css.style as style
import paginas.app_home as app_home
import paginas.app_carteira as app_carteira
import paginas.app_bolsa_eleicoes as app_bolsa_eleicoes
import paginas.app_analise_tecnica as app_analise_tecnica
import paginas.app_analise_fundamentalista as app_analise_fundamentalista
import paginas.app_panorama_mercado as app_panorama_mercado
import paginas.app_value_investing as app_value_investing
import paginas.setores_ibov as setores_ibov
import paginas.app_carteira as app_carteira
import pandas as pd

import matplotlib
matplotlib.use('Agg')

from streamlit_option_menu import option_menu

import warnings
warnings.filterwarnings('ignore')
 
import datetime as dt 
dia = dt.datetime.today().strftime(format='20%y-%m-%d')


st.set_page_config(  # Alternate names: setup_page, page, layout
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    page_title="QAF",  # String or None. Strings get appended with "• Streamlit". 
    page_icon= 'QAF.png',  # String, anything supported by st.image, or None.
)


###https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

#carrega os arquivos css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    
def main():
     
    pages={
         "Home":page_home,
          "Mercado":page_panorama,
          "Eleições":page_bolsa_eleicoes,
          "Análise técnica":page_analise_tecnica,
          "Análise Fundamentalista":page_analise_fundamentalista,
          "Value Investing":page_value_investing,
           "Setores Ibovespa":page_setores_ibov,
           "Carteira":page_carteira,
    }
    
        #esconder botão de menu e marca dágua no rodapé
    style.hidden_menu_and_footer()
        #cabeçalho detalhe superior da página 
    style.headerstyle()
           
    with st.sidebar:
            style.sidebarwidth() 
            page = option_menu('Menu', ["Home","Mercado","Carteira","Análise técnica","Análise Fundamentalista","Value Investing","Eleições","Setores Ibovespa"],
                                icons=['house','bar-chart','bullseye','cash-coin','cash','alarm'],
                                default_index=0, menu_icon="app-indicator",   #orientation='horizontal',
                                styles={
                "container": {"padding": "2!important", "background-color": "#ffffff","margin": "0px" }, # ,"background-size": "cover","margin": "0px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"}, #,"position": "relative","display": "inline"},
                "nav-link-selected": {"background-color": "#4a7198"},
                }) 
            
    pages[page]()
    
    with st.sidebar.expander('Sobre'):
        # Mostrar versões das bibliotecas
        #st.write(os.popen(f'python --version').read())
        #st.write('Streamlit:', st.__version__)
        #st.write('Pandas:', pd.__version__)
        #st.write('yfinance:', yf.__version__)
        #st.write('plotly:', plotly.__version__)
        #st.write('Fundamentus:', fundamentus.__version__)
        st.write('Feito com Carinho ')
        st.markdown("- Roberto Carlos Ricci")
        st.markdown("- <a href='mailto:pbisolucoes@gmail.com' target='_blank'><img src='https://img.shields.io/badge/Gmail-D14836?style=flat-square&logo=gmail&logoColor=white' target='_blank'> </a> ", unsafe_allow_html=True)
        st.markdown("- [![Linkedin Badge](https://img.shields.io/badge/-%40robertoricci-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://bit.ly/lirobertocarlosricci)](https://bit.ly/lirobertocarlosricci)")
       
if 'portifolio' not in st.session_state:
        st.session_state.portifolio = pd.DataFrame()
        st.session_state.portifolio['Ação'] = ''

if 'tabela_papeis' not in st.session_state: 
    st.session_state.tabela_papeis = pd.DataFrame()    
    st.session_state.tabela_papeis = pd.read_csv('tickers.csv',sep=',')
    
def page_home():
     app_home.home()

def page_analise_tecnica():
     app_analise_tecnica.analise_tecnica_fundamentalista()
     
def page_carteira():
    app_carteira.main()   

def page_analise_fundamentalista():
    app_analise_fundamentalista.main()
    
    
def page_value_investing():
    app_value_investing.main()


def page_bolsa_eleicoes():
     st.session_state.tabela_papeis = puxar_tabela_papeis()
     app_bolsa_eleicoes.bolsa()
     
     
def page_panorama():
    app_panorama_mercado.main()
     
def page_setores_ibov():
     setores_ibov.main()

@st.cache
def puxar_tabela_papeis():
    return pd.read_csv('tickers.csv')


  
if __name__ == "__main__":
   main()