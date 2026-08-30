import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='../tel_ota.svg') as d:
    d.config(unit=2)

    M7 = elm.AnalogNFet(offset_gate=False).anchor('gate').label('M7')
    elm.Line().up().length(3).at(M7.drain)
    ibias = elm.SourceI().reverse().label(r'$I_{BIAS}$', loc='top')
    elm.Ground().at(M7.source)
    elm.Dot().at(M7.gate)
    elm.Dot().at(M7.drain)
    elm.Wire('-|').at(M7.drain).to(M7.gate)

    elm.Line().right().length(12).at(M7.gate)
    M5 = elm.AnalogNFet(offset_gate=False).anchor('gate').reverse().label('M5', loc='right')
    elm.Ground().at(M5.source)
    M3c_up = elm.Line().up().length(0.5).at(M5.drain)
    elm.Dot()
    elm.Line().right().length(2)
    elm.Line().up().length(0.25)

    M2 = elm.AnalogNFet(offset_gate=False).anchor('source').theta(0).label('M2')
    elm.Line().up().length(0.25).at(M2.drain)

    M2c = elm.AnalogNFet(offset_gate=False).anchor('source').theta(0).reverse()
    elm.Line().up().length(0.25).at(M2c.drain)
    vout = elm.Dot()
    elm.Line().up().length(0.25)

    M4c = elm.AnalogPFet(offset_gate=False).anchor('drain').theta(0).reverse()
    elm.Line().up().length(0.25).at(M4c.source)

    M4 = elm.AnalogPFet(offset_gate=False).anchor('drain').theta(0).reverse().label('M4', loc='right')
    M4_up = elm.Line().up().length(0.5).at(M4.source)

    elm.Line().left().length(2).at(M3c_up.end)
    elm.Dot()
    elm.Line().up().length(0.25)
    M1 = elm.AnalogNFet(offset_gate=False).anchor('source').theta(0).reverse().label('M1', loc='right')
    elm.Line().up().length(0.25).at(M1.drain)

    M1c = elm.AnalogNFet(offset_gate=False).anchor('source').theta(0)
    M1c_up = elm.Line().up().length(0.5).at(M1c.drain)

    M3c = elm.AnalogPFet(offset_gate=False).anchor('drain').theta(0)
    elm.Line().up().length(0.25).at(M3c.source)

    M3 = elm.AnalogPFet(offset_gate=False).anchor('drain').theta(0).label('M3')
    elm.Line().up().length(0.5).at(M3.source)
    elm.Wire('|-').at(M3.gate, dx=0.25).to(M3c.drain, dy=-0.25)
    elm.Dot().at(M3.gate, dx=0.25)
    elm.Dot().at(M3c.drain, dy=-0.25)
    elm.Wire('-').at(M3.gate).to(M4.gate)

    M8 = elm.AnalogNFet(offset_gate=False).anchor('source').theta(0).at(M1c.source, dx=-4).label('M8')
    elm.Dot().at(M8.gate)
    elm.Dot().at(M8.drain)
    elm.Wire('-|').at(M8.drain).to(M8.gate)
    elm.Wire('-').at(M8.gate).to(M1c.gate)
    elm.Wire('|-').at(M8.source).to(M1.source, dy=-0.25)

    M9 = elm.AnalogPFet(offset_gate=False).anchor('drain').theta(0).at(M3.drain, dx=-4).reverse().label('M9', loc='right')
    elm.Line().up().length(0.5).at(M9.source)

    M10 = elm.AnalogPFet(offset_gate=False).anchor('drain').theta(0).at(M9.drain, dx=-4).label('M10')
    elm.Line().up().length(0.5).at(M10.source)
    elm.Dot().at(M10.gate)
    elm.Wire('|-').at(M10.gate).to(M3c.gate)
    elm.Dot().at((M10.gate.x, M3c.gate.y))
    elm.Wire('|-').at(M10.drain).to((M10.gate.x, M3c.gate.y))
    elm.Dot().at((M10.drain.x, M3c.gate.y))

    M6 = elm.AnalogNFet(offset_gate=False).anchor('drain').theta(0).at((M10.drain.x, M5.drain.y)).reverse()
    elm.Ground().at(M6.source)
    elm.Wire('-').at(M6.drain).to(M10.drain)

    elm.Line().left().length(0.5).at(M1.gate)
    elm.Dot().label(r'$V_{in,p}$')
    elm.Line().right().length(0.5).at(M2.gate)
    elm.Dot().label(r'$V_{in,n}$')

    elm.Wire('-').at(M3c.gate).to(M4c.gate)
    elm.Wire('-').at(M1c.gate).to(M2c.gate)
    elm.Wire('-').at(M10.gate).to(M9.gate)
    elm.Wire('-').at(M9.drain).to(M8.drain)
    elm.Wire('|-').at(ibias.end).to(M4_up.end).label(r'$V_{EXT}$')

    elm.Line().right().length(1.5).at(vout.center)
    elm.Dot().label(r'$V_{OUT}$')

    # elm.Line().right().length(1.5).at(vout.end)
    # elm.Dot().label(r'$V_{OUT}$')