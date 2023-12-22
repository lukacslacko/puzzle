import math

from draw import Draw

a = 2 * math.sin(math.pi * 22.5 / 180) / math.sqrt(2)

cx = -a * math.sin(math.pi * 22.5 / 180)
cy = -1 + a * math.cos(math.pi * 22.5 / 180)

dx = cy
dy = -cx

hhx = (1 + math.sqrt(2)) / 2 * -a * math.sin(math.pi * 22.5 / 180)
hhy = -1 + (1 + math.sqrt(2)) / 2 * a * math.cos(math.pi * 22.5 / 180)

gx = (1 + math.sqrt(2)) / 2 * -a * math.sin(math.pi * 22.5 / 180)
gy = -1 + (1 + math.sqrt(2)) / 2 * a * math.cos(math.pi * 22.5 / 180)

hx = hhx - (hhy - cy)
hy = hhy + (hhx - cx)

d = Draw()

r = 0.4
ts = 0.27
f, _ = d.tab_in(0, -1, 0, math.pi * 112.5 / 180, r, r * ts, r * ts / 4)
_, l = d.tab_in(0, -1, math.pi * 112.5 / 180, math.pi, r, r * ts, r * ts / 4)
d.line(*f, *l)

with open("4--8-2-a.dxf", "w") as f:
    d.dxf(f)

d = Draw()
f, l = d.tab_in(0, -1, math.pi * 112.5 / 180, math.pi, r, r * ts, r * ts / 4)
d.line(-1, -1, *l)
c, g = d.arc(
    hx,
    hy,
    a * (math.sqrt(2) - 1) / 2 * math.sqrt(2),
    math.pi * (90 + 22.5 + 90 - 135) / 180,
    math.pi * (90 + 22.5 + 90 + 135) / 180,
)
d.line(*c, *f)
d.line(*g, dx, dy)

u, v = d.tab_in(-1, 0, -math.pi / 2, math.pi * 22.5 / 180, r, r * ts, r * ts / 4)

d.line(dx, dy, *v)
d.line(*u, -1, -1)

with open("4--8-2-b.dxf", "w") as f:
    d.dxf(f)

d = Draw()
c, g = d.arc(
    hx,
    hy,
    a * (math.sqrt(2) - 1) / 2 * math.sqrt(2),
    math.pi * (90 + 22.5 + 90 - 135) / 180,
    math.pi * (90 + 22.5 + 90 + 135) / 180,
)
d.line(0, 0, *g)
d.line(*c, dx, dy)
d.line(dx, dy, 0, 0)

with open("4--8-2-c.dxf", "w") as f:
    d.dxf(f)
