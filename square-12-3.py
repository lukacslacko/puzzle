import math

from draw import Draw, area
import cmath

C = 1j
eps = cmath.exp(cmath.pi * 1j / 4)
B = C * eps
D = C / eps
A = -1
E = B + (A - B) * eps / cmath.sqrt(2)
F = E / eps
G = F / eps
Q = (G + D) / 2
P = (E + B) / 2

z = abs(P - Q)
u = cmath.sqrt(16 * area(0, E, A))
w = 1 / 2 * cmath.sqrt(2 * z**2 - u**2)
alpha = cmath.atan((u / 2 - w) / (u / 2 + w))
print(u, z, w, alpha, alpha * 180 / cmath.pi)
R = P + (Q - P) * cmath.cos(alpha) * cmath.exp(-1j * alpha)

d = Draw()

tabr = 0.14
taba = 0.3 * tabr
tabb = 0.2 * taba

a, b = d.ctab_in(P, R, B, tabr, taba, tabb)
x, y = d.ctab_out(Q, G, R, tabr, taba, tabb)
d.clines([a, R, y])
d.clines([x, G, C, F, B, b])
with open("sq-12-3-a.dxf", "w") as f:
    d.dxf(f)

d = Draw()
a, b = d.ctab_in(P, R, B, tabr, taba, tabb)
x, y = d.ctab_out(P, E, R, tabr, taba, tabb)
d.clines([b, x])
with open("sq-12-3-b.dxf", "w") as f:
    d.dxf(f)

d = Draw()
T = P + 1j * (Q - R)
U = (R + T) / 2 + 1j * (R - T) / 2
F1 = U + (F - U) / 1j
F2 = U + (F1 - U) / 1j
F3 = U + (F2 - U) / 1j

FF = (F + F1) / 2
FF1 = U + (FF - U) / 1j
FF2 = U + (FF1 - U) / 1j
FF3 = U + (FF2 - U) / 1j
BB = FF + (FF - B)
BB1 = U + (BB - U) / 1j
BB2 = U + (BB1 - U) / 1j
BB3 = U + (BB2 - U) / 1j

tabr *= 2
taba *= 1
tabb *= 1

FB, FA = d.ctab_in(F, BB3, FF, tabr, taba, tabb)
FB1, FA1 = d.ctab_in(F1, BB, FF1, tabr, taba, tabb)
FB2, FA2 = d.ctab_in(F2, BB1, FF2, tabr, taba, tabb)
FB3, FA3 = d.ctab_in(F3, BB2, FF3, tabr, taba, tabb, 2 * cmath.pi)

d.clines([FA, FF, BB, FB1])
d.clines([FA1, FF1, BB1, FB2])
d.clines([FA2, FF2, BB2, FB3])
d.clines([FA3, FF3, BB3, FB])
with open("sq-12-3-c.dxf", "w") as f:
    d.dxf(f)

d = Draw()

FY, FX = d.ctab_out(F1, FF, BB, tabr, taba, tabb)

d.clines([FX, BB, FF, FY])
with open("sq-12-3-d.dxf", "w") as f:
    d.dxf(f)

d = Draw()
FB1, FA1 = d.ctab_in(F1, BB, FF1, tabr, taba, tabb)
FY, FX = d.ctab_out(F1, FF, BB, tabr, taba, tabb)
d.clines([FA1, F1, FY])
with open("sq-12-3-e.dxf", "w") as f:
    d.dxf(f)
