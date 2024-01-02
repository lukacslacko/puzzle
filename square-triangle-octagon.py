import cmath
import svg
from jigsaw import along, line_intersection


octagon_edge = 1
octagon_height = cmath.tan(3 * cmath.pi / 8)
octagon_area = octagon_edge * octagon_height * 2
square_edge = cmath.sqrt(octagon_area)
square_diag = 1 + cmath.sqrt(2) / 2
# (square_edge - x) ** 2 + x ** 2 = square_diag ** 2
# square_edge ** 2 - 2 * square_edge * x + x ** 2 + x ** 2 = square_diag ** 2
# 2 * x ** 2 - 2 * square_edge * x + square_edge ** 2 - square_diag ** 2 = 0
a = 2
b = -2 * square_edge
c = square_edge**2 - square_diag**2
z = (-b - cmath.sqrt(b**2 - 4 * a * c)) / (2 * a)

z *= 2 / square_edge

A = -1 - 1j
B = 1j * A
C = 1j * B
D = 1j * C

OP = along(A, B, z)
OQ = along(D, A, z)
OT = along(OP, OP + (1 - 1j) * (OQ - OP), 1 / square_edge)
OU = OT + 2 * (OQ - OP) / abs(OQ - OP) / square_edge
OW = OT * 1j

octa_piece = svg.Path(A).line(OP).line(OT).line(OU).line(OQ).line(A)


triangle_edge = cmath.sqrt(4 / cmath.sqrt(3))
triangle_height = triangle_edge * cmath.sqrt(3) / 2

x = (triangle_height - 1) / 2
y = (1 - triangle_edge / 2) / 2

P = A + 2j * y
R = A + 4j * y
Q = C - 2j * y
S = C - 4j * y
T = R + 2 * x
U = S - 2 * x
W = U - Q
V = -W

IX = line_intersection(OT, OW, W, B)
IY = line_intersection(OT, OU, P, Q)
IZ = -IY
OR = OP * 1j

large_hinge = 0.2

OP_A = along(OP, A, large_hinge)
OP_B = along(OP, B, large_hinge)
OP_OT = along(OP, OT, large_hinge)

OR_B = along(OR, B, large_hinge)
OR_OW = along(OR, OW, large_hinge)
OR_S = along(OR, S, large_hinge)

IX_B = along(IX, B, large_hinge)
IX_W = along(IX, W, large_hinge)
IX_OT = along(IX, OT, large_hinge)
IX_OW = along(IX, OW, large_hinge)

OQ_R = along(OQ, R, large_hinge)
OQ_OU = along(OQ, OU, large_hinge)


small_hinge = 0.13

T_P = along(T, P, small_hinge)
T_R = along(T, R, small_hinge)
T_IY = along(T, IY, small_hinge)
P_A = along(P, A, small_hinge)
P_T = along(P, T, small_hinge)
P_R = along(P, R, small_hinge)

U_IZ = along(U, IZ, small_hinge)
U_S = along(U, S, small_hinge)
U_Q = along(U, Q, small_hinge)
Q_C = along(Q, C, small_hinge)
Q_U = along(Q, U, small_hinge)
Q_S = along(Q, S, small_hinge)

large_tab = 0.05
small_tab = 0.025

hinge_pieces = [
    svg.Path(A)
    .line(P_A)
    .circular_tab(P, P_T, A, large_tab, False)
    .line(IY)
    .line(OT)
    .line(OP_OT)
    .circular_tab(OP, OP_A, OP_A, large_tab, True)
    .line(A),
    svg.Path(OP_A)
    .line(OP_B)
    .circular_tab(OP, OP_OT, OP_OT, large_tab, False)
    .circular_tab(OP, OP_A, OP_A, large_tab, True),
    svg.Path(B)
    .line(OP_B)
    .circular_tab(OP, OP_OT, OP_OT, large_tab, False)
    .line(OT)
    .line(IX_OT)
    .circular_tab(IX, IX_B, IX_B, large_tab, False)
    .line(B),
    svg.Path(B)
    .line(IX_B)
    .circular_tab(IX, IX_OW, IX_OW, large_tab, False)
    .line(OW)
    .line(OR_OW)
    .circular_tab(OR, OR_B, OR_B, large_tab, True)
    .line(B),
    svg.Path(IX_W)
    .circular_tab(IX, IX_OT, IX_OT, large_tab, False)
    .circular_tab(IX, IX_B, IX_B, large_tab, False)
    .line(IX_W),
    svg.Path(IX_W)
    .line(IX_B)
    .circular_tab(IX, IX_OW, IX_OW, large_tab, False)
    .circular_tab(IX, IX_W, IX_W, large_tab, False),
    svg.Path(OR_B)
    .line(OR_S)
    .circular_tab(OR, OR_OW, OR_OW, large_tab, False)
    .circular_tab(OR, OR_B, OR_B, large_tab, True),
    svg.Path(P_R)
    .line(P_A)
    .circular_tab(P, P_T, P_T, large_tab, False)
    .circular_tab(P, P_R, P_R, small_tab, False),
    svg.Path(OT)
    .line(IY)
    .line(W)
    .line(IX_W)
    .circular_tab(IX, IX_OT, IX_OT, large_tab, False)
    .line(OT),
    svg.Path(W)
    .line(IZ)
    .line(OW)
    .line(IX_OW)
    .circular_tab(IX, IX_W, IX_W, large_tab, False)
    .line(W),
    svg.Path(T_P)
    .line(T_IY)
    .circular_tab(T, T_R, T_R, large_tab, False)
    .circular_tab(T, T_P, T_P, small_tab, False)
    .line(T_P),
    svg.Path(S)
    .linear_tab(U_S, small_tab, True)
    .circular_tab(U, U_Q, U_Q, small_tab, False)
    .line(Q_U)
    .circular_tab(Q, Q_S, Q_S, small_tab, False)
    .line(S),
    svg.Path(R)
    .linear_tab(T_R, small_tab, False)
    .circular_tab(T, T_P, T_P, small_tab, False)
    .line(P_T)
    .circular_tab(P, P_R, P_R, small_tab, False)
    .line(R),
    svg.Path(OW)
    .line(IZ)
    .line(U_IZ)
    .circular_tab(U, U_S, U_S, large_tab, False)
    .linear_tab(S, small_tab, False)
    .line(OR_S)
    .circular_tab(OR, OR_OW, OR_OW, large_tab, False)
    .line(OW),
    svg.Path(R)
    .line(OQ_R)
    .circular_tab(OQ, OQ_OU, OQ_OU, large_tab, False)
    .line(OU)
    .line(IY)
    .line(T_IY)
    .circular_tab(T, T_R, T_R, large_tab, False)
    .linear_tab(R, small_tab, True),
]


