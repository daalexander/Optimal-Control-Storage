


### flows
m0in=
m0out=
m2in=
m2out=
m1in=
m1out=


#first Layer
m0 * dotT0 = m0in * TSOS - m0out * TSH0 - (m0plus + m0in - m0out) * TSH0 + m0plus * TSH2 # m0in is PSOS # m0out is PC_1 or A_IN_1
#m0minus = m0plus + m0in - m0out 

#second Layer
m2 * dotT2 = -m2out * TSH2 + m2in  * TCO_1 + (m0plus + m0in - m0out) * TSH0 - m0plus * TSH2  \
- (-m2out +m0in -m0out +m2in +m2plus) * TSH2 + m2plus * TSH3 # m2out is PSOS, m2in is PC_1 or A_IN_1
#m2minus = -m2out +m0in -m0out +m2in +m2plus

#third Layer
m3 * dotT3 = (-m2out +m0in -m0out +m2in +m2plus) * TSH2 - m2plus * TSH3 - (-m2out +m0in -m0out +m2in +m2plus -m2plus +m3plus) * TSH1 + m3plus * TSH1
#m3minus = -m2out +m0in -m0out +m2in +m2plus -m2plus +m3plus

#fourth Layer
m4 * dotT4 = -m1out * TSH1 + (-m2out +m0in -m0out +m2in +m2plus -m2plus +m3plus) * TSH3 - m3plus * TSH1 + m1in * TCO_1


