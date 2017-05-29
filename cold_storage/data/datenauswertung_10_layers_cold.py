import pandas as pd
import datetime
import pylab as pl
import numpy as np


########################
date = "2017-03-29"
start_time = "00:00:00"
end_time = "23:59:59"
########################

## auslesen direkt aus datenbank
connection_string = "postgresql+psycopg2://stcs_student:stcs_student@w-stcs-services:5432/stcs"
# connection_string = "postgresql+psycopg2://stcs_student:stcs_student@w-stcs-services.hs-karlsruhe.de:5432/stcs"

## mit rolling_median
# query = """
# SELECT timestamp,tsh0,tsh1,tsh2,tsh3,tsos,psos,tshsi,vshs_op,vshs_cl,vshp_op,vshp_cl,pc_1,cch_1,tco_1,tci_1
# FROM stcs.public.chillii_rolling_median
# WHERE timestamp > '""" + date + " " + start_time + \
# """' AND timestamp < '""" + date + " " + end_time + \
# """' ORDER BY timestamp
# """


##===========================================================================================================
##ohne rolling_median
query = """
SELECT timestamp,tsc1,tsc0,pc_1,a_in_2,tchei_1,tcheo_1,cch_1,tco_1,tci_1
FROM stcs.public.chillii
WHERE timestamp > '""" + date + " " + start_time + \
"""' AND timestamp < '""" + date + " " + end_time + \
"""' ORDER BY timestamp
"""
##===========================================================================================================


data = pd.read_sql_query(query, con=connection_string)


