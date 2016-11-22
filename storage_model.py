import pylab as pl
import pandas as pd

import casadi as ca


# Constants



cp_water = 4182.0


# States

x = ca.MX.sym("x", 4)

TSH0 = x[0]
TSH2  = x[1]
TSH3  = x[2]
TSH1  = x[3]

# Parameters

# p = ca.MX.sym("p", 1)

# pinit = ca.vertcat([u_radiator_init])


# Controls

u = ca.MX.sym("u", 8)

PSOS = u[0]
PC_1 = u[1]
m0minus = u[2]
m0plus = u[3]
m2minus = u[4]
m2plus = u[5]
m3minus = u[6]
m3plus = u[7]


# Massflows storage

#first Layer
dotT0 = 1/m0 * (PSOS * TSOS - PC_1 * TSH0 - (m0plus + PSOS - PC_1) * TSH0 + m0plus * TSH2) 
#m0minus = m0plus + PSOS - PC_1 

#second Layer
dotT2 = 1/m2 * (-PSOS*VSHP_OP * TSH2 + PC_1*VSHS_OP  * TCO_1 + (m0plus + PSOS - PC_1) * TSH0 - m0plus * TSH2  \
    - (-PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP +m2plus) * TSH2 + m2plus * TSH3)
#m2minus = -PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP +m2plus

#third Layer
dotT3 = 1/m3 * ((-PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP +m2plus) * TSH2 - m2plus * TSH3 \
    - (-PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP  +m3plus) * TSH1 + m3plus * TSH1)
#m3minus = -PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP  +m3plus

#fourth Layer
dotT1 = 1/m1(-PSOS*VSHP_CL * TSH1 + (-PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP  +m3plus) * TSH3 - m3plus * TSH1 + PC_1*VSHS_CL * TCO_1)



dxdt = ca.vertcat( \
    dotT0, \
    dotT2, \
    dotT3, \
    dotT1)