


### flows
PSOS= PSOS
PSOS*VSHP_OP= PSOS
PSOS*VSHP_CL= PSOS


PC_1=PC_1
PC_1*VSHS_CL=PC_1
PC_1*VSHS_OP=PC_1;


#first Layer
m0 * dotT0 = PSOS * TSOS - PC_1 * TSH0 - (m0plus + PSOS - PC_1) * TSH0 + m0plus * TSH2 # PSOS is PSOS # PC_1 is PC_1 or A_IN_1
#m0minus = m0plus + PSOS - PC_1 

#second Layer
m2 * dotT2 = -PSOS*VSHP_OP * TSH2 + PC_1*VSHS_OP  * TCO_1 + (m0plus + PSOS - PC_1) * TSH0 - m0plus * TSH2  \
- (-PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP +m2plus) * TSH2 + m2plus * TSH3 # PSOS*VSHP_OP is PSOS, PC_1*VSHS_OP is PC_1 or A_IN_1
#m2minus = -PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP +m2plus

#third Layer
m3 * dotT3 = (-PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP +m2plus) * TSH2 - m2plus * TSH3 - (-PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP  +m3plus) * TSH1 + m3plus * TSH1
#m3minus = -PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP  +m3plus

#fourth Layer
m4 * dotT4 = -PSOS*VSHP_CL * TSH1 + (-PSOS*VSHP_OP +PSOS -PC_1 +PC_1*VSHS_OP  +m3plus) * TSH3 - m3plus * TSH1 + PC_1*VSHS_CL * TCO_1


