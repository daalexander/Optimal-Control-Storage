import pylab as pl
import pandas as pd

# import sys # for home
# sys.path.append(r"C:\Users\alexa\Documents\Master\Python programme\casadi-py27-np1.9.1-v2.4.3")
# sys.path.append(r"C:\Users\alexa\Documents\Master\Python programme\casiopeia")

import casadi as ca
import casiopeia as cp
import matplotlib.pyplot as plt

#############################
datatable = "data2017-03-28"
#############################
# datatable = "data2017-01-19"
# datatable = "data2017-02-22"
# datatable = "data2017-02-27"
# datatable = "data2017-02-23"
# datatable = "data2017-03-07"


# Constants

cp_water = 4182.0
layer = 10.0
Tamb = 20.0
Tfloor = 18.0
layer_surface = 0.9503 
storage_height = 2.38
storage_scope = 3.4558
floor_surface = 0.9503
storage_top_surface = 0.9503
alpha_water = 475.0
alpha_sto = 
alpha_floor = 

storage_surface = (storage_scope * (storage_height / layer) )

# alpha_0 = 1.15482 
# alpha_2 = 0.812026
# alpha_3 = 0.523315
# alpha_1 = 2.89951
# alpha_0_1 = 0.827681
# alpha_0_2 = 1.02636
# alpha_2_1 = 1.19537
# alpha_2_2 = 1.0
# alpha_3_1 = 1.0
# alpha_3_2 = 1.0



# States

x = ca.MX.sym("x", 10)

TSH0 = x[0]
TSH2  = x[1]
TSH3  = x[2]
TSH1  = x[3]
TSH0_1  = x[4]
TSH0_2  = x[5]
TSH2_1  = x[6]
TSH2_2  = x[7]
TSH3_1  = x[8]
TSH3_2  = x[9]


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

#=================================================================================================================================================
#first Layer
dotT0 = 1.0/m * (V_PSOS * TSOS - msto * TSH0 - (m0plus + V_PSOS - msto) * TSH0 + m0plus * TSH0_1 \
    - (alpha_sto * (storage_surface + storage_top_surface) * (TSH0 - Tamb)) / cp_water \
    - (alpha_water * layer_surface * (TSH0 - TSH0_1)) /cp_water) + alpha_iso
#m0minus = (m0plus + V_PSOS - msto) 

#layer1.1
dotT0_1 = 1.0/m * ((m0plus + V_PSOS - msto) * TSH0 - m0plus * TSH0_1 - (m0plus + V_PSOS - msto) * TSH0_1 + m0plus * TSH0_2 \
    - (alpha_sto * storage_surface * (TSH0_1 - Tamb)) / cp_water \
    + (alpha_water * layer_surface * (TSH0 - TSH0_1)) /cp_water \
    - (alpha_water * layer_surface * (TSH0_1 - TSH0_2)) /cp_water)

#layer1.2
dotT0_2 = 1.0/m * ((m0plus + V_PSOS - msto) * TSH0_1 - m0plus * TSH0_2 - (m0plus + V_PSOS - msto) * TSH0_2 + m0plus * TSH2 \
    - (alpha_sto * storage_surface * (TSH0_2 - Tamb)) / cp_water \
    + (alpha_water * layer_surface * (TSH0_1 - TSH0_2)) /cp_water \
    - (alpha_water * layer_surface * (TSH0_2 - TSH2)) /cp_water) 

#second Layer
dotT2 = 1.0/m * ( -V_PSOS * VSHP_OP * TSH2 + msto * VSHS_OP * TCO_1 + (m0plus + V_PSOS - msto) * TSH0_2 - m0plus * TSH2  \
    - (-V_PSOS * VSHP_OP + V_PSOS - msto + msto * VSHS_OP + m2plus) * TSH2 + m2plus * TSH2_1 \
    - (alpha_sto * storage_surface * (TSH2 - Tamb)) / cp_water \
    + (alpha_water * layer_surface * (TSH0_2 - TSH2)) /cp_water \
    - (alpha_water * layer_surface * (TSH2 - TSH2_1)) /cp_water)
#m2minus = (-V_PSOS*VSHP_OP +V_PSOS -msto +msto*VSHS_OP +m2plus)

#layer2.1
dotT2_1 = 1.0/m * ((-V_PSOS*VSHP_OP +V_PSOS -msto +msto*VSHS_OP +m2plus) * TSH2 - m2plus * TSH2_1 - \
    (-V_PSOS*VSHP_OP +V_PSOS -msto +msto*VSHS_OP +m2plus) * TSH2_1 + m2plus * TSH2_2 \
    - (alpha_sto * storage_surface * (TSH2_1 - Tamb)) / cp_water \
    + (alpha_water * layer_surface * (TSH2 - TSH2_1)) /cp_water \
    - (alpha_water * layer_surface * (TSH2_1 - TSH2_2)) /cp_water)

