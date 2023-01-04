# -*- coding: utf-8 -*-
"""
@author: Mario C. Vélez -- marvelez@eafit.edu.co

la tabla y el gráfico no se actualizan cuando se cambian los archivos de datos de entrada...
"""

import streamlit as st
import reglas
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title='Programación en sistemas Job-Shop', layout='centered')
ocultar_menu ='''
    <style>
    #MainMenu {visibility: hidden; }
    footer {visibility: hidden; }
    <\style>'''
st.markdown(ocultar_menu, unsafe_allow_html=True)

def imprime_programa(prog):
    separador = (10+18*len(prog[0]))*'='+ '\n'
    tabla = separador
    n_espacios = '{:^10}' + len(prog[0])*'{:<18}'+'\n'
    el_texto = ['Trabajo']+['Operación '+str(i+1) for i in range(1+len(prog[0]))]
    tabla += n_espacios.format(*el_texto)
    tabla += separador
    
    for i in range(len(prog)):
        x = ['j'+str(i+1)]+prog[i]
        tabla += '' + n_espacios.format(*[str(k) for k in x])
    tabla += separador
    
    st.subheader('Valores de inicio y fin de cada operación de cada trabajo:')
    st.text(tabla)

def imprime_gantt(rutas, prog):
    datos = dict(
        trabajo = ['j'+str(job+1) for job,fila in enumerate(prog) for op,k in enumerate(fila)],
        operacion = ['op'+str(op+1) for job,fila in enumerate(prog) for op,k in enumerate(fila)],
        inicio = [op[0] for fila in prog for op in fila],
        duracion = [op[1]-op[0] for fila in prog for op in fila],
        fin = [op[1] for fila in prog for op in fila],
        recurso = ['Máquina 0'+str(r+1) if r<9 else 'Máquina '+str(r+1) for fila in rutas for r in fila])
    
    hovertemp="<br>".join([
        "<b>Trabajo:</b> %{customdata[0]}",
        "<b>Operación:</b> %{customdata[1]}",
        "<b>Inicio:</b> %{base}",
        "<b>Fin:</b> %{x}<extra></extra>", # <extra></extra> elimina nombre del 'trace' (hover mode)
        ])
    
    fig = px.bar(data_frame=datos,
        base='inicio',
        x='duracion',
        y='recurso',
        color='trabajo',
        custom_data=['trabajo', 'operacion'],
        orientation = 'h',
        hover_name='trabajo',
        #hover_data = {'inicio':True, 'duracion':True, 'color':False},
        range_y=(0, 3))
    fig.update_yaxes(title='', autorange="reversed", categoryorder='category ascending')
    fig.update_xaxes(title='Tiempo')
    fig.update_traces(hovertemplate=hovertemp)
    #fig.update_layout(hovermode='x')

    return(fig)

variables = ['tiempos', 'rutas', 'solucion_spt', 'solucion_mwkr', 'Cmax_spt', 'Cmax_mwkr']
for var in variables:
    if var not in st.session_state:
        st.session_state[var] = None

st.title("Programación de Producción en Sistemas Job-Shop")

archivo_tiempos = st.file_uploader('Cargar archivo de tiempos de proceso', type='txt')
archivo_rutas = st.file_uploader('Cargar archivo de rutas', type = 'txt')

if archivo_tiempos:
    if st.session_state.tiempos == None:
        st.session_state.tiempos = [[float(i) for i in linea.decode('utf-8').split()] for linea in archivo_tiempos]

if archivo_rutas:
    if st.session_state.rutas == None:
        st.session_state.rutas = [[int(i)-1 for i in linea.decode('utf-8').split()] for linea in archivo_rutas]

if st.session_state.tiempos and st.session_state.rutas:

    if st.session_state.solucion_spt == None:
        st.session_state.Cmax_spt, st.session_state.solucion_spt = reglas.spt_rule(st.session_state.tiempos, st.session_state.rutas)
    
    if st.session_state.solucion_mwkr == None:
        st.session_state.Cmax_mwkr, st.session_state.solucion_mwkr = reglas.mwkr_rule(st.session_state.tiempos, st.session_state.rutas)
    
    regla = st.radio('Seleccione la regla de despacho a utilizar', ('SPT', 'MWKR'))
    
    if regla == 'SPT':
        imprime_programa(st.session_state.solucion_spt)
        st.subheader('Makespan = '+str(st.session_state.Cmax_spt))
        diagrama_gantt = st.container()
        with diagrama_gantt:
            gantt = imprime_gantt(st.session_state.rutas, st.session_state.solucion_spt)
            st.write(gantt)
    
    if regla == 'MWKR':
        imprime_programa(st.session_state.solucion_mwkr)
        st.subheader('Makespan = '+str(st.session_state.Cmax_mwkr))
        diagrama_gantt = st.container()
        with diagrama_gantt:
            gantt = imprime_gantt(st.session_state.rutas, st.session_state.solucion_mwkr)
            st.write(gantt)
        
