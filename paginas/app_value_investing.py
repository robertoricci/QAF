import math
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st
import pandas as pd
from cachetools import cached
from libs.fundamentus.lista import (
    get_df_acoes,
    get_df_setores,
    get_df_acoes_do_setor,
)
import extra_streamlit_components as stx
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime as dt, timedelta
import seaborn as sns
import numpy as np

@st.cache_data(show_spinner="Buscando dados fundamentalistas para ações.", ttl=3600)
def busca_dados_acoes():
    df = get_df_acoes()
    #iltrar empresas financeiras
    emp = get_df_acoes_do_setor(20)
    
    if emp:
        df = df[~df["Papel"].isin(emp)]
    
    df = df[df["Div.Yield"] > 0]
    
    df = df[df["Cotação"] > 0]
    df = df[df["Liq. Corr."] > 0]
    df = df[df["Liq.2meses"] > 0]
    
    st.session_state["lista_acoes"] = df
    return df

@st.cache_data(show_spinner="Buscando dados no Yahoo Finance.", ttl=3600)
def buscar_dados_yahoo(tickers, data_inicial, data_final):
    df = yf.download(tickers, data_inicial, data_final)["Adj Close"]
    ##return df["Adj Close"]
    return df


@st.cache_data(show_spinner="Buscando dados no Carteira Global.", ttl=3600)
def buscar_dados_carteira_global(tickers, data_inicial, data_final):
    from dados.carteira_global import CarteiraGlobal

    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    df = cg.retonar_cotacoes_fechamento(tickers, data_inicial, data_final)
    return df



@st.cache_data(show_spinner="Buscando dados do IBOV na Carteira Global.", ttl=3600)
def buscar_dados_ibov_carteira_global(data_inicial, data_final):
    from dados.carteira_global import CarteiraGlobal

    ID_IBOV = 2
    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    df = cg.retonar_dados_indice(ID_IBOV, data_inicial, data_final)
    df.rename(columns={"Close": "IBOV"}, inplace=True)
    return df


def busca_df_acoes_do_cache():
    if "lista_acoes" not in st.session_state:
        df = busca_dados_acoes()
        st.session_state["lista_acoes"] = df
    else:
        df = st.session_state["lista_acoes"]
    return df


def is_dados_carregados():
    return "lista_fiis" in st.session_state and "lista_acoes" in st.session_state


def mostrar_tab_estatisticas(df_tela):
    st.write("#### Estatísticas")
    df_stats = pd.DataFrame()
    df_stats["Menor valor"] = df_tela.min(numeric_only=True)
    df_stats["Valor médio"] = df_tela.mean(numeric_only=True)
    df_stats["Desvio padrão"] = df_tela.std(numeric_only=True)
    df_stats["Maior valor"] = df_tela.max(numeric_only=True)

    st.write(df_stats)


def mostrar_tab_graficos(df, titulo, graficos, numero_colunas, numero_linhas):
    fig = make_subplots(
        rows=numero_linhas, cols=numero_colunas, subplot_titles=graficos
    )

    col_atual = 1
    row_atual = 1

    for g in graficos:
        fig.add_trace(
            go.Bar(x=df.index, y=df[g], name=g),
            row=row_atual,
            col=col_atual,
        )
        fig.add_hline(
            y=df[g].mean(),
            line_dash="dot",
            annotation_text="Média",
            annotation_position="bottom right",
            row=row_atual,
            col=col_atual,
        )

        if col_atual == numero_colunas:
            row_atual += 1
            col_atual = 1
        else:
            col_atual += 1

    fig.update_layout(
        height=800,
        width=1200,
        title_text=titulo,
    )

    st.plotly_chart(fig)


