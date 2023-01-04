# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 20:55:16 2022

@author: marvelez
"""

def spt_rule(tiempos, rutas):
    
    # Inicializar Variable
    n = len(tiempos)                     # Número de trabajos
    m = max([len(i) for i in rutas])     # Número de máquinas
    TrabajoLibre = [0 for j in range(n)] # Tiempo en el que se libera cada trabajo
    MaquinaLibre = [0 for j in range(m)] # Tiempos en los que se libera cada máquina
    q = [0 for i in range(n)]            # Contador de operaciones programadas de cada trabajo
    SinTerminar = [i for i in range(n)]  # Trabajos sin terminar
    Gantt = []                           # Detalle del programa de producción
    Inicio_Fin = [[None for i in range(m)] for j in range(n)]
    
    t = 0
    while len(SinTerminar)>0:
    
        # Actualizar A(t): Máquinas disponibles en el instante t
        A = [maq for maq in range(m) if MaquinaLibre[maq]<=t]

        # Actualizar Um(t): Trabajos disponibles para programarse en la máquina m en el instante t
        U = [[j for j in SinTerminar if TrabajoLibre[j]<=t and rutas[j][q[j]]==m] for m in A]

        # Seleccionar el trabajo a programar en cada máquina en A
        for posicion, opciones in enumerate(U):
            if len(opciones)>0:
                if len(opciones)==1:
                    jj=opciones[0]    # jj --> índice del trabajo a programar
                else:
                    tiempos_proceso = [tiempos[trabajo][q[trabajo]] for trabajo in opciones]
                    jj = opciones[tiempos_proceso.index(min(tiempos_proceso))]  # jj --> índice del trabajo a programar (regla SPT)
    
                # Actualizar variables
                TrabajoLibre[jj] = t + tiempos[jj][q[jj]]
                MaquinaLibre[A[posicion]] = TrabajoLibre[jj]
                Gantt.append({'trabajo':jj, 'operacion':q[jj], 'inicio':t, 'fin':TrabajoLibre[jj]})
                Inicio_Fin[jj][q[jj]] = (t,TrabajoLibre[jj])
                q[jj]+=1
                if q[jj] == len(rutas[jj]):
                    SinTerminar.remove(jj)
                    if len(SinTerminar)==0:
                        return max(TrabajoLibre), Inicio_Fin
    
        # Actualizar t
        t = min([tiempo for tiempo in MaquinaLibre if tiempo>t])

def mwkr_rule(tiempos, rutas):
    # Inicializar Variable
    n = len(tiempos)                     # Número de trabajos
    m = max([len(i) for i in rutas])     # Número de máquinas
    TrabajoLibre = [0 for j in range(n)] # Tiempo en el que se libera cada trabajo
    MaquinaLibre = [0 for j in range(m)] # Tiempos en los que se libera cada máquina
    q = [0 for i in range(n)]            # Contador de operaciones programadas de cada trabajo
    SinTerminar = [i for i in range(n)]  # Trabajos sin terminar
    Gantt = []                           # Detalle del programa de producción
    mwkr = [sum(t) for t in tiempos]
    Inicio_Fin = [[None for i in range(m)] for j in range(n)]
    
    t = 0
    while len(SinTerminar)>0:
        
        # Actualizar A(t): Máquinas disponibles en el instante t
        A = [maq for maq in range(m) if MaquinaLibre[maq]<=t]
    
        # Actualizar Um(t): Trabajos disponibles para programarse en la máquina m en el instante t
        U = [[j for j in SinTerminar if TrabajoLibre[j]<=t and rutas[j][q[j]]==m] for m in A]
    
        # Seleccionar el trabajo a programar en cada máquina en A
        for posicion, opciones in enumerate(U):
            if len(opciones)>0:
                if len(opciones)==1:
                    jj=opciones[0]    # jj --> índice del trabajo a programar
                else:
                    work_remaining = [mwkr[trabajo] for trabajo in opciones]
                    jj = opciones[work_remaining.index(max(work_remaining))]  # jj --> índice del trabajo a programar (regla MWKR)
                # Actualizar variables
                TrabajoLibre[jj] = t + tiempos[jj][q[jj]]
                MaquinaLibre[A[posicion]] = TrabajoLibre[jj]
                mwkr[jj]-=tiempos[jj][q[jj]]
                Gantt.append({'trabajo':jj, 'operacion':q[jj], 'inicio':t, 'fin':TrabajoLibre[jj]})
                Inicio_Fin[jj][q[jj]] = (t,TrabajoLibre[jj])
                q[jj]+=1
                if q[jj]== len(rutas[jj]):
                    SinTerminar.remove(jj)
                    if len(SinTerminar)==0:
                        return max(TrabajoLibre), Inicio_Fin
        
        # Actualizar t
        t = min([tiempo for tiempo in MaquinaLibre if tiempo>t])