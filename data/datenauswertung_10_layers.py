import pandas as pd
import datetime
import pylab as pl
import numpy as np


########################
date = "2017-02-07"
start_time = "00:00:00"
end_time = "23:59:59"
########################

## auslesen direkt aus datenbank
connection_string = "postgresql+psycopg2://stcs_student:stcs_student@w-stcs-services:5432/stcs"
# connection_string = "postgresql+psycopg2://stcs_student:stcs_student@w-stcs-services.hs-karlsruhe.de:5432/stcs"

## Zeitpunkt muss hier angepasst werden
query = """
SELECT timestamp,tsh0,tsh1,tsh2,tsh3,tsos,psos,tshsi,vshs_op,vshs_cl,vshp_op,vshp_cl,pc_1,cch_1,tco_1,tci_1
FROM stcs.public.chillii_rolling_median
WHERE timestamp > '""" + date + " " + start_time + \
"""' AND timestamp < '""" + date + " " + end_time + \
"""' ORDER BY timestamp
"""

data = pd.read_sql_query(query, con=connection_string)

# ## aktuelle csv
# nametable = "20170223"
# data = pd.read_table(nametable+'.csv', sep = ",") #index_col=0)
# data = data[["timestamp","tsh0","tsh1", "tsh2", "tsh3", "tsos", "psos", "tshsi", "vshs_op", "vshs_cl", "vshp_op", "vshp_cl", "pc_1", "cch_1", "tco_1"]]
# # data = data.drop(data.index[0])

## rename collumns 
data.rename(columns={'timestamp': 'time'}, inplace=True)
data.rename(columns={'tsh0': 'TSH0'}, inplace=True)
data.rename(columns={'tsh1': 'TSH1'}, inplace=True)
data.rename(columns={'tsh2': 'TSH2'}, inplace=True)
data.rename(columns={'tsh3': 'TSH3'}, inplace=True)
data.rename(columns={'tsos': 'TSOS'}, inplace=True)
data.rename(columns={'psos': 'PSOS'}, inplace=True)
data.rename(columns={'tshsi': 'TSHSI'}, inplace=True)
data.rename(columns={'vshs_op': 'VSHS_OP'}, inplace=True)
data.rename(columns={'vshs_cl': 'VSHS_CL'}, inplace=True)
data.rename(columns={'vshp_op': 'VSHP_CL'}, inplace=True) # OP-CL vertauscht in Datenbank
data.rename(columns={'vshp_cl': 'VSHP_OP'}, inplace=True) # OP-CL vertauscht in Datenbank
data.rename(columns={'pc_1': 'PC_1'}, inplace=True)
data.rename(columns={'cch_1': 'CCH_1'}, inplace=True)
data.rename(columns={'tco_1': 'TCO_1'}, inplace=True)
data.rename(columns={'tci_1': 'TCI_1'}, inplace=True)

## set true/false to 1/0
data[['VSHS_OP','VSHS_CL','VSHP_OP','VSHP_CL']] = data[['VSHS_OP','VSHS_CL','VSHS_OP','VSHS_CL']].astype(int)

## correction of Temperature Delta
data['TSOS'] = data['TSOS'] - 0
data['TSH0'] = data['TSH0'] - 0.7
data['TSH2'] = data['TSH2'] - 0.5
data['TSH3'] = data['TSH3'] - 0.3
data['TSH1'] = data['TSH1'] - 0.4
data['TCO_1'] = data['TCO_1'] - 0.4
data['TCI_1'] = data['TCI_1'] - 0.5

# # alte csv
# #=================================================================================================================================================
# date = "20160930"
# data = pd.read_table(date+'.csv', sep = ";") #index_col=0)
# data = data[["Uhrzeit","TSH0","TSH1", "TSH2", "TSH3", "TSOS", "PSOS", "TSHSI", "VSHS_OP", "VSHS_CL", "VSHP_OP", "VSHP_CL", "PC_1", "CCH_1", "TCO_1", "TCI_1"]]
# data = data.drop(data.index[0])

