import matplotlib as mpl
import schemdraw
import schemdraw.elements as elm

# Set global font to Computer Modern (LaTeX standard)
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['font.family'] = 'serif'
# pForce the default math text to be Roman (upright) instead of Italic
mpl.rcParams['mathtext.default'] = 'rm'

with schemdraw.Drawing(file='../cm_ota.svg') as d:
    d.config(unit=2, lw=1, font='serif')
    Q6 = elm.AnalogNFet(offset_gate=False).anchor('gate').label('M6')
    elm.Line().up().length(2).at(Q6.drain)
    ibias = elm.SourceI().reverse().label(r'$I_{BIAS}$', loc='top')
    elm.Wire('-|').at(Q6.drain).to(Q6.gate)
    elm.Dot().at(Q6.drain)
    elm.Dot().at(Q6.gate)
    elm.Ground().at(Q6.source)

    elm.Line().right().length(6).at(Q6.gate)
    Q5 = elm.AnalogNFet(offset_gate=False).anchor('gate').reverse().label('M5', loc='right')
    elm.Ground().at(Q5.source)
    Q5_up = elm.Line().up().length(0.5).at(Q5.drain)
    elm.Dot()
    elm.Line().right().length(1.5)
    elm.Line().up().length(0.5)
    Q2 = elm.AnalogNFet(offset_gate=False).anchor('source').theta(0).label('M2')
    elm.Line().up().length(0.5).at(Q2.drain)
    Q4 = elm.AnalogPFet(offset_gate=False).anchor('drain').theta(0).label('M4', loc='left')
    elm.Line().up().length(0.5).at(Q4.source)

    elm.Line().left().length(1.5).at(Q5_up.end)
    elm.Line().up().length(0.5)
    Q1 = elm.AnalogNFet(offset_gate=False).anchor('source').theta(0).reverse().label('M1', loc='right')
    elm.Line().up().length(0.5).at(Q1.drain)
    Q3 = elm.AnalogPFet(offset_gate=False).anchor('drain').theta(0).reverse().label('M3', loc='right')
    elm.Line().up().length(0.5).at(Q3.source)

    elm.Line().left().length(1.5).at(Q3.gate)
    Q7 = elm.AnalogPFet(offset_gate=False).anchor('gate').theta(0).label('M7')
    elm.Line().up().length(0.5).at(Q7.source)
    elm.Line().down().length(6).at(Q7.drain)

    Q9 = elm.AnalogNFet(offset_gate=False).anchor('drain').theta(0).label('M9')
    elm.Dot().at(Q9.drain)
    elm.Dot().at(Q9.gate)
    elm.Wire('-|').at(Q9.drain).to(Q9.gate)
    elm.Ground().at(Q9.source)

    elm.Line().right(1.5).at(Q4.gate)
    Q8 = elm.AnalogPFet(offset_gate=False).anchor('gate').theta(0).reverse().label('M8', loc='right')
    Q8_up = elm.Line().up(0.5).at(Q8.source)
    elm.Line().down(3).at(Q8.drain)
    vout = elm.Dot()
    elm.Line().down(3)

    Q10 = elm.AnalogNFet(offset_gate=False).anchor('drain').theta(0).reverse().label('M10', loc='right')
    elm.Ground().at(Q10.source)
    elm.Wire('-').at(Q10.gate).to(Q9.gate)

    elm.Wire('-').at(ibias.end).to((ibias.end.x, Q8_up.end.y))
    elm.Wire('-').at((ibias.end.x, Q8_up.end.y), -0.5).to(Q8_up.end, 0.5).label(r'$V_{EXT}$', loc='top').linewidth(3)

    elm.Dot().at(Q3.drain)
    elm.Dot().at(Q3.gate)
    elm.Dot().at(Q4.drain)
    elm.Dot().at(Q4.gate)
    elm.Wire('-|').at(Q3.drain).to(Q3.gate)
    elm.Wire('-|').at(Q4.drain).to(Q4.gate)
    elm.Line().left().length(0.5).at(Q1.gate)
    elm.Dot().label(r'$V_{in,p}$').fill('white')
    elm.Line().right().length(0.5).at(Q2.gate)
    elm.Dot().label(r'$V_{in,n}$').fill('white')

    elm.Line().right().length(1.5).at(vout.end)
    elm.Dot().label(r'$V_{OUT}$').fill('white')