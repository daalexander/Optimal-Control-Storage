import pylab as pl
import pandas as pd

import casadi as ca


# Constants



cp_water = 4182.0



# States

x = ca.MX.sym("x", 4)

TSH0 = x[0]
TSH2  = x[1]
TSH3  = x[2]
TSH1  = x[3]

# Parameters

# # p = ca.MX.sym("p", 1)

# u_glass = 0.2 # 2.0
# u_wall =  0.0786715 # see: room_pe_step1_night.py

# window_transmission = 0.00195234 # see: room_pe_step2_day.py

# u_radiator = 0.286806


# pinit = ca.vertcat([u_radiator_init])

T_ref = 23.0
mdot_radiator_min = 0.0
mdot_radiator_max = 260.0 / 3600.0
mdot_radiator_init = 0.0
T_radiator_min = 70.0
T_radiator_max = 70.0 
T_radiator_init = T_radiator_min


# Controls

u = ca.MX.sym("u", 4)

environment_temperature = u[0]
qdot_sun = u[1]
mdot_radiator_in = u[2]
feed_temperature = u[3]


# Heat flows radiator

# Heat flow CVs

qdot_cv1 = u_radiator * exchange_surface_cv * \
    (radiator_cv_temperature[0] - room_temperature)

dt_cv1 = (1.0 / (cv_m * cp_water)) * \
    (mdot_radiator_in * cp_water * \
    (feed_temperature - radiator_cv_temperature[0]) - \
    qdot_cv1)


qdot_cv2 = u_radiator * exchange_surface_cv * \
    (radiator_cv_temperature[1] - room_temperature)

dt_cv2 = (1.0 / (cv_m * cp_water)) * \
    (mdot_radiator_in * cp_water * \
    (radiator_cv_temperature[0] - radiator_cv_temperature[1]) - \
    qdot_cv2)


qdot_cv3 = u_radiator * exchange_surface_cv * \
    (radiator_cv_temperature[2] - room_temperature)

dt_cv3 = (1.0 / (cv_m * cp_water)) * \
    (mdot_radiator_in * cp_water * \
    (radiator_cv_temperature[1] - radiator_cv_temperature[2]) - \
    qdot_cv3)


qdot_cv4 = u_radiator * exchange_surface_cv * \
    (radiator_cv_temperature[3] - room_temperature)

dt_cv4 = (1.0 / (cv_m * cp_water)) * \
    (mdot_radiator_in * cp_water * \
    (radiator_cv_temperature[2] - radiator_cv_temperature[3]) - \
    qdot_cv4)


qdot_cv5 = u_radiator * exchange_surface_cv * \
    (radiator_cv_temperature[4] - room_temperature)

dt_cv5 = (1.0 / (cv_m * cp_water)) * \
    (mdot_radiator_in * cp_water * \
    (radiator_cv_temperature[3] - radiator_cv_temperature[4]) - \
    qdot_cv5)



# Sum of radiator flows

qdot_radiator = sum([qdot_cv1, qdot_cv2, qdot_cv3, qdot_cv4, qdot_cv5]) 


# Heat flows room

environment_qdot_window = u_glass * window_surface * \
   (environment_temperature - room_temperature)
  
environment_qdot_wall = u_wall * environment_surface * \
   (environment_temperature - room_temperature)

environment_qdot = environment_qdot_window + environment_qdot_wall

qdot_loss = environment_qdot

qdot_sun_effective = 0.7 * window_surface * window_transmission * qdot_sun


dt_room = (1.0 / (room_mass * cp_air)) * \
   (qdot_loss + qdot_sun_effective + qdot_radiator + qdot_otherfactors)


dxdt = ca.vertcat( \
    dt_room, \
    dt_cv1, \
    dt_cv2, \
    dt_cv3, \
    dt_cv4, \
    dt_cv5)