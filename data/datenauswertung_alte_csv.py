import pandas as pd
import datetime
import pylab as pl
import numpy as np

# Bei data_1 vorher Zeile unter Kopfzeile und Eintraege vor 0 Uhr loeschen!

########################
nametable = "20160930"
########################

data = pd.read_table(nametable+'.csv', sep = ";") #index_col=0)
data = data[["Uhrzeit","TSH0","TSH1", "TSH2", "TSH3", "TSOS", "PSOS", "TSHSI", "VSHS_OP", "VSHS_CL", "VSHP_OP", "VSHP_CL", "PC_1", "CCH_1", "TCO_1"]]
data = data.drop(data.index[0])

data["Uhrzeit"] = map(lambda x: "23.10.2016" + " " + x, data["Uhrzeit"])
data["Uhrzeit"] = pd.to_datetime(data["Uhrzeit"])
data["Uhrzeit"] = map(lambda x: x + datetime.timedelta(minutes=38), data["Uhrzeit"])
data.sort_values(by='Uhrzeit')

#data["PSOP"] = pd.to_numeric(data["PSOP"])
data["PSOS"] = pd.to_numeric(data["PSOS"])
data["PC_1"] = pd.to_numeric(data["PC_1"])
#
# ungefaehre Umrechnung von Spannung auf Massenstrom
# pri
#data["PSOP"] = ( data["PSOP"] - 50.0 ) * ((48.0 - 28.5)/(100.0-50.0)) + 28.5
# sel
data["PSOS"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((36.0 - 23.5)/(100.0-50.0)) + 23.5) / 60.0, data["PSOS"])
# data["PC_1"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((36.0 - 23.5)/(100.0-50.0)) + 23.5) / 60.0, data["PC_1"])
# data["PC_1"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((34.0 - 20.3)/(100.0-50.0)) + 20.3) / 60.0, data["PC_1"]) ## keine Beimischung
data["PC_1"] = map(lambda x: 0 if x == 0 else (( x - 50.0 ) * ((30.0 - 18.3)/(100.0-50.0)) + 18.3) / 60.0, data["PC_1"]) ## volle Beimischung

# Negative Werte durch 0 ersetzen
data = data.clip(lower=0)

data = data.rename(columns={'Uhrzeit': 'time'})

# Timestamps zu Floats und auf Null setzen
data["time"] = map(lambda y: float(y.seconds), data["time"] - data["time"][1])
# 
# 
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

# Plotten
pl.figure()
pl.plot(data.index , data["PSOS"], label = "PSOS")
pl.plot(data.index , data["PC_1"], label = "PC_1")

# pl.plot(data.index , data["TSOS"], label = "TSOS")
# pl.plot(data.index , data["TSH0"], label = "TSH0")
# pl.plot(data.index , data["TSH1"], label = "TSH1")

# pl.plot(data.index , data["TSH2"], label = "TSH2")
# pl.plot(data.index , data["TSH3"], label = "TSH3")

# pl.plot(data.index , data["TCO_1"], label = "TCO_1")

# pl.plot(data.index , data["TSHSI"], label = "TSHSI")


pl.legend(loc = "upper left")
# pl.show()
pl.savefig("/home/da/Master/Thesis/Optimal-Control-Storage/plots/"+ str(nametable) + "_pumpen.png")
pl.show()


### calculate massflows from the layers

# Calculate m0
data_m0 = data['PSOS'] - data['PC_1'] 

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
data_m2 = - data['m0plus'] + data['m0minus'] - data['PSOS']*data['VSHP_OP'] + data['PC_1']*data['VSHS_OP'] 

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
data_m3 =  - data['PSOS']*data['VSHP_CL'] + data['PC_1']*data['VSHS_CL']

# separate if m3minus or m3plus
data['m3plus'] = data_m3[(data_m3 >= 0.0)]
data['m3minus'] = data_m3[(data_m3 <= 0.0)]

# Fill NaN with 0
data['m3minus'].fillna(0, inplace = True )
data['m3plus'].fillna(0, inplace = True )

# Change negative massflow from m3plus into positive
data['m3minus'] = data['m3minus'] * (-1)
data.loc[data['m3minus'] < 0.0000000000000000000000000001, 'm3minus'] = 0.0


data.rename(columns={'PSOS': 'V_PSOS'}, inplace=True)
data.rename(columns={'PC_1': 'V_PC_1'}, inplace=True)


print data.head()


data.to_csv('/home/da/Master/Thesis/Optimal-Control-Storage/data-probe/' + 'data' + str(nametable) + '.csv')



