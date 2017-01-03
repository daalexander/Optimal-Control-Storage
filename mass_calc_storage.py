import pandas as pd
import numpy as NP
import casadi as ca

data = pd.read_table("data20161015.csv", \
    delimiter=";")#, index_col=0)

list1 = data["TSOS"]
list2 = data["PC_1"]

list3 = list1 - list2

# list3 = list3.astype(float)

# data.to_csv('/home/da/Master/Thesis/massdata.csv')