def mostrar_tab_magic_formula_acoes(
    df,dt_ini,dt_fim
):
    manter = ["ROIC", "EV/EBIT","Div.Yield"]
    remover = [col for col in df.columns if col not in manter]
    df = df.drop(remover, axis=1)

    df["EV/EBIT"] = df["EV/EBIT"].astype(float)
    df = df[df["EV/EBIT"] > 0]
    df = df.sort_values(by="EV/EBIT", ascending=True)
    df["Ranking EV/EBIT"] = range(1, len(df) + 1)

    df["ROIC"] = df["ROIC"].astype(float)
    df = df[df["ROIC"] > 0]
    df = df.sort_values(by="ROIC", ascending=False)
    df["Ranking ROIC"] = range(1, len(df) + 1)

    df["Magic Formula"] = df["Ranking EV/EBIT"] + df["Ranking ROIC"]
    df["Ranking Magic Formula"] = range(1, len(df) + 1)
    
    df = df.sort_values("Ranking Magic Formula", ascending=True)
    
    col1, col2 = st.columns([6,6])
    with col1:
         st.write("")
         col1.image("imagens/livro-formula-magica.jpeg", width=250)
    with col2:
        st.write("")
        st.write("")
        st.write("")
    st.write("")
    st.write("")
    st.write("")
    col1,col2 = st.columns([11,1])
    # with col1:
    #     st.write("")
    #     st.write("")
    #     st.write("")
    #     st.write("")
    #     st.write("")
    #     col1.image("imagens/livro-formula-magica.jpeg", width=250)
    with col1:
        
        st.markdown(
        "**Filtros aplicados:** Dividend Yield > 0; Cotação > 0; Liq. Corr. > 0; Liq.2meses > 0")
        
        st.markdown(
        "**Cotações dos ultimos 3 anos:**")
        
        st.write(df.head(10))
        
        st.write("#### " + str(df.count().unique()[0]) + " registros retornados")

        acoes = [i + ".SA" for i in df.head(10).index]

        if len(acoes) <= 10:
            
            pd.options.plotting.backend = "plotly"
            
            df_fechamento = buscar_dados_yahoo(acoes,"2021-01-01", "2023-12-30")
            
            ##df_fechamento = df_fechamento.pct_change().dropna()
            
            df_fechamento['Carteira'] = df_fechamento.sum(axis = 1)
            ##df_fechamento['Carteira_anual'] =  df_fechamento['Carteira'].cumsum()
            
            ###df_ibov = buscar_dados_ibov_carteira_global("2021-01-01", "2023-12-31")
            
            df_ibov = buscar_dados_yahoo('^BVSP',"2021-01-01", "2023-12-30")
            ##df_ibov.rename(columns={'Adj Close': 'IBOV'}, inplace = True)
            
            ##df_ibov = df_ibov.pct_change().dropna().cumsum()
            
            df_fechamento = pd.merge(df_ibov, df_fechamento, how = 'inner', on = 'Date')
            df_fechamento.rename(columns={'Adj Close': 'IBOV'}, inplace = True)
            
         
            varIbov =  ((df_fechamento["IBOV"].tail(1).values[0]-df_fechamento["IBOV"].head(1).values[0] ) / df_fechamento["IBOV"].head(1).values[0] ) * 100
            
            varCart =  ((df_fechamento["Carteira"].tail(1).values[0]-df_fechamento["Carteira"].head(1).values[0] )/ df_fechamento["Carteira"].head(1).values[0] ) * 100
            
            varCart = str( round(varCart,3)) + '%'
            
            varIbov = str( round(varIbov,3)) + '%'
            
            st.markdown("**Retorno Magic Formula X IBOV** Nos do ultimos 3 anos")
            
            col1, col2,col3, col4 = st.columns([3,3,3,3])
            
            with col1:
                st.metric('Carteira', df_fechamento["Carteira"].tail(1), delta=varCart)
            with col2:
                st.metric('IBOV', df_fechamento["IBOV"].tail(1), delta=varIbov)

            df_fechamento = df_fechamento[['Carteira','IBOV']]
            
            df_fechamento = df_fechamento / df_fechamento.iloc[1]
            
            st.markdown("**Grafico**:")
           
            fig = df_fechamento.plot()
            
            fig.update_traces(line_width=5, selector=dict(name="IBOV"))
            fig.update_layout(legend_title_text="Tickers")
            
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("O gráfico só é gerado para 10 ativos ou menos.")
            
        
        acoes = list(df.head(10).index)
        todas = list(df.index)
        

        col1, col2 = st.columns([10,2])
        
        
        with st.form(key='form2'):
            
            st.markdown("**Parametrização de carteira personalizada**")
            
            #with st.expander("Entenda Hierarchical risk parity, clique para saber mais"):
       
            ativos = st.multiselect("Ticker", todas , acoes)
            valor = st.number_input(label='INFORME O VALOR DE INVESTIMENTO NO PORTIFÓLIO')
            import datetime
            
            # ##dt.today().strftime("%Y-%m-%d")
            # ano = int(dt.today().strftime("%Y"))
            # mes = int(dt.today().strftime("%m"))
            # dia = int(dt.today().strftime("%d"))
            

            # dt_ini_por = st.date_input("Data inicio", datetime.date(2021, 1, 1))
            # dt_fim_por = st.date_input("Data fim", datetime.date(ano, mes, dia))
            # st.write('Periodo de is:',dt_ini_por,' ate is:',dt_fim_por)
            
            ##dt_ini = st.number_input(label='data_ini')
            otimizacao = st.form_submit_button('Otimização')
        st.markdown('---')
        
        if otimizacao and len(ativos) > 0:
            
            with st.spinner('Excutando a personalização...'):
                ativos = [ticker + '.SA' for ticker in ativos] 
                
                dt_ini_por = "2021-01-01"
                dt_fim_por = "2023-12-30"
                # BACKTEST
                ###acoes = baixar_cotacoes_acoes(ativos)
                acoes = buscar_dados_yahoo(ativos,dt_ini_por, dt_fim_por)
                
                ##qtd_acoes = acoes.copy()
                
                pesos_iguais = calcular_pesos(acoes,dt_ini_por,dt_fim_por)
                
                dividendo = calcular_dividendos(acoes,valor)
                
                retorno_da_carteira =  ((pesos_iguais["retorno"].tail(1).values[0]-pesos_iguais["retorno"].head(1).values[0] ) / pesos_iguais["retorno"].head(1).values[0] ) * 100

                pesos_iguais = pesos_iguais / pesos_iguais.iloc[0]
            
            
            valor_final = valor + (valor * (retorno_da_carteira/100))
            vol_ano = 100
            
            dy_portifolio = dividendo / valor
            
  
            st.markdown("**Grafico**")
           
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=pesos_iguais.index, y=pesos_iguais.IBOV,
                     mode='lines', name='IBOV'))
            # fig.add_trace(go.Scatter(x=simulacao.index,  y=simulacao.retorno_anual,
            #          mode='lines',name='CARTEIRA ORIGINAL'))
            fig.add_trace(go.Scatter(x=pesos_iguais.index, y=pesos_iguais.retorno,
                     mode='lines',name='CARTEIRA PERSONALIZADA'))
            
            
            st.plotly_chart(fig, theme=None, use_container_width=True)

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric(label='VALOR FINAL', value=f'R$ {round((valor_final), 2):,.2f}')
            with col2:
                st.metric(label='RETORNO DO PORTIFÓLIO', value=f'{round(retorno_da_carteira,2)}%')
            with col3:
                st.metric(label='DY DO PORTIFÓLIO', value=f'{round((dy_portifolio * 100),2)}%')
            with col4:
                st.metric(label='DIVIDENDOS RECEBIDOS', value=f'R$ {round((dividendo), 2):,.2f}')
            with col5:
                st.metric(label='VOLATILIDADE', value=f'{vol_ano}')
                ##st.metric(label='VOLATILIDADE', value=f'{round((vol_ano[0][0]),2)}')
                
                
