from pygmid import Lookup as lk
import numpy as np
lv_nmos = lk('../analog-circuit-design/gmid/sg13_lv_nmos.mat')
lv_pmos = lk('../analog-circuit-design/gmid/sg13_lv_pmos.mat')

# For the Error Amplifier
gm_id_m12 = 8
gm_id_m34 = 5
gm_id_m56 = 5
l_12 = 10
l_34 = 5
l_56 = 5
i_bias = 5e-6
i_tail = 5e-6
VDS_m12 = 2 / gm_id_m12 + 0.6
VDS_m34 = 2 / gm_id_m34 + 0.4
VDS_m56 = 2 / gm_id_m56 + 0.4

gm_m12 = gm_id_m12 * i_tail / 2

gm_gds_m12 = lv_nmos.lookup('GM_GDS', GM_ID=gm_id_m12, L=l_12, VDS=VDS_m12, VSB=0)
gm_gds_m34 = lv_pmos.lookup('GM_GDS', GM_ID=gm_id_m34, L=l_34, VDS=VDS_m34, VSB=0)

gds_m12 = gm_m12 / gm_gds_m12
gm_m34 = gm_id_m34 * i_tail/2
gds_m34 = gm_m34 / gm_gds_m34

a0 = gm_m12 / (gds_m12 + gds_m34)
print('A0 =', round(20*np.log10(a0), 1), 'dB')

vgs_m12 = lv_nmos.look_upVGS(GM_ID=gm_id_m12, L=l_12, VDS=VDS_m12, VSB=0.0)
vgs_m34 = lv_pmos.look_upVGS(GM_ID=gm_id_m34, L=l_34, VDS=VDS_m34, VSB=0.0) 
vgs_m56 = lv_nmos.look_upVGS(GM_ID=gm_id_m56, L=l_56, VDS=VDS_m56, VSB=0.0) 

print('vgs_12 =', round(float(vgs_m12), 3), 'V')
print('vgs_34 =', round(float(vgs_m34), 3), 'V')
print('vgs_56 =', round(float(vgs_m56), 3), 'V')

id_m12 = i_tail/2
# calculate all widths
id_w_m12 = lv_nmos.lookup('ID_W', GM_ID=gm_id_m12, L=l_12, VDS=vgs_m12, VSB=0)
w_12 = id_m12 / id_w_m12
w_12_round = max(round(w_12*2)/2, 0.5)
print('M1/2 W =', round(w_12, 2), 'um, rounded W =', w_12_round, 'um')

id_m34 = id_m12
id_w_m34 = lv_pmos.lookup('ID_W', GM_ID=gm_id_m34, L=l_34, VDS=vgs_m34, VSB=0)
w_34 = id_m34 / id_w_m34
w_34_round = max(round(w_34*2)/2, 0.5) 
print('M3/4 W =', round(w_34, 2), 'um, rounded W =', w_34_round, 'um')

id_w_m5 = lv_nmos.lookup('ID_W', GM_ID=gm_id_m56, L=l_56, VDS=vgs_m56, VSB=0)
w_5 = i_tail / id_w_m5
w_5_round = max(round(w_5*2)/2, 0.5)
print('M5 W =', round(w_5, 2), 'um, rounded W =', w_5_round, 'um')
w_6 = w_5_round * i_bias / i_tail
w_6_round = max(round(w_6*2)/2, 0.5)
print('M6 W =', round(w_6_round, 2), 'um')

# For the Pass Device
# gm_id_pd = 5
# i_load = 504e-6
# l_pd = 5e-6
# VDS_pd = 2 / gm_id_pd + 0.6
# gm_gds_pd = lv_nmos.lookup('GM_GDS', GM_ID=gm_id_pd, L=l_pd, VDS=VDS_pd, VSB=0)
# vgs_pd = lv_nmos.look_upVGS(GM_ID=gm_id_pd, L=l_pd, VDS=VDS_pd, VSB=0.0)
# print('vgs_12 =', round(float(vgs_pd), 3), 'V')
# id_w_pd = lv_pmos.lookup('ID_W', GM_ID=gm_id_pd, L=l_pd, VDS=vgs_pd, VSB=0)
# w_pd = i_load / id_w_pd
# w_pd_round = max(round(w_pd*2)/2, 0.5)
# print('PD W =', round(w_pd_round, 2), 'um')