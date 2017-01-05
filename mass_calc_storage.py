import pandas as pd
import numpy as NP
import pylab as pl
# import casadi as ca

data = pd.read_table("data20161015.csv", sep = ",") #index_col=0)

# data = data[["Uhrzeit","TSH0","TSH1", "TSH2", "TSH3", "TSOS", "PSOS", "TSHSI", "VSHS_OP", "VSHS_CL", "VSHP_OP", "VSHP_CL", "PC_1", "CCH_1", "TCO_1"]]
data = data.drop(data.index[0])

data["PSOS"] = pd.to_numeric(data["PSOS"])
data["PC_1"] = pd.to_numeric(data["PC_1"])

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

print data.head()


data.to_csv('/home/da/Master/Thesis/massdata.csv')