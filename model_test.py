


### flows


#first Layer
dotT0 = 1/m0 * (PSOS * TSOS - PC_1 * TSH0 - (m0plus + PSOS - PC_1) * TSH0 + m0plus * TSH2) 
#m0minus = m0plus + PSOS - PC_1 

#second Layer
dotT2 = 1/m2 * (-PSOS*VSHP_OP * TSH2 + PC_1*VSHS_OP  * TCO_1 + (m0plus + PSOS - PC_1) * TSH0 - m0plus * TSH2  \
- (-PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP +m2plus) * TSH2 + m2plus * TSH3)
#m2minus = -PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP +m2plus

#third Layer
dotT3 = 1/m3 * ((-PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP +m2plus) * TSH2 - m2plus * TSH3 - (-PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP  +m3plus) * TSH1 + m3plus * TSH1)
#m3minus = -PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP  +m3plus

#fourth Layer
dotT1 = 1/m1(-PSOS*VSHP_CL * TSH1 + (-PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP  +m3plus) * TSH3 - m3plus * TSH1 + PC_1*VSHS_CL * TCO_1)


