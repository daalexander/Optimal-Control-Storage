import pylab as pl
import pandas as pd
import numpy as np

# import sys # for home
# sys.path.append(r"C:\Users\alexa\Documents\Master\Python programme\casadi-py27-np1.9.1-v2.4.3")
# sys.path.append(r"C:\Users\alexa\Documents\Master\Python programme\casiopeia")

import casadi as ca
import casiopeia as cp
import matplotlib.pyplot as plt

date = "data2017-02-03"

messdata = pd.read_table("data-ausgewertet/10_layer/data2017-02-03.csv", \
    delimiter=",", index_col=0)
data1 = pd.read_table("mpc/"'mpcdata2017-02-03start0.csv', sep = ",")
data2 = pd.read_table("mpc/"'mpcdata2017-02-03start38000.csv', sep = ",")
data3 = pd.read_table("mpc/"'mpcdata2017-02-03start41600.csv', sep = ",")
data4 = pd.read_table("mpc/"'mpcdata2017-02-03start45200.csv', sep = ",")
data5 = pd.read_table("mpc/"'mpcdata2017-02-03start48800.csv', sep = ",")
data6 = pd.read_table("mpc/"'mpcdata2017-02-03start52400.csv', sep = ",")
data7 = pd.read_table("mpc/"'mpcdata2017-02-03start56000.csv', sep = ",")
data8 = pd.read_table("mpc/"'mpcdata2017-02-03start59600.csv', sep = ",")
data9 = pd.read_table("mpc/"'mpcdata2017-02-03start63200.csv', sep = ",")
data10 = pd.read_table("mpc/"'mpcdata2017-02-03start66800.csv', sep = ",")
data11 = pd.read_table("mpc/"'mpcdata2017-02-03start70400.csv', sep = ",")

int_start = 0
int_end = 86000

plot_start = 35000
plot_end = 70000

time_points = messdata["time"].values[int_start:]
data1 = data1.transpose()
data2 = data2.transpose()
data3 = data3.transpose()
data4 = data4.transpose()
data5 = data5.transpose()
data6 = data6.transpose()
data7 = data7.transpose()
data8 = data8.transpose()
data9 = data9.transpose()
data10 = data10.transpose()

##Plot
pl.figure(figsize= (20,14))
# pl.subplot(2, 1, 1)
pl.subplot2grid((3, 1), (0, 0), rowspan=2)

pl.scatter(time_points[::500], messdata["TSH0"].values[int_start::500], marker = "x", label = r"meas TSH0", color = "b")
pl.scatter(time_points[::500], messdata["TSH2"].values[int_start::500], marker = "x", label = r"meas TSH2", color = "g")
pl.scatter(time_points[::500], messdata["TSH3"].values[int_start::500], marker = "x", label = r"meas TSH3", color = "r")
pl.scatter(time_points[::500], messdata["TSH1"].values[int_start::500], marker = "x", label = r"meas TSH1", color = "c")
pl.plot(time_points[::500], messdata["TSOS"].values[int_start::500], label = r"meas TSOS", color = "darkorange")

pl.plot(time_points, data1[0].values[int_start:], label = r"sim TSH2", color = "g", linestyle = "dashed")
pl.plot(time_points, data1[1].values[int_start:], label = r"sim TSH3", color = "r", linestyle = "dashed")
pl.plot(time_points, data1[2].values[int_start:], label = r"sim TSH1", color = "c", linestyle = "dashed")
pl.plot(time_points, data1[3].values[int_start:], label = r"sim TSH0", color = "b", linestyle = "dashed")

pl.plot(time_points[38000:45200], data2[0].values[0:7200], label = r"sim TSH2", color = "g")
pl.plot(time_points[38000:45200], data2[1].values[0:7200], label = r"sim TSH3", color = "r")
pl.plot(time_points[38000:45200], data2[2].values[0:7200], label = r"sim TSH1", color = "c")
pl.plot(time_points[38000:45200], data2[3].values[0:7200], label = r"sim TSH0", color = "b")
# pl.plot(time_points[38000:41600], data2[3].values[0:3600], label = r"sim TSH1", color = "c")

pl.plot(time_points[45200:52400], data4[0].values[0:7200], color = "g")
pl.plot(time_points[45200:52400], data4[1].values[0:7200], color = "r")
pl.plot(time_points[45200:52400], data4[2].values[0:7200], color = "c")
pl.plot(time_points[45200:52400], data4[3].values[0:7200], color = "b")

pl.plot(time_points[52400:59600], data6[0].values[0:7200], color = "g")
pl.plot(time_points[52400:59600], data6[1].values[0:7200], color = "r")
pl.plot(time_points[52400:59600], data6[2].values[0:7200], color = "c")
pl.plot(time_points[52400:59600], data6[3].values[0:7200], color = "b")

pl.plot(time_points[59600:66800], data8[0].values[0:7200], color = "g")
pl.plot(time_points[59600:66800], data8[1].values[0:7200], color = "r")
pl.plot(time_points[59600:66800], data8[2].values[0:7200], color = "c")
pl.plot(time_points[59600:66800], data8[3].values[0:7200], color = "b")

# pl.plot(time_points[66800:74000], data10[0].values[0:7200], label = r"sim TSH0", color = "b")
# pl.plot(time_points[66800:74000], data10[1].values[0:7200], label = r"sim TSH2", color = "g")
# pl.plot(time_points[66800:74000], data10[2].values[0:7200], label = r"sim TSH3", color = "r")
# pl.plot(time_points[66800:74000], data10[3].values[0:7200], label = r"sim TSH1", color = "c")

pl.title("storage model")
pl.ylabel('temperature (C)')
pl.xlabel('time (s)')
# pl.legend(loc = "upper left")
pl.legend(loc = "upper right")
pl.xlim([plot_start, plot_end])
pl.title("Scenario: " +  date , y=1.08)



pl.subplot2grid((3, 1), (2, 0))

pl.plot( messdata["V_PSOS"], label = "m_PSOS")
pl.plot( messdata["msto"], label = "msto")
pl.xlabel('time (s)')
pl.ylabel('massflow (kg/s)')
pl.xlim([plot_start, plot_end])
pl.legend(loc = "upper left")

# TSH2
# TSH3
# TSH1
# TSH0



# pl.savefig("/home/da/Master/Thesis/Optimal-Control-Storage/plots_pe/10_schichten_inkl_warmeaustausch/" + str(datatable) + "_" \
#    + "start_from_" + str(int_start) + "_" \
#   #+ str(int_end)+\
#    "storage.png", \
#         bbox_inches='tight')


pl.show()