##===========================================================================================================
#messfehler durch median glaetten
data["tsc1"] = pd.rolling_median(data["tsc1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tsc0"] = pd.rolling_median(data["tsc0"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["a_in_2"] = pd.rolling_median(data["a_in_2"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tchei_1"] = pd.rolling_median(data["tchei_1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tcheo_1"] = pd.rolling_median(data["tcheo_1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["pc_1"] = pd.rolling_median(data["pc_1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["cch_1"] = pd.rolling_median(data["cch_1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tco_1"] = pd.rolling_median(data["tco_1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tci_1"] = pd.rolling_median(data["tci_1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
##===========================================================================================================

# ## csv
# nametable = "20170223"
# data = pd.read_table(nametable+'.csv', sep = ",") #index_col=0)
# data = data[["timestamp","tsh0","tsh1", "tsh2", "tsh3", "tsos", "psos", "tshsi", "vshs_op", "vshs_cl", "vshp_op", "vshp_cl", "pc_1", "cch_1", "tco_1"]]
# # data = data.drop(data.index[0])

## rename collumns 
data.rename(columns={'timestamp': 'time'}, inplace=True)
data.rename(columns={'tsc1': 'TSC1'}, inplace=True)
data.rename(columns={'tsc0': 'TSC0'}, inplace=True)
data.rename(columns={'a_in_2': 'A_IN_2'}, inplace=True)
data.rename(columns={'tchei_1': 'TCHEI_1'}, inplace=True)
data.rename(columns={'tcheo_1': 'TCHEO_1'}, inplace=True)
data.rename(columns={'pc_1': 'PC_1'}, inplace=True)
data.rename(columns={'cch_1': 'CCH_1'}, inplace=True)
data.rename(columns={'tco_1': 'TCO_1'}, inplace=True)
data.rename(columns={'tci_1': 'TCI_1'}, inplace=True)

## set true/false to 1/0
data[['CCH_1']] = data[['CCH_1']].astype(int)

## correction of Temperature Delta
# data['TSOS'] = data['TSOS'] - 0




#data["PSOP"] = pd.to_numeric(data["PSOP"])
# data["PSOS"] = pd.to_numeric(data["PSOS"])
data["PC_1"] = pd.to_numeric(data["PC_1"])
#
## ungefaehre Umrechnung von Spannung auf Massenstrom
# data["PSOS"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((30.0 - 19.6)/(100.0-50.0)) + 19.6) / 60.0, data["PSOS"])## korrekt Test30l
data["PC_1"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((30.0 - 18.3)/(100.0-50.0)) + 18.3) / 60.0, data["PC_1"]) ## volle Beimischung

# A_IN_2 umrechnung in gk/s
data["A_IN_2"] = data["A_IN_2"] / 60.0

dt  = map(lambda x: (x-data["time"][0]).total_seconds(), data["time"]) #aus Datenbank
data['time'] = dt # datenbank

## Berechnung zwischenschichten
data['TSC1_1'] = data["TSC1"] - 1.0 * ((data["TSC1"] - data["TSC0"]) / 9) 
data['TSC1_2'] = data["TSC1"] - 2.0 * ((data["TSC1"] - data["TSC0"]) / 9) 
data['TSC1_3'] = data["TSC1"] - 3.0 * ((data["TSC1"] - data["TSC0"]) / 9) 
data['TSC1_4'] = data["TSC1"] - 4.0 * ((data["TSC1"] - data["TSC0"]) / 9) 
data['TSC1_5'] = data["TSC1"] - 5.0 * ((data["TSC1"] - data["TSC0"]) / 9) 
data['TSC1_6'] = data["TSC1"] - 6.0 * ((data["TSC1"] - data["TSC0"]) / 9) 
data['TSC1_7'] = data["TSC1"] - 7.0 * ((data["TSC1"] - data["TSC0"]) / 9) 
data['TSC1_8'] = data["TSC1"] - 8.0 * ((data["TSC1"] - data["TSC0"]) / 9) 

# Mittelwert von FlowSolarSek auf 36l/min
#data["FlowSolarSek"] = map(lambda x: 35, data["FlowSolarSek"])

#==============================================================================
# # Messreihen verschieben
# data["TSOS"] = data["TSOS"].shift(periods=-1, freq=None, axis=0)
# data["TSH2"] = data["TSH2"].shift(periods=1, freq=None, axis=0)
# data["TSH1"] = data["TSH1"].shift(periods=1, freq=None, axis=0)
# data = data[pd.notnull(data["TSOS"])]
# data = data[pd.notnull(data["TSH1"])]
# data = data[pd.notnull(data["TSH2"])]
#==============================================================================
# start = 4370
# end = 6640
# step = 1

# data = data[start:end:step].astype(float)

data = data.astype(float)


time_points = data["time"]

## Mischverhaeltniss entnahme Speicher
data['msto'] = data['PC_1'] * ((data['TCI_1'] - data['TCO_1']) / (data['TSC0'] - data ['TCO_1'])) 
data.loc[data['msto'] < 0.0000000000000000000000000001, 'msto'] = 0.0 ## Negative Werter entfernen 

### calculate massflows from the layers

# Calculate m0
data_m1 = data['msto'] - data['A_IN_2'] 

# separate if m0minus or m0plus
data['m1plus'] = data_m1[(data_m1 <= 0.0)]
data['m1minus'] = data_m1[(data_m1 >= 0.0)]

# Fill NaN with 0
data['m1minus'].fillna(0, inplace = True )
data['m1plus'].fillna(0, inplace = True )

# Change negative massflow from m0plus into positive
data['m1plus'] = data['m1plus'] * (-1)
data.loc[data['m1plus'] < 0.0000000000000000000000000001, 'm1plus'] = 0.0



# Plotten
pl.figure(figsize= (18,12))
pl.subplot(2, 1, 1)
pl.plot(time_points , data["A_IN_2"], label = "A_IN_2")
pl.plot(time_points , data["msto"], label = "msto")


pl.xlabel('time (s)')
pl.ylabel('massflow (kg/s)')
pl.legend(loc = "upper left")
pl.title("Scenario: " +  date , y=1.08)

pl.subplot(2, 1, 2)
pl.plot(time_points , data["TSC1"], label = "TSC1")
pl.plot(time_points , data["TSC0"], label = "TSC0")

pl.plot(time_points , data["TCHEO_1"], label = "TCHEO_1", color = "darkorange")


pl.xlabel('time (s)')
pl.ylabel('temperature ($^{\circ}$C)')
pl.legend(loc = "upper left")


pl.savefig("/home/da/Master/Thesis/Optimal-Control-Storage/cold_storage/plots_daten/"+ str(date) + "_10_layer_pumpen.png")
# pl.show()

# data.rename(columns={'PSOS': 'V_PSOS'}, inplace=True)
data.rename(columns={'PC_1': 'V_PC_1'}, inplace=True)


print data.head()


data.to_csv('/home/da/Master/Thesis/Optimal-Control-Storage/cold_storage/data/' + 'data' + str(date) + '.csv')



