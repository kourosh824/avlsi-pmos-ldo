import matplotlib as mpl
import schemdraw
import schemdraw.elements as elm

# Set global font to Computer Modern (LaTeX standard)
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['font.family'] = 'serif'
# pForce the default math text to be Roman (upright) instead of Italic
mpl.rcParams['mathtext.default'] = 'rm'

with schemdraw.Drawing(file='../pmos_ldo_ss.svg') as d:
    d.config(unit=2, lw=1, font='serif')
    gm_ea = elm.SourceControlledI().down().label(r'$g_{m,EA}u_{in}$')
    elm.Ground()

    elm.Line().right().length(2).at(gm_ea.start)
    elm.Dot()
    r1 = elm.Resistor().down().label(r'$R_1$')
    elm.Ground()

    elm.Line().right().length(2).at(r1.start)
    elm.Dot().label(r'$u_1$')
    c1 = elm.Capacitor().down().label(r'$C_1$')
    elm.Ground()

    elm.Line().right().length(0.5).at(c1.start)
    rc = elm.Resistor().right().label(r'$R_c$')
    elm.Capacitor().right().label(r'$C_c$')
    cc = elm.Line().right().length(0.5)

    elm.Dot()
    elm.SourceControlledI().down().label(r'$g_{m,PD}u_1$')
    elm.Ground()

    elm.Line().right().length(2).at(cc.end)
    elm.Dot()
    r2 = elm.Resistor().down().label(r'$R_2$')
    elm.Ground()

    elm.Line().right().length(2).at(r2.start)
    elm.Dot()
    c2 = elm.Capacitor().down().label(r'$C_2$')
    elm.Ground()

    elm.Line().right().length(1).at(c2.start)
    elm.Dot().label(r'$u_{out}$').fill('white')