import matplotlib as mpl
import schemdraw
import schemdraw.dsp as dsp

# Set global font to Computer Modern (LaTeX standard)
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['mathtext.default'] = 'rm'

with schemdraw.Drawing(file='../pll_diagram.svg') as d:
    d.config(unit=2, lw=1.5, fontsize=12, font='serif')

    dsp.Dot().fill('white').label(r'$f_{REF}$')
    dsp.Arrow().right().length(d.unit/2)
    pfd = dsp.Box(w=d.unit/2, h=d.unit/2).anchor('W').label('PFD')
    
    dsp.Line().right().at(pfd.E, 0, -d.unit/8).length(d.unit/2)
    dsp.Line().right().at(pfd.E, 0, +d.unit/8).length(d.unit/2)

    cp = dsp.Box(w=d.unit/2, h=d.unit/2).anchor('W').at(pfd.E, d.unit/2).label('CP')
    dsp.Line().right().at(cp.E).length(d.unit/2)
    
    lf = dsp.Box(w=d.unit, h=d.unit/2).anchor('W').label('Loop\nFilter')
    
    dsp.Arrow().right().at(lf.E).length(2).label(r'$V_{CTRL}$', loc='top')
    
    vco = dsp.Box(w=d.unit/2, h=d.unit/2).anchor('W').label('VCO')
    
    out_wire = dsp.Line().right().at(vco.E).length(d.unit/2)
    dsp.Dot()
    dsp.Line().right().length(d.unit/2)
    dsp.Dot().fill('white').label(r'$f_{OUT}$', loc='right')
    
    dsp.Line().down().at(out_wire.end).length(d.unit*1.1)

    dsp.Arrow().left().length(d.unit*2)

    div = dsp.Box(w=d.unit, h=d.unit/2).anchor('E').label('Divider\n' + r'$\div N$')
    
    dsp.Line().left().at(div.W).tox(pfd.S)
    dsp.Arrow().up().to(pfd.S)

    vdd1 = dsp.Line().right().at(pfd.N, -d.unit/4, +d.unit/4).length(d.unit/2).label(r'$V_{DD1}$')
    dsp.Wire('-').at(vdd1.center).to(pfd.N)

    vdd2 = dsp.Line().right().at(cp.N, -d.unit/4, +d.unit/4).length(d.unit/2).label(r'$V_{DD2}$')
    dsp.Wire('-').at(vdd2.center).to(cp.N)

    vdd3 = dsp.Line().right().at(lf.N, -d.unit/4, +d.unit/4).length(d.unit/2).label(r'$V_{DD3}$')
    dsp.Wire('-').at(vdd3.center).to(lf.N)

    vdd4 = dsp.Line().right().at(vco.N, -d.unit/4, +d.unit/4).length(d.unit/2).label(r'$V_{DD4}$')
    dsp.Wire('-').at(vdd4.center).to(vco.N)

    vdd5 = dsp.Line().right().at(div.N, -d.unit/4, +d.unit/4).length(d.unit/2).label(r'$V_{DD5}$')
    dsp.Wire('-').at(vdd5.center).to(div.N)

    ldo = dsp.Box(w=d.unit/2, h=d.unit).at(lf.N, 0, +d.unit*0.8).anchor('S').label('LDO')
    dsp.Line().left().length(d.unit/2).at(ldo.W)
    ldo_vdd_line = dsp.Line().up().length(d.unit/4)
    dsp.Line().right().length(d.unit/2).at(ldo_vdd_line.end, -d.unit/4, 0).label(r'$V_{EXT}$')

    dsp.Line().right(d.unit/2).at(ldo.E, 0, 2*d.unit/6)
    dsp.Dot().fill('white').label(r'$V_{DD1}$', loc='right')
    dsp.Line().right(d.unit/2).at(ldo.E, 0, d.unit/6)
    dsp.Dot().fill('white').label(r'$V_{DD2}$', loc='right')
    dsp.Line().right(d.unit/2).at(ldo.E)
    dsp.Dot().fill('white').label(r'$V_{DD3}$', loc='right')
    dsp.Line().right(d.unit/2).at(ldo.E, 0, -d.unit/6)
    dsp.Dot().fill('white').label(r'$V_{DD4}$', loc='right')
    dsp.Line().right(d.unit/2).at(ldo.E, 0, -2*d.unit/6)
    dsp.Dot().fill('white').label(r'$V_{DD5}$', loc='right')