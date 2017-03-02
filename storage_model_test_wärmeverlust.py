import pylab as pl
import pandas as pd

# import sys # for home
# sys.path.append(r"C:\Users\alexa\Documents\Master\Python programme\casadi-py27-np1.9.1-v2.4.3")
# sys.path.append(r"C:\Users\alexa\Documents\Master\Python programme\casiopeia")

import casadi as ca
import casiopeia as cp
import matplotlib.pyplot as plt

#############################
datatable = "data2017-02-23"
#############################


# Constants

cp_water = 4182.0
layer = 4
Tamb = 20.0
alpha_0 = 1.90944#1.79339
alpha_2 = 1.24485#1.7431
alpha_3 = 1.42851#1.56512
alpha_1 = 6.44813#16.8649

# States

x = ca.MX.sym("x", 4)

TSH0 = x[0]
TSH2  = x[1]
TSH3  = x[2]
TSH1  = x[3]

# Parameters

p = ca.MX.sym("p", 1)
alpha_iso = p[0]

# pinit = ca.vertcat([u_radiator_init]) # from pe_step3


# Controls

u = ca.MX.sym("u", 14)

V_PSOS = u[0]
msto = u[1] 
m0minus = u[2]
m0plus = u[3]
m2minus = u[4]
m2plus = u[5]
m3minus = u[6]
m3plus = u[7]
TSOS = u[8]
TCO_1 = u[9]
VSHP_OP = u[10]
VSHP_CL = u[11]
VSHS_OP = u[12]
VSHS_CL = u[13]



m = 2000.0 / layer

# Massflows storage

# ## without VSHS_CL/OP and VSHP_CL/OP
# #first Layer
# dotT0 = 1.0/m * (V_PSOS * TSOS - msto * TSH0 - (m0plus + V_PSOS - msto) * TSH0 + m0plus * TSH2) + alpha_iso
# #m0minus = m0plus + V_PSOS - msto 

# #second Layer
# dotT2 = 1.0/m * ( -V_PSOS * TSH2 + msto * TCO_1 + (m0plus + V_PSOS - msto) * TSH0 - m0plus * TSH2  \
#     - (-V_PSOS + V_PSOS - msto + msto + m2plus) * TSH2 + m2plus * TSH3)
# #m2minus = -V_PSOS +V_PSOS -msto +msto +m2plus

# #third Layer
# dotT3 = 1.0/m * ((-V_PSOS + V_PSOS - msto + msto + m2plus) * TSH2 - m2plus * TSH3 \
#     - (-V_PSOS + V_PSOS - msto + msto  + m3plus) * TSH3 + m3plus * TSH1)
# #m3minus = -V_PSOS +V_PSOS -msto +msto  +m3plus

# #fourth Layer
# dotT1 = 1.0/m * (-V_PSOS * TSH1 + (-V_PSOS + V_PSOS - msto + msto  + m3plus) * TSH3 - m3plus * TSH1 + msto * TCO_1)

#=================================================================================================================================================
## with VSHS_CL/OP and VSHP_CL/OP
#first Layer
dotT0 = 1.0/m * (V_PSOS * TSOS - msto * TSH0 - (m0plus + V_PSOS - msto) * TSH0 + m0plus * TSH2 - (alpha_0 * (TSH0 - Tamb)) / cp_water)  + alpha_iso
#m0minus = m0plus + V_PSOS - msto 

#second Layer
dotT2 = 1.0/m * ( -V_PSOS * VSHP_OP * TSH2 + msto * VSHS_OP * TCO_1 + (m0plus + V_PSOS - msto) * TSH0 - m0plus * TSH2  \
    - (-V_PSOS * VSHP_OP + V_PSOS - msto + msto * VSHS_OP + m2plus) * TSH2 + m2plus * TSH3 - (alpha_2 * (TSH2 - Tamb)) / cp_water)
#m2minus = -V_PSOS*VSHP_OP +V_PSOS -msto +msto*VSHS_OP +m2plus

#third Layer
dotT3 = 1.0/m * ((-V_PSOS * VSHP_OP + V_PSOS - msto + msto*VSHS_OP + m2plus) * TSH2 - m2plus * TSH3 \
    - (-V_PSOS * VSHP_OP + V_PSOS - msto + msto * VSHS_OP  + m3plus) * TSH3 + m3plus * TSH1 - (alpha_3 * (TSH3 - Tamb)) / cp_water)
#m3minus = -V_PSOS*VSHP_OP +V_PSOS -msto +msto*VSHS_OP  +m3plus

#fourth Layer
dotT1 = 1.0/m * (-V_PSOS * VSHP_CL * TSH1 + (-V_PSOS * VSHP_OP + V_PSOS - msto + msto * VSHS_OP  + m3plus) * TSH3 \
    - m3plus * TSH1 + msto * VSHS_CL * TCO_1 - (alpha_1 * (TSH1 - Tamb)) / cp_water)
