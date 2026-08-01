from pygmid import Lookup as lk
import numpy as np

LV_NMOS = lk('../analog-circuit-design/gmid/sg13_lv_nmos.mat')
LV_PMOS = lk('../analog-circuit-design/gmid/sg13_lv_pmos.mat')

def dB(x):
    return 20 * np.log10(x)

def inv_dB(x):
    return 10 ** (x / 20)

# type: nmos | pmos
# L: in um
# ID: in Ampere
class MOS:
    def __init__(self, name, type, l, gm_id, id, vds_const, vsb):
        self.name = name
        self.type = type
        self.l = l
        self.gm_id = gm_id
        self.gm = gm_id * id
        lv = LV_NMOS if type == 'nmos' else LV_PMOS
        self.vds = 2 / gm_id + vds_const
        self.vgs = lv.look_upVGS(GM_ID=gm_id, L=l, VDS=self.vds, VSB=vsb)
        self.gm_gds = lv.lookup('GM_GDS', GM_ID=gm_id, L=l, VDS=self.vds, VSB=vsb)
        self.gds = self.gm / self.gm_gds
        self.id_w = lv.lookup('ID_W', GM_ID=gm_id, L=l, VDS=self.vds, VSB=vsb)
        self.w = id / self.id_w

    def __str__(self):
        w_rounded = max(round(self.w * 2) / 2, 0.5)
        return f"| {self.name:<6} | L = {self.l:>6}μm | W = {w_rounded:>6}μm | Vgs = {self.vgs:>6.2f}V | gm = {self.gm*1000:>6.3f}mS | rds = {(1/self.gds)/1000:>10.3f}kΩ |"

###### We start with the typical one stage Error Amplifier (once again)
ugbw = 200e3 * (2 * np.pi)
psrr_dc = 65
cc_max = 6.9e-12
vref = 1.2
vout = [2.3, 2.1, 1.6]
A_ea_min = 0
ifb_max = 30e-6 # Maximum current we want to consume in the feedback network
iload = 500e-6
ipd = iload + ifb_max
ibias = 5e-6

# Calculate the feedback b coefficient
bf = []
for v in vout:
    bf.append(vref / v)

# Calculate feedback resistors R1 and R2 such that
# the maximum consumption in the feedback network is ifb_max
r2 = []
r2.append(vref / ifb_max) # corresponds to the smalles resistance
r1 = (1/bf[0] - 1) * r2[0]
for b in bf[1:3]:
    r2.append(r1 / (1/b - 1))
for r in r2:
    print(f'R1 = {r1/1000:>6.3f}kΩ | R2 = {r/1000:>6.3f}kΩ')

###### Pass Device sizing
pd = MOS('PD', 'pmos', 0.13, 5, ipd, 0.4, 0)
A_pd = pd.gm / pd.gds # You should put R2 here but we ignore it for now
print(f'Pass Device Gain A_pd = {A_pd:.3f} = {dB(A_pd):.3f}dB')


###### Based on the paper UBGW = bf * gm,EA / C2
gm_ea_max = ugbw * cc_max / bf[0]
print('Maximum gm of the EA for UGBW =', gm_ea_max)
A_ea_min = np.power(10, 3.25 - np.log10(bf[0]) - np.log10(A_pd))
print(f'Minimum gain of the EA for PSRR = {A_ea_min:.3f} = {dB(A_ea_min):.3f}dB')
rout_ea_min = A_ea_min / gm_ea_max
print(f'Output resistance of EA to achieve such PSRR and gm = {rout_ea_min/1000:.3f}kΩ')

###### Error Amplifier sizing (Basic Differential Pair)
itail = ibias * 2
gm_m12 = gm_ea_max
m1_2 = MOS('M1/2', 'nmos', 10, gm_m12 / (itail / 2), itail / 2, 0.4, 0)
print(f'M1-2 output resistance = {(1/m1_2.gds)/1000:.3f}kΩ')
print('\nThis is why a simple DP would never work. Just compare the output resistance of this transistor to that of the whole EA.\n')

###### Error Amplifier sizing (Telescopic Differential Pair)
itail = ibias * 2
gm_m12 = gm_ea_max
m1_2 = MOS('M1/2', 'nmos', 0.5, gm_m12 / (itail / 2), itail / 2, 0.3, 0)
m1_2c = MOS('M1/2C', 'nmos', 0.5, 15, itail / 2, 0.3, 0)
m3_4 = MOS('M3/4', 'pmos', 0.5, 15, itail / 2, 0.3, 0)
m3_4c = MOS('M3/4C', 'pmos', 0.5, 15, itail / 2, 0.3, 0)
m5 = MOS('M5', 'nmos', 1, 5, 15e-6, 0.4, 0)
m6 = MOS('M6', 'nmos', 1, 5, 5e-6, 0.4, 0)
m7 = MOS('M7', 'nmos', 1, 5, 5e-6, 0.4, 0)
m8 = MOS('M8', 'pmos', 1, 5, 5e-6, 0.4, 0)
m9 = MOS('M9', 'pmos', 1, 5, 5e-6, 0.4, 0)
m10 = MOS('M10', 'nmos', 1, 5, 5e-6, 0.4, 0)

gout_ea = (m3_4c.gds * m3_4.gds) / m3_4c.gm + (m1_2.gds * m1_2c.gds) / m1_2c.gm
print(f'EA output resistance = {(1/gout_ea)/1000:.3f}kΩ')
A_ea = gm_m12 / gout_ea
print(f'EA output voltage gain = {A_ea/1000:.3f}kV/V = {dB(A_ea):.3f}dB')
print(m1_2)
print(m1_2c)
print(m3_4)
print(m3_4c)
print(m5)
print(m6)
print(m7)
print(m8)
print(m9)
print(m10)
print(pd)