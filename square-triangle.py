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

pieces = [
    svg.Path(B).line(Q).line(R).line(P).line(B),
    svg.Path(C).line(T).line(R).line(Q).line(C),
    svg.Path(D).line(S).line(T).line(D),
    svg.Path(A).line(P).line(R).line(S).line(A),
]

W = 2 * (P - Q)

tri_pieces = [
    svg.Path(A).line(2 * P - Q).line(2 * P - R).line(P).line(A),
    svg.Path(Q + W).line(R + W).line(T + W).line(C + W).line(Q + W),
    svg.Path(S).line(2 * S - T).line(2 * S - D).line(S),
    svg.Path(A).line(P).line(R).line(S).line(A),
]

svg.Path.default_linear_tab_left = True
svg.Path.default_linear_tab_radius = 0.1
hinged_pieces = [
    svg.Path(B).line(QB).linear_tab(QR).line(R).line(PR).linear_tab(PB).line(B),
    svg.Path(C).line(TC).linear_tab(TR).line(R).line(QR).linear_tab(QC).line(C),
    svg.Path(D).line(SD).linear_tab(SR).line(TR).linear_tab(TD).line(D),
    svg.Path(A).line(PA).linear_tab(PR).line(R).line(SR).linear_tab(SA).line(A),
]
hinges = [
    svg.Path(QB).linear_tab(QR).linear_tab(QC).line(QB),
    svg.Path(TC).linear_tab(TR).linear_tab(TD).line(TC),
    svg.Path(SD).linear_tab(SR).linear_tab(SA).line(SD),
    svg.Path(PA).linear_tab(PR).linear_tab(PB).line(PA),
]

svg.Path.default_linear_tab_left = False
tri_hinged_pieces = [
    svg.Path(A)
    .line(PA)
    .linear_tab(2 * P - PR)
    .line(2 * P - R)
    .line(2 * P - QR)
    .linear_tab(2 * P - QB)
    .line(A),
    svg.Path(C + W)
    .line(TC + W)
    .linear_tab(TR + W)
    .line(R + W)
    .line(QR + W)
    .linear_tab(QC + W)
    .line(C + W),
    svg.Path(2 * S - D)
    .line(2 * S - TD)
    .linear_tab(2 * S - TR)
    .line(2 * S - SR)
    .linear_tab(2 * S - SD)
    .line(2 * S - D),
    svg.Path(A).line(SA).linear_tab(SR).line(R).line(PR).linear_tab(PA).line(A),
]
tri_hinges = [
    svg.Path(2 * P - QB).linear_tab(QR + W).line(2 * P - QR).linear_tab(2 * P - QB),
    svg.Path(TR + W).linear_tab(TC + W).linear_tab(2 * S - TR).line(TR + W),
    svg.Path(SA).linear_tab(SR).line(2 * S - SR).linear_tab(SA),
    svg.Path(PA).linear_tab(2 * P - PR).line(PR).linear_tab(PA),
]

with svg.SVG(0, 3, 700, 700, __file__) as s:
    with s.transformation(shift=-1.5 - 1.25j, rotate=0):
        for i, piece in enumerate(pieces):
            s.draw_path(piece, svg.COLORS[i])

        # s.mark_all_caps([globals(), locals()])

    with s.transformation(shift=0.5 - 0.5j, rotate=0):
        for i, piece in enumerate(tri_pieces):
            s.draw_path(piece, svg.COLORS[i])

    with s.transformation(shift=-1.5 + 1.7j):
        for i, piece in enumerate(hinged_pieces):
            s.draw_path(piece, svg.COLORS[i])
        for i, hinge in enumerate(hinges):
            s.draw_path(hinge, svg.COLORS[i + 4])

    with s.transformation(shift=0.5 + 2.5j):
        for i, piece in enumerate(tri_hinged_pieces):
            s.draw_path(piece, svg.COLORS[i])
        for i, hinge in enumerate(tri_hinges):
            s.draw_path(hinge, svg.COLORS[i + 4])