#layer2.2
dotT2_2 = 1.0/m * ((-V_PSOS*VSHP_OP +V_PSOS -msto +msto*VSHS_OP +m2plus) * TSH2_1 - m2plus * TSH2_2 - \
    (-V_PSOS*VSHP_OP +V_PSOS -msto +msto*VSHS_OP +m2plus) * TSH2_2 + m2plus * TSH3 \
    - (alpha_sto * storage_surface * (TSH2_2 - Tamb)) / cp_water \
    + (alpha_water * layer_surface * (TSH2_1 - TSH2_2)) /cp_water \
    - (alpha_water * layer_surface * (TSH2_2 - TSH3)) /cp_water)

#third Layer
dotT3 = 1.0/m * ((-V_PSOS * VSHP_OP + V_PSOS - msto + msto*VSHS_OP + m2plus) * TSH2_2 - m2plus * TSH3 \
    - (-V_PSOS * VSHP_OP + V_PSOS - msto + msto * VSHS_OP  + m2plus) * TSH3 + m2plus * TSH3_1 \
    - (alpha_sto * storage_surface * (TSH3 - Tamb)) / cp_water \
    + (alpha_water * layer_surface * (TSH2_2 - TSH3)) /cp_water \
    - (alpha_water * layer_surface * (TSH3 - TSH3_1)) /cp_water)
#m3minus = (-V_PSOS*VSHP_OP +V_PSOS -msto +msto*VSHS_OP  +m3plus)## m3minus ist m2minus und m3plus ist m2plus

#leyer3.1
dotT3_1 = 1.0/m * ((-V_PSOS*VSHP_OP +V_PSOS -msto +msto*VSHS_OP  +m2plus) * TSH3 - m2plus * TSH3_1 \
    - (-V_PSOS*VSHP_OP +V_PSOS -msto +msto*VSHS_OP  +m2plus) * TSH3_1 + m2plus * TSH3_2 \
    - (alpha_sto * storage_surface * (TSH3_1 - Tamb)) / cp_water \
    + (alpha_water * layer_surface * (TSH3 - TSH3_1)) /cp_water \
    - (alpha_water * layer_surface * (TSH3_1 - TSH3_2)) /cp_water)

#leyer3.2
dotT3_2 = 1.0/m * ((-V_PSOS*VSHP_OP +V_PSOS -msto +msto*VSHS_OP  +m2plus) * TSH3_1 - m2plus * TSH3_2 \
    - (-V_PSOS*VSHP_OP +V_PSOS -msto +msto*VSHS_OP  +m2plus) * TSH3_2 + m2plus * TSH1 \
    - (alpha_sto * storage_surface * (TSH3_2 - Tamb)) / cp_water \
    + (alpha_water * layer_surface * (TSH3_1 - TSH3_2)) /cp_water \
    - (alpha_water * layer_surface * (TSH3_2 - TSH1)) /cp_water)

#fourth Layer
dotT1 = 1.0/m * (-V_PSOS * VSHP_CL * TSH1 + (-V_PSOS * VSHP_OP + V_PSOS - msto + msto * VSHS_OP  + m2plus) * TSH3_2 \
    - m2plus * TSH1 + msto * VSHS_CL * TCO_1 \
    - (alpha_sto * storage_surface * (TSH1 - Tamb)) / cp_water \
    - (alpha_floor * floor_surface * (TSH1 - Tfloor)) / cp_water \
    + (alpha_water * layer_surface * (TSH3_2 - TSH1)) /cp_water)
#=================================================================================================================================================


#ODE

f = ca.vertcat([ \
    dotT0, \
    dotT2, \
    dotT3, \
    dotT1, \
    dotT0_1,\
    dotT0_2,\
    dotT2_1,\
    dotT2_2,\
    dotT3_1,\
    dotT3_2])

phi = x

system = cp.system.System(x = x, u = u, f = f, phi = phi, p = p)


# Start heating

int_start = 0
# int_end = [1000]
# int_step = 1


