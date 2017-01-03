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

#ODE

f = ca.vertcat( \
    dotT0, \
    dotT2, \
    dotT3, \
    dotT1)

#phi = room_temperature

system = cp.system.System(x = x, u = u, f = f)#, p = p, phi = phi)


# Start heating

int_start = 0
int_end = 1000
steps = 1

# int_start = 10800
# int_end = 11500
# steps = 1

TSH0 = x[0]
TSH2  = x[1]
TSH3  = x[2]
TSH1  = x[3]

data = pd.read_table("data20161015.csv", \
    delimiter=";", index_col=0)

for k,e in enumerate(int_start):

    time_points = pl.linspace(0, int_end[k] - e - 1, int_end[k] - e) 

    udata_0 = data["PSOS"][e:int_end[k]-1:int_step].values

    udata_1 = data["PC_1"][e:int_end[k]-1:int_step].values 

    udata_2 = data["m0minus"][e:int_end[k]-1:int_step].values 

    udata_3 = data["m0plus"][e:int_end[k]-1:int_step].values

    udata_4 = data["m2minus"][e:int_end[k]-1:int_step].values

    udata_5 = data["m2plus"][e:int_end[k]-1:int_step].values 

    udata_6 = data["m3minus"][e:int_end[k]-1:int_step].values 

    udata_7 = data["m3plus"][e:int_end[k]-1:int_step].values

    udata = ca.horzcat([udata_0, udata_1, udata_2, udata_3, udata_4, udata_5, udata_6, udata_7])

    #t_outlet = data["Outlet"][e:int_end[k]-1:int_step].values #from pe_step3

    x0_init = TSH0
    x1_init = TSH2
    x2_init = TSH3
    x3_init = TSH1

    #y1_5_init = pl.linspace(udata_3[0], t_outlet[0], 5) #from pe_step3

    xinit = ca.horzcat([pl.atleast_2d(x0_init).T, pl.atleast_2d(x1_init).T, pl.atleast_2d(x2_init).T, pl.atleast_2d(x3_init).T,]) #????

    # wv = pl.ones(ydata.shape[0])
    # wv[:int(ydata.shape[0]*0.1)] = 5

    pe_setups.append(cp.pe.LSq(system = system, time_points = time_points, \
        udata = udata, \
        #pinit = pinit, \
        #ydata = ydata, \
        xinit = xinit)) #, \
        # wv = wv))


mpe = cp.pe.MultiLSq(pe_setups)
# # mpe.run_parameter_estimation({"linear_solver": "ma57"})
mpe.run_parameter_estimation()

# sim_est = cp.sim.Simulation(system = system, pdata = est_parameter)
sim_est = cp.sim.Simulation(system = system, pdata = mpe.estimated_parameters)
# sim_est.run_system_simulation(time_points = time_points, \
#     x0 = xinit[0,:], udata = udata)

pl.close("all")


# # Plot

plt.figure(figsize= (8,7))

plt.subplot(2, 1, 1)
plt.plot(tgrid,x[0],'--')
plt.plot(tgrid,x[1],'--')
plt.plot(tgrid,x[2],'--')
plt.plot(tgrid,x[3],'--')
plt.plot(tgrid,u[0],'--')
plt.plot(tgrid,u[1],'--')
plt.plot(tgrid,u[2],'--')
plt.plot(tgrid,u[3],'--')
plt.plot(tgrid,u[4],'--')
plt.plot(tgrid,u[5],'--')
plt.plot(tgrid,u[6],'--')
plt.plot(tgrid,u[7],'--')
plt.title("storage model")
plt.ylabel('temperature (C)')
plt.xlabel('time (s)')


# plt.show()

plt.savefig("/tmp/storage/" + str(data) + "_" \
  + str(int_start) + "-" \
  + str(int_end)+ "storage.png", \
        bbox_inches='tight')


