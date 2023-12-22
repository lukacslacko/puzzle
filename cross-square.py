import math

from draw import Draw

d = Draw()

e = math.atan2(1, -2)

a = 0.75
b = 1.5

d.line(2 - b, -1, 2 + a, -1)
d.tab_in(2, -1, 0, e, a, a * 0.3, a * 0.3 / 5)
d.tab_out(2, -1, e, math.pi, b, b * 0.15, b * 0.03)

with open("test.dxf", "w") as f:
    d.dxf(f)

d = Draw()
p, q = d.tab_in(2, -1, 0, e, a, a * 0.3, a * 0.3 / 5)
f, l = d.tab_out(1, 2, e + 0.5 * math.pi, 1.5 * math.pi, b, b * 0.15, b * 0.03)
d.line(*p, 3, -1)
d.line(3, -1, 3, 1)
d.line(3, 1, 1, 1)
d.line(1, 2, *l)
d.line(0, 0, *f)
d.line(0, 0, *q)
with open("test2.dxf", "w") as f:
    d.dxf(f)