pieces = [
    svg.Path(A).line(B).line(W).line(T).line(P).line(A),
    svg.Path(B).line(S).line(U).line(W).line(B),
    svg.Path(C).line(D).line(V).line(U).line(Q).line(C),
    svg.Path(D).line(R).line(T).line(V).line(D),
    svg.Path(P).line(T).line(R).line(P),
    svg.Path(S).line(Q).line(U).line(S),
]

tri_pieces = [
    svg.Path(A + V).line(B + V).line(W + V).line(T + V).line(P + V).line(A + V),
    svg.Path(B + V).line(S + V).line(U + V).line(W + V).line(B + V),
    svg.Path(C + W).line(D + W).line(V + W).line(U + W).line(Q + W).line(C + W),
    svg.Path(D + W).line(R + W).line(T + W).line(V + W).line(D + W),
    svg.Path(T).line(A + V).line(T + W).line(T),
    svg.Path(U).line(C + W).line(U + V).line(U),
]


def f(p):
    return -p.real - (-p.imag - triangle_edge) * 1j


real_tri_pieces = [
    svg.Path(f(A + V))
    .line(f(B + V))
    .line(f(W + V))
    .line(f(T + V))
    .line(f(P + V))
    .line(f(A + V)),
    svg.Path(B + V).line(S + V).line(U + V).line(W + V).line(B + V),
    svg.Path(C + W).line(D + W).line(V + W).line(U + W).line(Q + W).line(C + W),
    svg.Path(f(D + W)).line(f(R + W)).line(f(T + W)).line(f(V + W)).line(f(D + W)),
    svg.Path(f(T)).line(f(A + V)).line(f(T + W)).line(f(T)),
    svg.Path(U).line(C + W).line(U + V).line(U),
]

with svg.SVG(0, 3.5, 700, 700, __file__) as s:
    with s.transformation(shift=-1.5 - 1j):
        s.mark_all_caps([globals(), locals()], size=0.1)
        for i, piece in enumerate(pieces):
            s.draw_path(piece, svg.COLORS[i])

    with s.transformation(shift=1.5 - 1j):
        for i, piece in enumerate(tri_pieces):
            s.draw_path(piece, svg.COLORS[i])

    with s.transformation(shift=1.5 + 1j):
        for i, piece in enumerate(real_tri_pieces):
            s.draw_path(piece, svg.COLORS[i])

    with s.transformation(shift=-1.5 + 1.5j):
        for i, piece in enumerate(pieces):
            s.draw_path(piece, "transparent")
        for i in range(4):
            with s.transformation(rotate=90 * i):
                s.draw_path(octa_piece, "transparent")

for helpers, suffix in [(True, "-b"), (False, "-c")]:
    with svg.SVG(0, 1.2, 900, 900, __file__, suffix) as s:
        if helpers:
            s.mark_all_caps([globals(), locals()], 0.04)
            for i, piece in enumerate(pieces):
                s.draw_path(piece, "transparent", stroke_width=0.005)
            for i in range(4):
                with s.transformation(rotate=90 * i):
                    s.draw_path(octa_piece, "transparent", stroke_width=0.005)
        special = hinge_pieces[-4:]
        regular = hinge_pieces[:-4]
        all_pieces = (
            [(p, 0) for p in regular]
            + [(p, 180) for p in regular]
            + [(p, 0) for p in special]
        )
        for i, piece_and_rotation in enumerate(all_pieces):
            piece, rotation = piece_and_rotation
            with s.transformation(rotate=rotation):
                s.draw_path(
                    piece,
                    f"rgba({(i*73)%256},{(128+i*i*101+11*i*i*i)%256},{(99+53*i+i*i*i*77)%256},{0.9 if helpers else 1})",
                    stroke_width=0.005,
                )
