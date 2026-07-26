from pygmid import Lookup as lk
import numpy as np
import math
lv_nmos = lk('../analog-circuit-design/gmid/sg13_lv_nmos.mat')
lv_pmos = lk('../analog-circuit-design/gmid/sg13_lv_pmos.mat')

# For the Error Amplifier
print("-- Error Amplifier Parameters --")
gm_id_m12 = 5
gm_id_m34 = 5
gm_id_m56 = 2
l_12 = 10
l_34 = 8
l_56 = 5
i_bias = 5e-6
i_tail = 10e-6
VDS_m12 = 2 / gm_id_m12 + 0.6
VDS_m34 = 2 / gm_id_m34 + 0.6
VDS_m56 = 2 / gm_id_m56 + 0.4

gm_m12 = gm_id_m12 * i_tail / 2

gm_gds_m12 = lv_nmos.lookup('GM_GDS', GM_ID=gm_id_m12, L=l_12, VDS=VDS_m12, VSB=0)
gm_gds_m34 = lv_pmos.lookup('GM_GDS', GM_ID=gm_id_m34, L=l_34, VDS=VDS_m34, VSB=0)

gds_m12 = gm_m12 / gm_gds_m12
gm_m34 = gm_id_m34 * i_tail/2
gds_m34 = gm_m34 / gm_gds_m34

a0 = gm_m12 / (gds_m12 + gds_m34)
print('A0 =', round(20*np.log10(a0), 1), 'dB')
r_out_dp = 1 / (gds_m12 + gds_m34)
print(f'Rout = {r_out_dp/1000:.3f}kΩ')

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

# For Pass Device
print('\n-- Pass Device Parameters --')
gm_id_pd = 9
l_pd = 0.130
i_pd_max = 504e-6
VDS_pd = 2 / gm_id_pd + 0.6
gm_pd = gm_id_pd * i_pd_max
print(f'gm_pd = {gm_pd*1000}mS')

r2 = [520e3, 640e3, 1.45e6]
v2 = [2.3, 2.1, 1.6]
il = 500e-6
rl = []
ro = []
for i, v in enumerate(r2):
    rl.append(v2[i] / il)

gm_gds_pd = lv_pmos.lookup("GM_GDS", GM_ID=gm_id_pd, L=l_pd, VDS=VDS_pd, VSB=0)
rds_pd = gm_gds_pd / gm_pd
print(f'rds_pd = {rds_pd/1000:.3f}kΩ')

for i, v in enumerate(r2):
    ro.append(1 / (1 / v + 1 / rl[i] + 1 / rds_pd))
    print(f'ro[{i}] = {ro[i]/1000:.3f}kΩ')

ro_min = ro[0]
ro_min_index = 0
for i, v in enumerate(ro):
    if ro_min > v:
        ro_min = v
        ro_min_index = i

print(f'{i}: ro_min = {ro_min/1000:.3f}kΩ')
apd_min = gm_pd * ro_min
print(f'Apd_min = {round(20*np.log10(apd_min), 1)}dB')

vgs_pd = lv_pmos.look_upVGS(GM_ID=gm_id_pd, L=l_pd, VDS=VDS_pd, VSB=0.0)
print('vgs_pd =', round(float(vgs_pd), 3), 'V')

id_w_pd = lv_pmos.lookup('ID_W', GM_ID=gm_id_pd, L=l_pd, VDS=vgs_pd, VSB=0)
w_pd = i_pd_max / id_w_pd
w_pd_round = max(round(w_pd*2)/2, 0.5)
print('PD W =', round(w_pd_round, 2), 'um')

# DP pole frequency after compensation
Cc = 7e-12
fpd = 1 / (2 * math.pi * r_out_dp * Cc * (1 + gm_pd * ro_min))
print('\n-- Compensation --')
print(f'fpd = {fpd/1000:.3f}kHz')


# For the CS stage
print('\n-- CS Parameters --')
gm_id_m8 = 10
gm_id_m7 = 2
l_8 = 5
l_7 = 5
i_cs = 10e-6
VDS_m8 = 2 / gm_id_m8 + 0.6
VDS_m7 = 2 / gm_id_m7 + 0.4

gm_m8 = gm_id_m8 * i_cs
gm_m7 = gm_id_m7 * i_cs
gm_gds_m7 = lv_nmos.lookup("GM_GDS", GM_ID=gm_id_m7, L=l_7, VDS=VDS_m7, VSB=0)
gm_gds_m8 = lv_pmos.lookup("GM_GDS", GM_ID=gm_id_m8, L=l_8, VDS=VDS_m8, VSB=0)
rds_m8 = gm_gds_m8 / gm_m8
rds_m7 = gm_gds_m7 / gm_m7

r_out_cs = (rds_m7 * rds_m8) / (rds_m7 + rds_m8)
acs = gm_m8 * r_out_cs
print('Acs =', round(20*np.log10(acs), 1), 'dB')
print(f'Rout = {r_out_cs:.3f}kΩ')

vgs_m7 = lv_nmos.look_upVGS(GM_ID=gm_id_m7, L=l_7, VDS=VDS_m7, VSB=0.0)
vgs_m8 = lv_pmos.look_upVGS(GM_ID=gm_id_m8, L=l_8, VDS=VDS_m8, VSB=0.0) 
print('vgs_7 =', round(float(vgs_m7), 3), 'V')
print('vgs_8 =', round(float(vgs_m8), 3), 'V')

id_w_m7 = lv_nmos.lookup('ID_W', GM_ID=gm_id_m7, L=l_7, VDS=vgs_m7, VSB=0)
id_w_m8 = lv_pmos.lookup('ID_W', GM_ID=gm_id_m8, L=l_8, VDS=vgs_m8, VSB=0)
w_7 = w_6_round * i_cs / i_bias
w_7_round = max(round(w_7*2)/2, 0.5)
print('M7 W =', round(w_7_round, 2), 'um')
w_8 = i_cs / id_w_m8
w_8_round = max(round(w_8*2)/2, 0.5)
print('M8 W =', round(w_8_round, 2), 'um')