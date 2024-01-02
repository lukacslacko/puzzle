import cmath
import svg
from jigsaw import area, line_intersection, along

eps = cmath.exp(cmath.pi * 1j / 4)
S0 = 1
S1 = S0 * eps
S2 = S1 * eps
S3 = S2 * eps
S4 = S3 * eps
S5 = S4 * eps
S6 = S5 * eps
S7 = S6 * eps

O = 0

X = line_intersection(S0, S3, S1, S6)
Y = X * eps
Z = Y * eps
F = (S1 + X) / 2
G = (S3 + Z) / 2
star_area = 16 * area(0, S0, X)
square_edge_length = cmath.sqrt(star_area)
square_diag = abs(F - G)
# x**2 + (square_edge_length-x)**2 = square_diag**2
# x**2 + square_edge_length**2 - 2*square_edge_length*x + x**2 = square_diag**2
a = 2
b = -2 * square_edge_length
c = square_edge_length**2 - square_diag**2
x = (-b + cmath.sqrt(b**2 - 4 * a * c)) / (2 * a)
print(x, square_edge_length, abs(F - G))
alpha = cmath.acos(x / abs(G - F))
P = F + (G - F) * x / abs(G - F) * cmath.exp(1j * alpha)
Q = along(P, F, abs(Y - F))
R = P + Z - S3

star_simple = svg.Path(P).line(G).line(Z).line(S2).line(Y).line(S1).line(F).line(P)
filler_simple = svg.Path(P).line(Q).line(R).line(P)

hinge = 0.075
tab = 0.031
GZ = along(G, Z, hinge)
GP = along(G, P, hinge)
GS3 = along(G, S3, hinge)
FS1 = along(F, S1, hinge)
FP = along(F, P, hinge)
star_hinge = (
    svg.Path(P)
    .line(GP)
    .circular_tab(G, GZ, GZ, tab, False)
    .line(Z)
    .line(S2)
    .line(Y)
    .line(S1)
    .line(FS1)
    .circular_tab(F, FP, FP, tab, False)
    .line(P)
)
outer_connector = (
    svg.Path(GP)
    .circular_tab(G, GZ, GZ, tab, False)
    .line(GS3)
    .circular_tab(G, GP, GP, tab, False)
)

S = 2 * Q - P
QP = along(Q, P, hinge)
QR = along(Q, R, hinge)
QS = along(Q, S, hinge)

inner_small = svg.Path(R).line(P).line(QP).circular_tab(Q, QR, QR, tab, False).line(R)
inner_connector = (
    svg.Path(QP)
    .circular_tab(Q, QR, QR, tab, False)
    .circular_tab(Q, QS, QS, tab, False)
    .line(QP)
)

with svg.SVG(0, 2.05, 800, 800, __file__) as s:
    with s.transformation(shift=-1 - 1j):
        s.mark_all_caps([globals(), locals()], size=0.06)
        for i in range(4):
            with s.transformation(rotate=90 * i):
                s.draw_path(star_simple, svg.COLORS[i], stroke_width=0.003)
                s.draw_path(filler_simple, svg.COLORS[i + 4], stroke_width=0.003)

    W = (S7 - Z) * (1 - 1j) / 2
    MA = S1 + W + S3 - Z
    MB = S1 + W
    MC = Y + W
    MF = (MA + MB) / 2
    corner_simple = svg.Path(MF).line(MB).line(MC).line(MF)

    with s.transformation(shift=1 - 1j):
        for p in "MA MB MC MF".split():
            s.mark(eval(p), p, "bc", 0.06)
        for i in range(4):
            with s.transformation(rotate=90 * i):
                with s.transformation(shift=W):
                    s.draw_path(star_simple, svg.COLORS[i], stroke_width=0.003)
                s.draw_path(corner_simple, svg.COLORS[i + 4], stroke_width=0.003)

    with s.transformation(shift=1j):
        for i in range(4):
            with s.transformation(rotate=90 * i):
                s.draw_path(star_hinge, svg.COLORS[i], stroke_width=0.003)
                s.draw_path(outer_connector, svg.COLORS[i + 4], stroke_width=0.003)
                s.draw_path(inner_small, svg.COLORS[i+4], stroke_width=0.003)
                s.draw_path(
                    inner_connector, svg.COLORS[(i + 2) % 4], stroke_width=0.003
                )