#20161015 "Intervalle/20160303_Intervall7.csv"
data = pd.read_table("data-ausgewertet/10_layer/"+ datatable + ".csv", \
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
x4_init = data["TSH0_1"].values[int_start] 
x5_init = data["TSH0_2"].values[int_start] 
x6_init = data["TSH2_1"].values[int_start] 
x7_init = data["TSH2_2"].values[int_start] 
x8_init = data["TSH3_1"].values[int_start] 
x9_init = data["TSH3_2"].values[int_start] 

xinit = ca.horzcat([pl.atleast_2d(x0_init).T, pl.atleast_2d(x1_init).T, pl.atleast_2d(x2_init).T, pl.atleast_2d(x3_init).T, \
    pl.atleast_2d(x4_init).T, pl.atleast_2d(x5_init).T, pl.atleast_2d(x6_init).T, pl.atleast_2d(x7_init).T, pl.atleast_2d(x8_init).T, \
    pl.atleast_2d(x9_init).T,]) 


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


pl.figure(figsize= (20,14))
# pl.subplot(2, 1, 1)
pl.subplot2grid((3, 1), (0, 0), rowspan=2)

pl.scatter(time_points[::500], data["TSH0"].values[int_start::500], marker = "x", label = r"meas TSH0", color = "b")
pl.scatter(time_points[::500], data["TSH2"].values[int_start::500], marker = "x", label = r"meas TSH2", color = "g")
pl.scatter(time_points[::500], data["TSH3"].values[int_start::500], marker = "x", label = r"meas TSH3", color = "r")
pl.scatter(time_points[::500], data["TSH1"].values[int_start::500], marker = "x", label = r"meas TSH1", color = "c")
# pl.scatter(time_points[::500], data["TSH0_1"].values[int_start::500], marker = "x", label = r"meas TSH0_1", color = "m")
# pl.scatter(time_points[::500], data["TSH0_2"].values[int_start::500], marker = "x", label = r"meas TSH0_2", color = "k")
# pl.scatter(time_points[::500], data["TSH2_1"].values[int_start::500], marker = "x", label = r"meas TSH2_1", color = "y")
# pl.scatter(time_points[::500], data["TSH2_2"].values[int_start::500], marker = "x", label = r"meas TSH2_2", color = "grey")
# pl.scatter(time_points[::500], data["TSH3_1"].values[int_start::500], marker = "x", label = r"meas TSH3_1", color = "saddlebrown")
# pl.scatter(time_points[::500], data["TSH3_2"].values[int_start::500], marker = "x", label = r"meas TSH3_2", color = "lime")
pl.plot(time_points, pl.squeeze(sim_est.simulation_results[0,:]), label = r"sim TSH0", color = "b")
pl.plot(time_points, pl.squeeze(sim_est.simulation_results[1,:]), label = r"sim TSH2", color = "g")
pl.plot(time_points, pl.squeeze(sim_est.simulation_results[2,:]), label = r"sim TSH3", color = "r")
pl.plot(time_points, pl.squeeze(sim_est.simulation_results[3,:]), label = r"sim TSH1", color = "c")
# pl.plot(time_points, pl.squeeze(sim_est.simulation_results[4,:]), label = r"sim TSH0_1", color = "m")
# pl.plot(time_points, pl.squeeze(sim_est.simulation_results[5,:]), label = r"sim TSH0_2", color = "k")
# pl.plot(time_points, pl.squeeze(sim_est.simulation_results[6,:]), label = r"sim TSH2_1", color = "y")
# pl.plot(time_points, pl.squeeze(sim_est.simulation_results[7,:]), label = r"sim TSH2_2", color = "grey")
# pl.plot(time_points, pl.squeeze(sim_est.simulation_results[8,:]), label = r"sim TSH3_1", color = "saddlebrown")
# pl.plot(time_points, pl.squeeze(sim_est.simulation_results[9,:]), label = r"sim TSH3_2", color = "lime")
pl.plot(time_points[::500], data["TSOS"].values[int_start::500], label = r"meas TSOS", color = "darkorange")
pl.title("storage model")
pl.ylabel('temperature (C)')
pl.xlabel('time (s)')
pl.legend(loc = "upper left")
# pl.legend(loc = "upper right")
pl.xlim([time_points[0], 86000])
pl.title("Scenario: " +  datatable , y=1.08)

# pl.subplot(2, 1, 2)
pl.subplot2grid((3, 1), (2, 0))

pl.plot(time_points , data["V_PSOS"], label = "V_PSOS")
pl.plot(time_points , data["msto"], label = "msto")
pl.xlabel('time (s)')
pl.ylabel('massflow (kg/s)')
pl.legend(loc = "upper left")


pl.savefig("/home/da/Master/Thesis/Optimal-Control-Storage/plots_pe/10_schichten/" + str(datatable) + "_" \
   + "start_from_" + str(int_start) + "_" \
  #+ str(int_end)+\
   "storage.png", \
        bbox_inches='tight')


# pl.show()