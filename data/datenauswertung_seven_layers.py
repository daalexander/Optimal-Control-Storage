import pandas as pd
import datetime
import pylab as pl
import numpy as np


########################
date = "2017-03-22"
start_time = "00:00:00"
end_time = "23:59:59"
########################

## auslesen aus datenbank
connection_string = "postgresql+psycopg2://stcs_student:stcs_student@w-stcs-services:5432/stcs"

## Zeitpunkt muss hier angepasst werden
query = """
SELECT timestamp,tsh0,tsh1,tsh2,tsh3,tsos,psos,tshsi,vshs_op,vshs_cl,vshp_op,vshp_cl,pc_1,cch_1,tco_1,tci_1
FROM stcs.public.chillii_rolling_median
WHERE timestamp > '""" + date + " " + start_time + \
"""' AND timestamp < '""" + date + " " + end_time + \
"""' ORDER BY timestamp
"""

data = pd.read_sql_query(query, con=connection_string)


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



#data["PSOP"] = pd.to_numeric(data["PSOP"])
data["PSOS"] = pd.to_numeric(data["PSOS"])
data["PC_1"] = pd.to_numeric(data["PC_1"])

## ungefaehre Umrechnung von Spannung auf Massenstrom

data["PSOS"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((30.0 - 19.6)/(100.0-50.0)) + 19.6) / 60.0, data["PSOS"])
data["PC_1"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((30.0 - 18.3)/(100.0-50.0)) + 18.3) / 60.0, data["PC_1"]) 


dt  = map(lambda x: (x-data["time"][0]).total_seconds(), data["time"]) #aus Datenbank
data['time'] = dt # datenbank

## Berechnung zwischenschichten
data['TSH0_5'] = (data["TSH0"] + data["TSH2"]) / 2
data['TSH2_5'] = (data["TSH2"] + data["TSH3"]) / 2
data['TSH3_5'] = (data["TSH3"] + data["TSH1"]) / 2


# start = 4370
# end = 6640
# step = 1

# data = data[start:end:step].astype(float)

data = data.astype(float)


time_points = data["time"]

## Mischverhaeltniss entnahme Speicher
data['msto'] = data['PC_1'] * ((data['TCI_1'] - data['TCO_1']) / (data['TSH0'] - data ['TCO_1'])) 
data.loc[data['msto'] < 0.0000000000000000000000000001, 'msto'] = 0.0 

### calculate massflows from the layers

# Calculate m0
data_m0 = data['PSOS'] - data['msto'] 


# separate if m0minus or m0plus
data['m0plus'] = data_m0[(data_m0 <= 0.0)]
data['m0minus'] = data_m0[(data_m0 >= 0.0)]

# Fill NaN with 0
data['m0minus'].fillna(0, inplace = True )
data['m0plus'].fillna(0, inplace = True )

# Change negative massflow from m0plus into positive
data['m0plus'] = data['m0plus'] * (-1)
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


pl.xlabel('time (s)')
pl.ylabel('massflow (kg/s)')
pl.legend(loc = "upper left")
pl.title("Scenario: " +  date , y=1.08)

pl.subplot(2, 1, 2)
pl.plot(time_points , data["TSH0"], label = "TSH0")
pl.plot(time_points , data["TSH1"], label = "TSH1")

pl.plot(time_points , data["TSH2"], label = "TSH2")
pl.plot(time_points , data["TSH3"], label = "TSH3")

pl.plot(time_points , data["TSH0_5"], label = "TSH0_5")
pl.plot(time_points , data["TSH2_5"], label = "TSH2_5")
pl.plot(time_points , data["TSH3_5"], label = "TSH3_5")
pl.xlabel('time (s)')
pl.ylabel('temperature ($^{\circ}$C)')
pl.legend(loc = "upper left")


pl.savefig("/home/da/Master/Thesis/Optimal-Control-Storage/plots/"+ str(date) + "_7_layer_pumpen.png")
pl.show()

data.rename(columns={'PSOS': 'V_PSOS'}, inplace=True)
data.rename(columns={'PC_1': 'V_PC_1'}, inplace=True)


print data.head()


data.to_csv('/home/da/Master/Thesis/Optimal-Control-Storage/data-ausgewertet/7_layer/' + 'data' + str(date) + '.csv')



