import svg
from jigsaw import along

A = 1 + 1j
B = 1 + 3j
C = -1 + 3j
D = -1 + 1j
E = -3 + 1j
F = -3 - 1j
G = -1 - 1j
P = (A + B) / 2
Q = (E + D) / 2
O = 0
PB = along(P, B, 0.5)
PO = along(P, O, 0.5)
POA = along(P, O, 1.5)
QO = along(Q, O, 0.5)
PA = along(P, A, 1.5)
QD = along(Q, D, 1.5)

QOD = along(Q, O, 1.5)


tab_radius = 0.15

hinge = (
    svg.Path(PB)
    .circular_tab(P, PO, PO, tab_radius, True)
    .line(POA)
    .circular_tab(P, PA, PA, tab_radius, False)
    .line(PB)
)

piece = (
    svg.Path(O)
    .line(QOD)
    .circular_tab(Q, QD, QD, tab_radius, False)
    .line(D)
    .line(C)
    .line(B)
    .line(PB)
    .circular_tab(P, PO, PO, tab_radius, True)
    .line(O)
)

MA = 2+.5j
MB = 2-.5j
MC = 2-1j
MD = 3+1j
ME = 1-3j
MF = along(MC, ME, .5)
MG = along(MC, MD, 1.5)

mirror_hinge = svg.Path(MG).circular_tab(MC,MA,MA,tab_radius,False).line(MB).circular_tab(MC,MF,MF,tab_radius,True).line(MG)

with svg.SVG(0, 4, 800, 500, __file__) as s:
    with s.transformation(shift=-3, rotate=45):
        for i in range(4):
            with s.transformation(rotate=90*i):
                s.draw_path(hinge, svg.COLORS[2*i])
                s.draw_path(piece, svg.COLORS[2*i+1])


    with s.transformation(shift=3, rotate=0):
        for i in range(4):
            with s.transformation(rotate=90*i):
                s.draw_path(mirror_hinge, svg.COLORS[2*i])
                with s.transformation(shift=-C):
                    s.draw_path(piece, svg.COLORS[(2*i+7)%8])
    