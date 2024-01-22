import svg
import cmath

r = 0.7
rho = 0.15
a = 1.5

A = 1
B = 1j
C = 1-r/cmath.sqrt(2)*(1-1j)
E = A-r
D = 1-r/cmath.sqrt(2)*(1+1j)
G = -E
F = -D

pieces = [
    svg.Path(A).line(C).linear_tab(E,rho,False).linear_tab(D,rho,False).line(A),
    svg.Path(C).line(B).line(F).linear_tab(G,rho).line(E).linear_tab(C,rho),
]

with svg.SVG(0, 1, 300, 300, __file__) as s:
    for i, p in enumerate(pieces):
        s.draw_path(p, svg.COLORS[i], "black", 0.003)
        p.to_dxf(__file__, str(i))