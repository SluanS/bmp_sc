import streamlit as st
from index import baterMapa
import datetime as dt

col1, col2, col3 = st.columns([1,2,3])
result = None
with col1:
    # st.header("Bate Mapa")
    dia = st.selectbox("Escolha o dia", 
                         ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "sexta-feira", "Sabado", "Domingo"],
                         )


with col2:
    dadosNeoh = st.file_uploader("Planilha NEOH", type="xlsx", help="Yo dog! Aqui só a planilha que acabou de ser gerada a partir do neoh")
    dadosHorario = st.file_uploader("Planilha Horário")
    
    if st.button("Bater mapa",disabled= True if dadosNeoh == None or dadosHorario ==None else False):
        result = baterMapa(dia,dadosHorario,dadosNeoh)

with col3:
    st.markdown(":green[Novos avisos]")
    with st.container(border=True):
        if (result != None):
            for a in result.new:
                st.write(a)
        else:
            st.empty()
    st.markdown(":orange[Reagendados]")
    with st.container(border=True):
        if (result != None):
            for t in result.transfered:
                st.write(a)
        else:
            st.empty()
    st.write("Novo horário")
    with st.container(border=True):
        if result != None:
            for k, v in result.newTime.items():
                with st.container(border=True):
                    oldTime = dt.datetime.strftime(v[0], "%H:%M")
                    newTime = dt.datetime.strftime(v[1], "%H:%M")
                    st.markdown(f":red[{k}] :")
                    st. write(f"{oldTime} -> {newTime}")
        else:
            st.empty()
    st.write("Autorizado")
    with st.container(border=True):
        if result != None:
            for k,v in result.situationUpdate.items():
                with st.container(border=True):
                    st.write(k)
                    st.markdown(f":red[{v[0]}] -> :green[{v[1]}]")