# data["Uhrzeit"] = map(lambda x: "23.10.2016" + " " + x, data["Uhrzeit"])
# data["Uhrzeit"] = pd.to_datetime(data["Uhrzeit"])
# data["Uhrzeit"] = map(lambda x: x + datetime.timedelta(minutes=38), data["Uhrzeit"])
# data.sort_values(by='Uhrzeit')
# #=================================================================================================================================================



#data["PSOP"] = pd.to_numeric(data["PSOP"])
data["PSOS"] = pd.to_numeric(data["PSOS"])
data["PC_1"] = pd.to_numeric(data["PC_1"])
#
## ungefaehre Umrechnung von Spannung auf Massenstrom
# data["PSOS"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((36.0 - 23.5)/(100.0-50.0)) + 23.5) / 60.0, data["PSOS"])
data["PSOS"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((30.0 - 19.6)/(100.0-50.0)) + 19.6) / 60.0, data["PSOS"])## korrekt Test30l
# data["PC_1"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((36.0 - 23.5)/(100.0-50.0)) + 23.5) / 60.0, data["PC_1"])
# data["PC_1"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((34.0 - 20.3)/(100.0-50.0)) + 20.3) / 60.0, data["PC_1"]) ## keine Beimischung
data["PC_1"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((30.0 - 18.3)/(100.0-50.0)) + 18.3) / 60.0, data["PC_1"]) ## volle Beimischung

# #=======================================================
# # Negative Werte durch 0 ersetzen
# data = data.clip(lower=0)
# data = data.rename(columns={'Uhrzeit': 'time'}) ## alte csv
# # Timestamps zu Floats und auf Null setzen
# data["time"] = map(lambda y: float(y.seconds), data["time"] - data["time"][1]) #alte csv
# #=======================================================

dt  = map(lambda x: (x-data["time"][0]).total_seconds(), data["time"]) #aus Datenbank
data['time'] = dt # datenbank

## Berechnung zwischenschichten
data['TSH0_1'] = data["TSH0"] - 1.0 * ((data["TSH0"] - data["TSH2"]) / 3) 
data['TSH0_2'] = data["TSH0"] - 2.0 * ((data["TSH0"] - data["TSH2"]) / 3)  
data['TSH2_1'] = data["TSH2"] - 1.0 * ((data["TSH2"] - data["TSH3"]) / 3) 
data['TSH2_2'] = data["TSH2"] - 2.0 * ((data["TSH2"] - data["TSH3"]) / 3) 
data['TSH3_1'] = data["TSH3"] - 1.0 * ((data["TSH3"] - data["TSH1"]) / 3) 
data['TSH3_2'] = data["TSH3"] - 2.0 * ((data["TSH3"] - data["TSH1"]) / 3) 

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
data['msto'] = data['PC_1'] * ((data['TCI_1'] - data['TCO_1']) / (data['TSH0'] - data ['TCO_1'])) 
data.loc[data['msto'] < 0.0000000000000000000000000001, 'msto'] = 0.0 ## Negative Werter entfernen 

### calculate massflows from the layers

# Calculate m0
data_m0 = data['PSOS'] - data['msto'] 

# data['m0'] = data['PSOS'] - data['PC_1'] 
# data_m0 = data['m0']

# separate if m0minus or m0plus
data['m0plus'] = data_m0[(data_m0 <= 0.0)]
data['m0minus'] = data_m0[(data_m0 >= 0.0)]

# Fill NaN with 0
data['m0minus'].fillna(0, inplace = True )
data['m0plus'].fillna(0, inplace = True )

