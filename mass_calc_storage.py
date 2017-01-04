import pandas as pd
import numpy as NP
# import casadi as ca

data = pd.read_table("data20161015.csv", \
    delimiter=";")#, index_col=0)

# list1 = data["PSOS"]
# list2 = data["PC_1"]
data['m0'] = data.PSOS - data.PC_1 

data_m0 = data['m0']

data_m0plus = data_m0[(data_m0['m0'] < 0)]
data_minus = data_m0[(data_m0['m0'] > 0)]

data.insert('data_minus', 'data_m0plus')

print data.head()

# list3 = list3.astype(float)

data.to_csv('/home/da/Master/Thesis/massdata.csv')