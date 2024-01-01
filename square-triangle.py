import cmath
import svg
from jigsaw import along, line_intersection

A = 1 - 1j
B = 1 + 1j
C = -1 + 1j
D = -1 - 1j

# Triangle area = triangle_edge * (sqrt(3)/2 * triangle_edge) / 2
# Triangle edge = sqrt(4 * triangle_area / sqrt(3))
triangle_edge = cmath.sqrt(16 / cmath.sqrt(3))
x = cmath.sqrt(triangle_edge**2 / 4 - 1)

P = 1
Q = B - x
R = P + cmath.exp(cmath.pi * 1j / 3) * (Q - P)

T = -1

S = line_intersection(T, R, A, D)

hinge_size = 0.6

QB = along(Q, B, hinge_size)
QR = along(Q, R, hinge_size)
QC = along(Q, C, hinge_size)
TC = along(T, C, hinge_size)
TR = along(T, R, hinge_size)
TD = along(T, D, hinge_size)
SD = along(S, D, hinge_size)
SR = along(S, R, hinge_size)
SA = along(S, A, hinge_size)
PA = along(P, A, hinge_size)
PR = along(P, R, hinge_size)
PB = along(P, B, hinge_size)

piece_1 = svg.Path(A)
piece_1.line(P)
piece_1.line(R)
piece_1.line(S)
piece_1.line(A)

piece_2 = svg.Path(P)
piece_2.line(B)
piece_2.line(Q)
piece_2.line(R)
piece_2.line(P)

piece_3 = svg.Path(Q)
piece_3.line(C)
piece_3.line(T)
piece_3.line(R)
piece_3.line(Q)

piece_4 = svg.Path(T)
piece_4.line(D)
piece_4.line(S)
piece_4.line(T)

svg.Path.default_linear_tab_left = True
svg.Path.default_linear_tab_radius = 0.1
hinged_pieces = [
    svg.Path(B).line(QB).linear_tab(QR).line(R).line(PR).linear_tab(PB).line(B),
    svg.Path(C).line(TC).linear_tab(TR).line(R).line(QR).linear_tab(QC).line(C),
    svg.Path(D).line(SD).linear_tab(SR).line(TR).linear_tab(TD).line(D),
    svg.Path(A).line(PA).linear_tab(PR).line(R).line(SR).linear_tab(SA).line(A),
]
hinges = [
    
]

with svg.SVG(0, 3, 700, 700, __file__) as s:
    with s.transformation(shift=-1.5-1j, rotate=0):
        for i, piece in enumerate([piece_1, piece_2, piece_3, piece_4]):
            s.draw_path(piece, svg.COLORS[i])

        s.mark_all_caps([globals(), locals()])

    with s.transformation(shift=0.5, rotate=0):
        s.draw_path(piece_1, svg.COLORS[0])
        with s.transformation(shift=P, rotate=180), s.transformation(shift=-P):
            s.draw_path(piece_2, svg.COLORS[1])
        with s.transformation(shift=S, rotate=180), s.transformation(shift=-S):
            s.draw_path(piece_4, svg.COLORS[3])
        with s.transformation(shift=P, rotate=180), s.transformation(
            shift=-P
        ), s.transformation(shift=Q, rotate=180), s.transformation(shift=-Q):
            s.draw_path(piece_3, svg.COLORS[2])

    with s.transformation(shift=-1.5+1.5j):
        for i, piece in enumerate(hinged_pieces):
            s.draw_path(piece, svg.COLORS[i])