def calcular_dividendos(acoes,valor):
    
    qtd_acoes = acoes.dropna()
    
    primeiro_dia = qtd_acoes.index.min().strftime('%Y-%m-%d')
    #print(primeiro_dia)
    qtd_acoes = qtd_acoes[qtd_acoes.index == primeiro_dia]
    
    ativos  = list(acoes.columns)
    
    for tick in ativos:
        qtd_acoes[tick] = round( ( (1/len(ativos) * valor) / ( qtd_acoes[tick])))
        
    dividendos_recebidos = 0
    for tick in ativos:
        try:
            dividendos_recebidos += (yf.Ticker(tick).history(start=primeiro_dia)['Dividends'].sum() * qtd_acoes[tick][0])
        except:
            print('erro')
        continue
              
    
    return dividendos_recebidos
  
def  calcular_pesos(acoes,dt_ini,dt_fim):
    
    pesos_iguais = acoes.copy()
    
    ativos = list(pesos_iguais.columns)
    
    for tick in ativos:
        pesos_iguais[tick] = pesos_iguais[tick] * (1/len(ativos))
    pesos_iguais['retorno'] = pesos_iguais.sum(axis=1)
    pesos_iguais['retorno_anual'] = pesos_iguais['retorno'].cumsum()
    
    
    ibov = buscar_dados_yahoo('^BVSP',dt_ini, dt_fim)
    
    pesos_iguais = pd.merge(ibov, pesos_iguais, how = 'inner', on = 'Date')
    pesos_iguais.rename(columns={'Adj Close': 'IBOV'}, inplace = True)
    
    return pesos_iguais
                 
      
 
