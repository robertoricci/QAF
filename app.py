import streamlit as st
import style as style
import app_home
import app_carteira
import app_bolsa_eleicoes
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
    page_icon= './images/QAF.png',  # String, anything supported by st.image, or None.
)


#carrega os arquivos css
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    
def main(): 
    pages={
         "Home":page_home,
          "Eleições":page_bolsa_eleicoes
    }
    
        #esconder botão de menu e marca dágua no rodapé
    style.hidden_menu_and_footer()
        #cabeçalho detalhe superior da página 
    style.headerstyle()
           
    with st.sidebar:
            style.sidebarwidth() 
            page = option_menu('Menu', ["Home","Eleições"],
                                icons=['house','cash-coin'],
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
        st.write('Feito com Carinho')
        st.write('Roberto Carlos Ricci')
        st.write('pbisolucoes@gmail.com')
        st.write('https://bit.ly/lirobertocarlosricci')
       
if 'portifolio' not in st.session_state:
        st.session_state.portifolio = pd.DataFrame()
        st.session_state.portifolio['Ação'] = ''
    
def page_home():
     app_home.home()

def page_carteira():
     app_carteira.carteira()


def page_bolsa_eleicoes():
     st.session_state.tabela_papeis = puxar_tabela_papeis()
     app_bolsa_eleicoes.bolsa()
 
  
    
@st.cache
def puxar_tabela_papeis():
    return pd.read_csv('tickers.csv')


  
if __name__ == "__main__":
   main()