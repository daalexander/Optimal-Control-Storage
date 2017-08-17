import pylab as pl
import pandas as pd
import numpy as np
import casadi as ca
import casiopeia as cp
import matplotlib.pyplot as plt

#############################
datatable = "data2017-06-13"
#############################


# Constants

cp_water = 4182.0
layer = 5.0
Tamb = 20.0
alpha_1 = -11.1411 
alpha_0 = -2.82515 
alpha_1_1 = -8.91987 
alpha_1_2 = -6.67047 
alpha_1_3 = -4.664 


# States
##5 Layers
x = ca.MX.sym("x", 5)
TSC1 = x[0]
TSC0  = x[1]
TSC1_1  = x[2]
TSC1_2  = x[3]
TSC1_3  = x[4]

# Parameters

p = ca.MX.sym("p", 1)
alpha_iso = p[0]


# Controls

u = ca.MX.sym("u", 6)

A_IN_2 = u[0]
msto = u[1] 
m1minus = u[2]
m1plus = u[3]
TCHEO_1 = u[4]
TCO_1 = u[5]


m = 1000.0 / layer

# Massflows storage

#=================================================================================================================================================
#first Layer
dotT1 = 1.0/m * ( -A_IN_2 * TSC1 + msto * TCO_1 - m1minus * TSC1 + m1plus * TSC1_1 + (alpha_1 * (TSC1 - Tamb)) / cp_water) + alpha_iso
#m0minus = (m0plus + V_PSOS - msto) 

#second layer
dotT0 = 1.0/m * ( A_IN_2 * TCHEO_1 - msto * TSC0 - m1plus * TSC0 + m1minus * TSC1_1 + (alpha_0 * (TSC0 - Tamb)) / cp_water) 

#
dotT1_1 = 1.0/m * ( m1minus * (TSC1 -  TSC1_1) + m1plus* (TSC1_2 - TSC1_1) + (alpha_1_1 * (TSC1_1 - Tamb)) / cp_water)

#
dotT1_2 = 1.0/m * ( m1minus * (TSC1_1 -  TSC1_2) + m1plus* (TSC1_3 - TSC1_2) + (alpha_1_2 * (TSC1_2 - Tamb)) / cp_water)

#
dotT1_3 = 1.0/m * ( m1minus * (TSC1_2 -  TSC1_3) + m1plus* (TSC0 - TSC1_3) + (alpha_1_3 * (TSC1_3 - Tamb)) / cp_water)
#=================================================================================================================================================


#ODE

f = ca.vertcat([ \
    dotT1, \
    dotT0, \
    dotT1_1, \
    dotT1_2, \
    dotT1_3]) 

phi = x

system = cp.system.System(x = x, u = u, f = f, phi = phi, p = p)


# Start heating

int_start =0
int_end = 86000
# int_step = 1


data = pd.read_table("data/"+ datatable + ".csv", \
    delimiter=",", index_col=0)


time_points = data["time"].values[int_start:]

udata_0 = data["A_IN_2"][:-1].values[int_start:]

udata_1 = data["msto"][:-1].values[int_start:]

udata_2 = data["m1minus"][:-1].values[int_start:]

udata_3 = data["m1plus"][:-1].values[int_start:]

udata_4 = data["TCHEO_1"][:-1].values[int_start:]

udata_5 = data["TCO_1"][:-1].values[int_start:]


udata = ca.horzcat([udata_0, udata_1, udata_2, udata_3, udata_4, udata_5])



x0_init = data["TSC1"].values[int_start]
x1_init = data["TSC0"].values[int_start]
x2_init = data["TSC1_1"].values[int_start] 
x3_init = data["TSC1_2"].values[int_start] 
x4_init = data["TSC1_3"].values[int_start] 


xinit = ca.horzcat([pl.atleast_2d(x0_init).T, pl.atleast_2d(x1_init).T, pl.atleast_2d(x2_init).T, pl.atleast_2d(x3_init).T, \
    pl.atleast_2d(x4_init).T,]) 



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

pl.scatter(time_points[::500], data["TSC0"].values[int_start::500], marker = "x", label = r"meas TSC0", color = "g")
pl.scatter(time_points[::500], data["TSC1"].values[int_start::500], marker = "x", label = r"meas TSC1", color = "b")
pl.plot(time_points, pl.squeeze(sim_est.simulation_results[0,:]), label = r"sim TSC1", color = "b")
pl.plot(time_points, pl.squeeze(sim_est.simulation_results[1,:]), label = r"sim TSC0", color = "g")
pl.plot(time_points[::500], data["TCHEO_1"].values[int_start::500], label = r"meas TCHEO_1", color = "darkorange")
pl.title("storage model")
pl.ylabel('temperature (C)')
pl.xlabel('time (s)')
pl.legend(loc = "upper left")

pl.xlim([time_points[0], int_end])
pl.title("Scenario: " +  datatable , y=1.08)


pl.subplot2grid((3, 1), (2, 0))

pl.plot( data["A_IN_2"], label = "A_IN_2")
pl.plot( data["msto"], label = "msto")
# pl.plot( data["CCH_1"], label = "CCH_1")
pl.xlabel('time (s)')
pl.ylabel('massflow (kg/s)')
pl.xlim([time_points[0], int_end])
pl.legend(loc = "upper left")


pl.savefig("/home/da/Master/Thesis/Optimal-Control-Storage/cold_storage/plots/" + str(datatable) + "_" \
   + "start_from_" + str(int_start) + "_" \
  #+ str(int_end)+\
   "storage.png", \
        bbox_inches='tight')


# pl.show()