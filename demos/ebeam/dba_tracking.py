__author__ = 'Sergey Tomin'

from ocelot.cpbd.match import *
from ocelot.gui.accelerator import *

Q1 = Quadrupole(l= 0.4, k1=-1.3, id = "Q1")
Q2 = Quadrupole(l= 0.8, k1=1.4, id = "Q2")
Q3 = Quadrupole(l= 0.4, k1=-1.7, id = "Q3")
Q4 = Quadrupole(l= 0.5, k1=1.19250444829 , id = "Q4")

B  = Bend(l=2.7, k1=-.06, angle=2*pi/16., e1=pi/16., e2=pi/16., id = "B")

SF = Sextupole(l=0., ms = 1.5, id = "SF") #random value
SD = Sextupole(l=0., ms = -1.5, id = "SD") #random value

D1 = Drift(l=2., id = "D1")
D2 = Drift(l=0.6, id = "D2")
D3 = Drift(l=0.3, id = "D3")
D4 = Drift(l=0.7, id = "D4")
D5 = Drift(l=0.9, id = "D5")
D6 = Drift(l=0.2, id = "D6")


cell = (D1, Q1, D2, Q2, D3, Q3, D4, B, D5, SD, D5, SF, D6, Q4, D6, SF, D5, SD,D5, B, D4, Q3, D3, Q2, D2, Q1, D1)


lat = MagneticLattice(cell)

tw0 = Twiss()
tw0.x = 0.1
tw0.y = 0.2
tws=twiss(lat, tw0, nPoints=1000)
print( "start: Dx = ", tws[0].Dx, " Dxp = ", tws[0].Dxp)
print("end:   Dx = ", tws[-1].Dx, " Dxp = ", tws[-1].Dxp)
plot_opt_func(lat, tws,top_plot = ["x", "y"])
plt.show()

# Single particle tracking with transverse shift

p1 = Particle(x = 0.1, y = 0.2)

navi = Navigator()
dz = 0.01
P1 = []
for i in range(int(lat.totalLen/dz)):
    step(lat, [p1], dz = dz, navi = navi)
    P1.append(copy(p1))

s = [f.s for f in P1]#map(lambda f: f.s, P1)
x = [f.x for f in P1]#map(lambda f: f.x, P1)
y = [f.y for f in P1] #map(lambda f: f.y, P1)

font = {'size'   : 10}
matplotlib.rc('font', **font)

plt.plot(s, x, "r", label = "X")
plt.plot(s, y, "b", label = "Y")

plt.title("Single particle tracking with transverse shift")
plt.legend()
plt.xlabel("S, m")
plt.ylabel("X/Y, m")
plt.grid(True)
plt.show()

# Single particle tracking with energy shift
p1 = Particle(p = -0.001)
p2 = Particle(p = 0.001)

navi = Navigator()
dz = 0.01
P1 = []
P2 = []
for i in range(int(lat.totalLen/dz)):
    step(lat, [p1, p2], dz = dz, navi = navi)
    P1.append(copy(p1))
    P2.append(copy(p2))

s = [f.s for f in P1]#map(lambda f: f.s, P1)
x = [f.x for f in P1]#map(lambda f: f.x, P1)
y = [f.y for f in P1]#map(lambda f: f.y, P1)
tau = [f.tau for f in P1]# map(lambda f: f.tau, P1)
#s = map(lambda f: f.s, P1)
x2 = [f.x for f in P2]#map(lambda f: f.x, P2)
y2 = [f.y for f in P2]#map(lambda f: f.y, P2)
tau2 = [f.tau for f in P2]#map(lambda f: f.tau, P1)



plt.subplot(311)
plt.plot(s, x, "r", label = "x1")
plt.plot(s, x2, "b", label = "x2")
plt.xlabel("S, m")
plt.ylabel("x1/x2, m")
plt.legend()

plt.subplot(312)
plt.plot(s, y, "r", label = "y1")
plt.plot(s, y2, "b", label = "y2")

plt.legend()
plt.xlabel("S, m")
plt.ylabel("y1/y2, m")

plt.subplot(313)
plt.plot(s, tau, "r", label = "tau1")
plt.plot(s, tau2, "b", label = "tau2")

plt.legend()
plt.xlabel("S, m")
plt.ylabel("tau1/tau2, m")

plt.grid(True)

plt.show()