def quantidade_de_acoes_para_comprar(ativos, valor, pesos):
    
    acoes = yf.download(ativos, period='1y')['Close']
    
    acoes.fillna(method='ffill',inplace=True)
    
    acoes = acoes.iloc[-1]
   
    for tick in ativos:
        acoes[tick] = ((pesos[tick] * valor)/ (acoes[tick]) )
    return acoes



def mostrar_filtros_acoes(filtros):
    
    df_acoes = busca_df_acoes_do_cache().copy()
    col1, _, col2, _, col3, _ = st.columns([6, 1, 4, 1, 4, 1])

    with col1:
        setores_possiveis_ordenados = sorted(
            get_df_setores()["Setor"], key=lambda x: int(x.split(" - ")[0])
        )
        
        codigo_nome = pd.read_excel('data/classification_b3.xlsx')
        ##nome_do_ativo = st.selectbox('Escolha a ação que deseja analisar', (codigo_nome['Código']) )
        
        # setores_possiveis = ["Todos"] + list(setores_possiveis_ordenados)

        filtros["setores"] = st.multiselect(
            "Setor(es):", codigo_nome, []
        )

        menor_cotacao = float(df_acoes["Cotação"].min(numeric_only=True))
        maior_cotacao = float(df_acoes["Cotação"].max(numeric_only=True))

        filtros["cotacao"] = st.slider(
            "Cotação",
            menor_cotacao,
            maior_cotacao,
            (menor_cotacao, maior_cotacao),
            step=1.0,
            format="R$ %.2f",
        )

        menor_liquidez = float(df_acoes["Liq. Corr."].min(numeric_only=True))
        maior_liquidez = float(df_acoes["Liq. Corr."].max(numeric_only=True))

        filtros["Liq. Corr."] = st.slider(
            "Liquidez Corrente",
            menor_liquidez,
            maior_liquidez,
            (menor_liquidez, maior_liquidez),
            step=1.0,
            format="%.2f",
        )

    with col2:
        pass

    with col3:
        pass



def filtrar_df_acoes(filtros,filtrar_ticker = False):
    
    df_tela = busca_df_acoes_do_cache().copy()


    #excluir ticker da mesma empresa
    if filtrar_ticker:
        df_tela['Ticker'] = df_tela.apply(lambda row : row['Papel'][:4], axis=1)
        df_aux = df_tela[['Ticker', 'Liq.2meses']]  # novo dataframe com 2 colunas apenas
        indexes = df_aux['Liq.2meses'].index.to_series().groupby(df_aux['Ticker']).max().to_list()  # pegando os índices onde o ticker (símbolo) possui maior líquidez
        df_tela =  df_tela[df_tela.index.isin(indexes)] 
    
    df_tela.set_index("Papel", drop=True, inplace=True)
    df_tela["ROE"] = df_tela["ROE"] * 100.0
    df_tela["ROIC"] = df_tela["ROIC"] * 100.0
    df_tela["Div.Yield"] = df_tela["Div.Yield"] * 100.0
    df_tela["Cresc. Rec.5a"] = df_tela["Cresc. Rec.5a"] * 100.0
    df_tela["Mrg Ebit"] = df_tela["Mrg Ebit"] * 100.0
    df_tela["Mrg. Líq."] = df_tela["Mrg. Líq."] * 100.0

    return df_tela


def main():
    st.title(":star: Value Investing")
    mensagens = st.container()
    
    filtros ={'setores':''}
    
    df_acoes_tela = filtrar_df_acoes(filtros,True)
    
    mostrar_tab_magic_formula_acoes(df_acoes_tela,"2021-01-01", "2023-12-07")
    
