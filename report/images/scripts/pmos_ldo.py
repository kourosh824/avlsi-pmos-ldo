import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='../pmos_ldo.svg') as d:
    d.config(unit=2)
    vref = elm.Dot().label(r'$V_{REF}$')
    elm.Line()
    ea = elm.Opamp().anchor('in1').label('EA', loc='center')
    ea_in = elm.Line().left().length(1).at(ea['in2'])
    elm.Line().right().length(5).at(ea.out)
    pd = elm.AnalogPFet(offset_gate=False).anchor('gate').reverse().label('PD', loc='right')

    ea_up = elm.Line().up().at(ea.vd).length(2)
    pd_up = elm.Line().up().at(pd.source).toy(ea_up.end)
    elm.Line().at(ea_up.end).to(pd_up.end).label(r'$V_{EXT}$', loc='top')
    elm.Line().down().length(0.5).at(pd.drain)
    compensation = elm.Dot()

    r1 = elm.Resistor().down().at(compensation.start).label(r'$R_1$', loc='bottom')
    r2 = elm.ResistorVar().down().at(r1.end).label(r'$R_2$', loc='bottom')
    elm.Ground()
    elm.Wire('-|').at(r1.end).to(ea_in.end)

    elm.Line().left().length(0.5).at(compensation.start)
    cc = elm.Capacitor().left().label(r'$C_c$')
    rc = elm.Resistor().left().label(r'$R_c$')
    elm.Line().left().length(0.5)
    elm.Line().up().length(1.3)
    elm.Dot()

    elm.Line().right().length(2).at(compensation.start)
    load = elm.Dot()
    elm.Line().down().length(1)
    cload = elm.Capacitor().down().label(r'$C_L$', loc='bottom')
    elm.Line().down().length(1)
    elm.Ground()

    elm.Line().right().length(2).at(load.start)
    elm.Line().down().length(1)
    iload = elm.SourceI().down().label(r'$I_L$', loc='bottom')
    elm.Line().down().length(1)
    elm.Ground()