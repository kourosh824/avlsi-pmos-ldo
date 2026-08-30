import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file="../5t_ota.svg") as d:
    d.config(unit=2)

    Q6 = elm.AnalogNFet(offset_gate=False).anchor('gate').label('M6')
    elm.Line().up().length(2).at(Q6.drain)
    ibias = elm.SourceI().reverse().label(r'$I_{BIAS}$', loc='top')
    elm.Wire('-|').at(Q6.drain).to(Q6.gate)
    elm.Dot().at(Q6.drain)
    elm.Dot().at(Q6.gate)
    elm.Ground().at(Q6.source)

    elm.Line().right().length(3).at(Q6.gate)
    Q5 = elm.AnalogNFet(offset_gate=False).anchor('gate').reverse().label('M5', loc='right')
    elm.Ground().at(Q5.source)
    Q5_up = elm.Line().up().length(0.5).at(Q5.drain)
    elm.Dot()
    elm.Line().right().length(1.5)
    elm.Line().up().length(0.5)
    Q2 = elm.AnalogNFet(offset_gate=False).anchor('source').theta(0).label('M2')
    elm.Line().up().length(0.25).at(Q2.drain)
    vout = elm.Dot()
    elm.Line().up().length(0.25)
    Q4 = elm.AnalogPFet(offset_gate=False).anchor('drain').theta(0).reverse().label('M4', loc='right')
    Q4_up = elm.Line().up().length(0.5).at(Q4.source)

    elm.Line().left().length(1.5).at(Q5_up.end)
    elm.Line().up().length(0.5)
    Q1 = elm.AnalogNFet(offset_gate=False).anchor('source').theta(0).reverse().label('M1', loc='right')
    elm.Line().up().length(0.5).at(Q1.drain)
    Q3 = elm.AnalogPFet(offset_gate=False).anchor('drain').theta(0).label('M3')
    Q3_up = elm.Line().up().length(0.5).at(Q3.source)

    elm.Wire('|-').at(Q3.gate).to(Q3.drain)
    elm.Dot().at(Q3.drain)
    elm.Dot().at(Q3.gate)
    elm.Wire('-').at(Q3.gate).to(Q4.gate)
    elm.Wire('-').at(Q3_up.end).to(Q4_up.end)

    elm.Wire('|-').at(ibias.end).to(Q3_up.end).label(r'$V_{DD}$', loc='end')

    elm.Line().left().length(0.5).at(Q1.gate)
    elm.Dot().label(r'$V_{in,p}$')
    elm.Line().right().length(0.5).at(Q2.gate)
    elm.Dot().label(r'$V_{in,n}$')

    elm.Line().right().length(1.5).at(vout.end)
    elm.Dot().label(r'$V_{OUT}$')