# Change negative massflow from m0plus into positive
data['m0plus'] = data['m0plus'] * (-1)
# data['m0plus'].replace( -0.0 , 0.0)
# data['m0plus'] = data['m0plus'].clip(lower=0.0000000000000000000000000000000001)
data.loc[data['m0plus'] < 0.0000000000000000000000000001, 'm0plus'] = 0.0


# Calculate m2
data_m2 = - data['m0plus'] + data['m0minus'] - data['PSOS']*data['VSHP_OP'] + data['msto']*data['VSHS_OP'] 

# separate if m2minus or m2plus
data['m2plus'] = data_m2[(data_m2 <= 0.0)]
data['m2minus'] = data_m2[(data_m2 >= 0.0)]

# Fill NaN with 0
data['m2minus'].fillna(0, inplace = True )
data['m2plus'].fillna(0, inplace = True )

# Change negative massflow from m2plus into positive
data['m2plus'] = data['m2plus'] * (-1)
data.loc[data['m2plus'] < 0.0000000000000000000000000001, 'm2plus'] = 0.0


# Calculate m3
data_m3 =  - data['PSOS']*data['VSHP_CL'] + data['msto']*data['VSHS_CL']

# separate if m3minus or m3plus
data['m3plus'] = data_m3[(data_m3 >= 0.0)]
data['m3minus'] = data_m3[(data_m3 <= 0.0)]

# Fill NaN with 0
data['m3minus'].fillna(0, inplace = True )
data['m3plus'].fillna(0, inplace = True )

# Change negative massflow from m3plus into positive
data['m3minus'] = data['m3minus'] * (-1)
data.loc[data['m3minus'] < 0.0000000000000000000000000001, 'm3minus'] = 0.0


# Plotten
pl.figure(figsize= (18,12))
pl.subplot(2, 1, 1)
pl.plot(time_points , data["PSOS"], label = "PSOS")
pl.plot(time_points , data["msto"], label = "msto")

# pl.plot(data.index , data["TSOS"], label = "TSOS")
# pl.plot(data.index , data["TSH0"], label = "TSH0")
# pl.plot(data.index , data["TSH1"], label = "TSH1")

# pl.plot(data.index , data["TSH2"], label = "TSH2")
# pl.plot(data.index , data["TSH3"], label = "TSH3")

# pl.plot(data.index , data["TCO_1"], label = "TCO_1")

# pl.plot(data.index , data["TSHSI"], label = "TSHSI")
pl.xlabel('time (s)')
pl.ylabel('massflow (kg/s)')
pl.legend(loc = "upper left")
pl.title("Scenario: " +  date , y=1.08)

pl.subplot(2, 1, 2)
pl.plot(time_points , data["TSH0"], label = "TSH0")
pl.plot(time_points , data["TSH1"], label = "TSH1")

pl.plot(time_points , data["TSH2"], label = "TSH2")
pl.plot(time_points , data["TSH3"], label = "TSH3")

# pl.plot(time_points , data["TSH0_1"], label = "TSH0_1")
# pl.plot(time_points , data["TSH0_2"], label = "TSH0_2")
# pl.plot(time_points , data["TSH2_1"], label = "TSH2_1")
# pl.plot(time_points , data["TSH2_2"], label = "TSH2_2")
# pl.plot(time_points , data["TSH3_1"], label = "TSH3_1")
# pl.plot(time_points , data["TSH3_2"], label = "TSH3_2")
pl.xlabel('time (s)')
pl.ylabel('temperature ($^{\circ}$C)')
pl.legend(loc = "upper left")


pl.savefig("/home/da/Master/Thesis/Optimal-Control-Storage/plots/"+ str(date) + "_10_layer_pumpen.png")
pl.show()

data.rename(columns={'PSOS': 'V_PSOS'}, inplace=True)
data.rename(columns={'PC_1': 'V_PC_1'}, inplace=True)


print data.head()


data.to_csv('/home/da/Master/Thesis/Optimal-Control-Storage/data-ausgewertet/10_layer/' + 'data' + str(date) + '.csv')



