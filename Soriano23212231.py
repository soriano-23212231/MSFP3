"""
Práctica 3: Modelado y control del sistema musculoesquelético

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Judith Valeria Soriano Angeles
Número de control: 23212231
Correo institucional: l23212231@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Librerías para cálculo numérico y generación de gráficas
import sys

import numpy as np
import math as m
import matplotlib.pyplot as plt
from scipy import signal
import control as ctrl
import pandas as pd

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5 
N = round((tend-t0)/dt)+1
t = np.linspace(t0,tend,N)
u =np.zeros(N); u[round(1/dt):round(2/dt)]=1

#Funcion de transferencia (segun caso)
def casos(R):
    a = 0.25
    Cs = 10E-6
    Cp = 100E-6
    
    # Componentes del circuito RC
    num = [Cs*R,1-a]
    den = [R*(Cs+Cp),1]
    sys = ctrl.tf(num, den)
    L= np.roots(den)
    return sys,L

#Funcion de transferencia CONTROL
R= 100
sysControl,L = casos(R)
print(f"Funcion de transferencia CONTROL:{sysControl}")
print(f"Polos del sistema: L1 = {L[0]:.3e}\n")

#Funcion de transferencia CASO
R= 10E3
sysCaso,L = casos(R)
print(f"Funcion de transferencia CASO:{sysCaso}")
print(f"Polos del sistema: L1 = {L[0]:.3e}\n")


# Controlador PI
kP = 0.214494288634787
kI = 3714.60750905146
Cr = 1e-6
Re = 1/(kI*Cr)
Rr = kP*Re
numPID = [Rr*Cr,1]
denPID = [Re*Cr,0]
PID = ctrl.tf(numPID, denPID)
print(f"Funcion de transferencia CASO en lazo cerrado: {PID} \n")

#Colores
clr1 = np.array([43, 71, 137])/255; #azul
clr2 = np.array ([16, 177, 131])/ 255; #verde oscuro
clr3 = np.array([160, 203, 117])/ 255; #verde claro
clr4 = np.array([227, 109, 155])/ 255; #rosa

#Funciones del sistema en lazo abierto y lazo cerrado
_,Fsx = ctrl.forced_response(sysControl,t,u,x0) #Control
_,Fsy = ctrl.forced_response(sysCaso,t,u,x0) #Caso

sysPID=ctrl.feedback(ctrl.series(PID,sysCaso),1,sign =-1) #PI Caso
_,PI = ctrl.forced_response(sysPID,t,Fsx,x0) #PI Tratamiento


# Respuestas: Simulaciones numéricas
fg = plt.figure(1)
fg.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.plot(t,u,'-',linewidth=1.0,color=clr4,label='F(t)')
plt.plot(t,Fsx,'-',linewidth=1.0,color=clr1,label='Fs(t) Control')
plt.plot(t,Fsy,':',linewidth=1.0,color=clr2,label='Fs(t) Caso')
plt.plot(t,PI,'--',linewidth=1.5,color=clr3,label='PI(t) Tratamiento')
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.1); plt.yticks(np.arange(-0.1,1.1,0.1))
plt.xlabel('t [s]')
plt.ylabel('F(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=4,frameon=False)
plt.show()
fg.savefig('Caso_python.pdf',bbox_inches='tight')