#=================================================================================================================================================


#ODE

f = ca.vertcat([ \
    dotT0, \
    dotT2, \
    dotT3, \
    dotT1])

phi = x

system = cp.system.System(x = x, u = u, f = f, phi = phi, p = p)


# Start heating

int_start = 0
# int_end = [1000]
# int_step = 1


#20161015 "Intervalle/20160303_Intervall7.csv"
data = pd.read_table("data-ausgewertet/"+ datatable + ".csv", \
    delimiter=",", index_col=0)

# for k,e in enumerate(int_start):

    # time_points = pl.linspace(0, int_end[k] - e - 1, int_end[k] - e) * 13 #*13 for seconds

time_points = data["time"].values[int_start:]

udata_0 = data["V_PSOS"][:-1].values[int_start:]

udata_1 = data["msto"][:-1].values[int_start:]

udata_2 = data["m0minus"][:-1].values[int_start:]

udata_3 = data["m0plus"][:-1].values[int_start:]

udata_4 = data["m2minus"][:-1].values[int_start:]

udata_5 = data["m2plus"][:-1].values[int_start:]

udata_6 = data["m3minus"][:-1].values[int_start:]

udata_7 = data["m3plus"][:-1].values[int_start:]

udata_8 = data["TSOS"][:-1].values[int_start:]

udata_9 = data["TCO_1"][:-1].values[int_start:]

udata_10 = data["VSHP_OP"][:-1].values[int_start:]

udata_11 = data["VSHP_CL"][:-1].values[int_start:]

udata_12 = data["VSHS_OP"][:-1].values[int_start:]

udata_13 = data["VSHS_CL"][:-1].values[int_start:]

udata = ca.horzcat([udata_0, udata_1, udata_2, udata_3, udata_4, udata_5, udata_6, udata_7, udata_8, udata_9, \
    udata_10, udata_11, udata_12, udata_13])



x0_init = data["TSH0"].values[int_start]
x1_init = data["TSH2"].values[int_start]
x2_init = data["TSH3"].values[int_start] 
x3_init = data["TSH1"].values[int_start] 


xinit = ca.horzcat([pl.atleast_2d(x0_init).T, pl.atleast_2d(x1_init).T, pl.atleast_2d(x2_init).T, pl.atleast_2d(x3_init).T,]) 

#     # wv = pl.ones(ydata.shape[0])
#     # wv[:int(ydata.shape[0]*0.1)] = 5

#     pe_setups.append(cp.pe.LSq(system = system, time_points = time_points, \
#         udata = udata, \
#         #pinit = pinit, \
#         #ydata = ydata, \
#         xinit = xinit)) #, \
#         # wv = wv))


# mpe = cp.pe.MultiLSq(pe_setups)
# # # mpe.run_parameter_estimation({"linear_solver": "ma57"})
# mpe.run_parameter_estimation()

sim_est = cp.sim.Simulation(system = system, pdata = 0.0)
# sim_est = cp.sim.Simulation(system = system, pdata = mpe.estimated_parameters)
sim_est.run_system_simulation(time_points = time_points, \
    x0 = xinit[0,:], udata = udata)




pl.close("all")


# # # Plot


pl.figure(figsize= (16,10))


# pl.subplot(1, 1, 1)
pl.scatter(time_points[::500], data["TSH0"].values[int_start::500], marker = "x", label = r"meas TSH0", color = "b")
pl.scatter(time_points[::500], data["TSH2"].values[int_start::500], marker = "x", label = r"meas TSH2", color = "g")
pl.scatter(time_points[::500], data["TSH3"].values[int_start::500], marker = "x", label = r"meas TSH3", color = "r")
pl.scatter(time_points[::500], data["TSH1"].values[int_start::500], marker = "x", label = r"meas TSH1", color = "c")
pl.plot(time_points, pl.squeeze(sim_est.simulation_results[0,:]), label = r"sim TSH0", color = "b")
pl.plot(time_points, pl.squeeze(sim_est.simulation_results[1,:]), label = r"sim TSH2", color = "g")
pl.plot(time_points, pl.squeeze(sim_est.simulation_results[2,:]), label = r"sim TSH3", color = "r")
pl.plot(time_points, pl.squeeze(sim_est.simulation_results[3,:]), label = r"sim TSH1", color = "c")
pl.title("storage model")
pl.ylabel('temperature (C)')
pl.xlabel('time (s)')
pl.legend(loc = "upper left")
pl.xlim([time_points[0], 86000])



pl.savefig("/home/da/Master/Thesis/Optimal-Control-Storage/plots/" + str(datatable) + "_" \
   + "start_from_" + str(int_start) + "_" \
  #+ str(int_end)+\
   "storage.png", \
        bbox_inches='tight')


pl.show()