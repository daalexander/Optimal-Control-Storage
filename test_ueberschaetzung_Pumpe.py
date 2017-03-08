import pandas as pd
import datetime
import pylab as pl
import numpy as np


########################
date = "2017-03-08"
start_time = "08:30:00"
end_time = "20:59:59"
########################

## auslesen direkt aus datenbank
connection_string = "postgresql+psycopg2://stcs_student:stcs_student@w-stcs-services:5432/stcs"
# connection_string = "postgresql+psycopg2://stcs_student:stcs_student@w-stcs-services.hs-karlsruhe.de:5432/stcs"

## Zeitpunkt muss hier angepasst werden
query = """
SELECT timestamp,psos,pc_1,tsh0,tco_1,tci_1
FROM stcs.public.chillii_rolling_median
WHERE timestamp > '""" + date + " " + start_time + \
"""' AND timestamp < '""" + date + " " + end_time + \
"""' ORDER BY timestamp
"""

data = pd.read_sql_query(query, con=connection_string)

## Zeitpunkt muss hier angepasst werden
query2 = """
SELECT timestamp,fvfs_sos,fvfs_c_1
FROM stcs.public.flow_sensors_cellar
WHERE timestamp > '""" + date + " " + start_time + \
"""' AND timestamp < '""" + date + " " + end_time + \
"""' ORDER BY timestamp
"""

data2 = pd.read_sql_query(query2, con=connection_string)

## rename collumns 
data.rename(columns={'timestamp': 'time'}, inplace=True)
data.rename(columns={'psos': 'PSOS'}, inplace=True)
data.rename(columns={'pc_1': 'PC_1'}, inplace=True)
data.rename(columns={'tsh0': 'TSH0'}, inplace=True)
data.rename(columns={'tco_1': 'TCO_1'}, inplace=True)
data.rename(columns={'tci_1': 'TCI_1'}, inplace=True)
data2.rename(columns={'fvfs_sos': 'FVFS_SOS'}, inplace=True)
data2.rename(columns={'fvfs_c_1': 'FVFS_C_1'}, inplace=True)
data2.rename(columns={'timestamp': 'time'}, inplace=True)

data['TSH0'] = data['TSH0'] - 0.7
data['TCO_1'] = data['TCO_1'] - 0.4
data['TCI_1'] = data['TCI_1'] - 0.5

##Umrechnung prozent auf masse
data["PSOS"] = pd.to_numeric(data["PSOS"])
data["PC_1"] = pd.to_numeric(data["PC_1"])
# data["PSOS"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((36.0 - 23.5)/(100.0-50.0)) + 23.5) / 60.0, data["PSOS"])
data["PSOS"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((30.0 - 18.3)/(100.0-50.0)) + 18.3) / 60.0, data["PSOS"])## korrekt Test30l
data["PC_1"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((30.0 - 18.3)/(100.0-50.0)) + 18.3) / 60.0, data["PC_1"])

dt  = map(lambda x: (x-data["time"][0]).total_seconds(), data["time"]) #aus Datenbank
data['time'] = dt # datenbank

dt2  = map(lambda x: (x-data2["time"][0]).total_seconds(), data2["time"]) #aus Datenbank
data2['time'] = dt2 # datenbank

## Mischverhaeltniss entnahme Speicher
data['msto'] = data['PC_1'] * ((data['TCI_1'] - data['TCO_1']) / (data['TSH0'] - data ['TCO_1'])) 
# data.loc[data['msto'] < 0.0000000000000000000000000001, 'msto'] = 0.0 #unsicher


data = data.astype(float)

data2['FVFS_SOS'] = data2['FVFS_SOS'] / 60.0
data2['FVFS_C_1'] = data2['FVFS_C_1'] / 60.0


## Mischverhaeltniss entnahme Speicher
data2['FVFS_msto'] = data2['FVFS_C_1'] * ((data['TCI_1'] - data['TCO_1']) / (data['TSH0'] - data ['TCO_1'])) 
# data.loc[data['msto'] < 0.0000000000000000000000000001, 'msto'] = 0.0 #unsicher

time_points = data["time"]
time_points2 = data2["time"]


# Plotten
pl.figure(figsize= (18,12))
pl.subplot(2, 1, 1)
pl.plot(time_points , data["PSOS"], label = "PSOS")
pl.scatter(time_points2[::50] , data2["FVFS_SOS"][::50], label = "FVFS_SOS", marker = "x", color = 'g')

# pl.plot(time_points2 , data2["FVFS_SOS"], label = "FVFS_SOS")
# pl.plot(time_points2 , data2["FVFS_C_1"], label = "FVFS_C_1")

pl.xlabel('time (s)')
pl.ylabel('massflow (kg/s)')
pl.legend(loc = "upper left")
pl.title("Scenario: " +  date , y=1.08)

pl.subplot(2, 1, 2)
pl.plot(time_points , data["msto"], label = "msto")
pl.scatter(time_points2[::50]  , data2["FVFS_msto"][::50] , label = "FVFS_msto", marker = "x", color = 'g')
pl.xlabel('time (s)')
pl.ylabel('massflow (kg/s)')
pl.legend(loc = "upper left")

# pl.subplot(2, 1, 2)
# pl.plot(time_points , data["TSH0"], label = "TSH0")
# pl.plot(time_points , data["TSH1"], label = "TSH1")

# pl.plot(time_points , data["TSH2"], label = "TSH2")
# pl.plot(time_points , data["TSH3"], label = "TSH3")
# pl.xlabel('time (s)')
# pl.ylabel('temperature ($^{\circ}$C)')
# pl.legend(loc = "upper left")


# pl.savefig("/home/da/Master/Thesis/Optimal-Control-Storage/plots/"+ str(date) + "_pumpen.png")
pl.show()


data.rename(columns={'PSOS': 'V_PSOS'}, inplace=True)
data.rename(columns={'PC_1': 'V_PC_1'}, inplace=True)



# data.to_csv('/home/da/Master/Thesis/Optimal-Control-Storage/data-ausgewertet/' + 'data' + str(date) + '.csv')