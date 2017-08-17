import pandas as pd
import datetime
import pylab as pl
import numpy as np


########################
date = "2017-05-28"
start_time = "00:00:00"
end_time = "23:59:59"
########################

## auslesen aus datenbank
connection_string = "postgresql+psycopg2://stcs_student:stcs_student@w-stcs-services:5432/stcs"

query = """
SELECT timestamp,tsh0,tsh1,tsh2,tsh3,tsos,psos,tshsi,vshs_op,vshs_cl,vshp_op,vshp_cl,pc_1,cch_1,tco_1,tci_1,a_in_1,tchgo_1
FROM stcs.public.chillii
WHERE timestamp > '""" + date + " " + start_time + \
"""' AND timestamp < '""" + date + " " + end_time + \
"""' ORDER BY timestamp
"""


data = pd.read_sql_query(query, con=connection_string)


##===========================================================================================================
#messfehler durch median glaetten
data["tsh0"] = pd.rolling_median(data["tsh0"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tsh1"] = pd.rolling_median(data["tsh1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tsh2"] = pd.rolling_median(data["tsh2"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tsh3"] = pd.rolling_median(data["tsh3"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tsos"] = pd.rolling_median(data["tsos"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["psos"] = pd.rolling_median(data["psos"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tshsi"] = pd.rolling_median(data["tshsi"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["vshs_op"] = pd.rolling_median(data["vshs_op"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["vshs_cl"] = pd.rolling_median(data["vshs_cl"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["vshp_op"] = pd.rolling_median(data["vshp_op"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["vshp_cl"] = pd.rolling_median(data["vshp_cl"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["pc_1"] = pd.rolling_median(data["pc_1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["cch_1"] = pd.rolling_median(data["cch_1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tco_1"] = pd.rolling_median(data["tco_1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tci_1"] = pd.rolling_median(data["tci_1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["a_in_1"] = pd.rolling_median(data["a_in_1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
data["tchgo_1"] = pd.rolling_median(data["tchgo_1"], window=5, center=True).fillna(method='bfill').fillna(method='ffill')
##===========================================================================================================


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
data.rename(columns={'a_in_1': 'A_IN_1'}, inplace=True)
data.rename(columns={'tchgo_1': 'TCHGO_1'}, inplace=True)

## Massflow in kg/s
data['A_IN_1'] = data['A_IN_1'] / 60.0

## set true/false to 1/0
data[['VSHS_OP','VSHS_CL','VSHP_OP','VSHP_CL','CCH_1']] = data[['VSHS_OP','VSHS_CL','VSHS_OP','VSHS_CL','CCH_1']].astype(int)

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
data['TSH0_1'] = data["TSH0"] - 1.0 * ((data["TSH0"] - data["TSH2"]) / 3) 
data['TSH0_2'] = data["TSH0"] - 2.0 * ((data["TSH0"] - data["TSH2"]) / 3)  
data['TSH2_1'] = data["TSH2"] - 1.0 * ((data["TSH2"] - data["TSH3"]) / 3) 
data['TSH2_2'] = data["TSH2"] - 2.0 * ((data["TSH2"] - data["TSH3"]) / 3) 
data['TSH3_1'] = data["TSH3"] - 1.0 * ((data["TSH3"] - data["TSH1"]) / 3) 
data['TSH3_2'] = data["TSH3"] - 2.0 * ((data["TSH3"] - data["TSH1"]) / 3) 


# start = 4370
# end = 6640
# step = 1

# data = data[start:end:step].astype(float)

data = data.astype(float)


time_points = data["time"]

## Mischverhaeltniss entnahme Speicher
# data['msto'] = data['PC_1'] * ((data['TCI_1'] - data['TCO_1']) / (data['TSH0'] - data ['TCO_1']))  #### for heating
# data['msto'] = map(lambda x: data['A_IN_1'] if data['CCH_1'] == 1 \
# 	else data['PC_1'] * ((data['TCI_1'] - data['TCO_1']) / (data['TSH0'] - data ['TCO_1']))
# data['msto'] = np.where(data['CCH_1']=1, data['A_IN_1'], np.where(data['CCH_1']=0, data['PC_1'] * ((data['TCI_1'] - data['TCO_1']) / (data['TSH0'] - data ['TCO_1'])), 0))

## searching cooling or heating
data.loc[data['CCH_1'] >= 1, 'msto'] = data['A_IN_1']
data.loc[data['CCH_1'] <= 0, 'msto'] = data['PC_1'] * ((data['TCI_1'] - data['TCO_1']) / (data['TSH0'] - data ['TCO_1']))

data.loc[data['msto'] < 0.0000000000000000000000000001, 'msto'] = 0.0 ## Negative Werter entfernen 

## calculation return flow temperatur
data['TRF'] = data['TCO_1']
data.loc[data['CCH_1'] >= 1, 'TRF'] = data['TCHGO_1']

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
pl.plot(time_points , data["PSOS"], label = "m_PSOS")
pl.plot(time_points , data["msto"], label = "msto")
pl.plot(time_points , data["CCH_1"], label = "CCH_1")
pl.xlabel('time (s)')
pl.ylabel('massflow (kg/s)')
pl.legend(loc = "upper left")
pl.title("Scenario: " +  date , y=1.08)

pl.subplot(2, 1, 2)
pl.plot(time_points , data["TSH0"], label = "TSH0")
pl.plot(time_points , data["TSH1"], label = "TSH1")

pl.plot(time_points , data["TSH2"], label = "TSH2")
pl.plot(time_points , data["TSH3"], label = "TSH3")
pl.plot(time_points , data["TSOS"], label = "TSOS", color = "darkorange")


pl.xlabel('time (s)')
pl.ylabel('temperature ($^{\circ}$C)')
pl.legend(loc = "upper left")


pl.savefig("/home/da/Master/Thesis/Optimal-Control-Storage/plots/"+ str(date) + "_10_layer_pumpen.png")
# pl.show()

data.rename(columns={'PSOS': 'V_PSOS'}, inplace=True)
data.rename(columns={'PC_1': 'V_PC_1'}, inplace=True)


print data.head()


data.to_csv('/home/da/Master/Thesis/Optimal-Control-Storage/data-ausgewertet/10_layer/' + 'data' + str(date) + '.csv')



