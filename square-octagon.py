import cmath
import svg
from jigsaw import along

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
x = (-b - cmath.sqrt(b**2 - 4 * a * c)) / (2 * a)

A = (1 + 1j) * square_edge / 2
B = A * 1j
C = -A
D = -B

P = along(A, B, x)
Q = along(D, A, x)
T = along(P, P + (1 - 1j) * (Q - P), 0.5)
U = T + (Q - P) / abs(Q - P)

print(abs(U - T), abs(T - P), abs(U - Q), abs(Q - P))


def octa_piece(plain: bool = False) -> tuple[svg.Path, svg.Path, svg.Path]:
    if plain:
        p = svg.Path(A)
        p.line(P)
        p.line(T)
        p.line(U)
        p.line(Q)
        p.line(A)
        return p, None, None

    PA = along(P, A, abs(P - T))
    QA = along(Q, A, abs(P - T))
    p = svg.Path(A)
    p.line(PA)
    p.linear_tab(T, 0.15, left=True)
    p.line(U)
    p.linear_tab(QA, 0.15, left=True)
    p.line(A)

    PB = along(P, A, -abs(P - T))
    q = svg.Path(PA)
    q.linear_tab(T, 0.15, left=True)
    q.linear_tab(PB, 0.15, left=True)
    q.line(PA)

    W = (PA + PB) / 2
    WT = 2 * W - T

    r = svg.Path(PA)
    r.linear_tab(T, 0.15, left=True)
    r.line(WT)
    r.linear_tab(PA, 0.15, left=True)

    return p, q, r


with svg.SVG(0, 4, 700, 700, __file__) as s:
    plain, hinge, mirror_hinge = octa_piece(True)
    puzzle, hinge, mirror_hinge = octa_piece(False)
    for piece, y in [(plain, -1.6j), (puzzle, 1.6j)]:
        with s.transformation(shift=y):
            with s.transformation(shift=-1.5):
                for i in range(4):
                    with s.transformation(rotate=90 * i):
                        s.draw_path(piece, svg.COLORS[i])
                        if piece == puzzle:
                            s.draw_path(hinge, svg.COLORS[i + 4])

            with s.transformation(shift=1.5):
                with s.transformation(shift=-P - Q, rotate=0):
                    s.draw_path(piece, svg.COLORS[0])
                with s.transformation(shift=-P + Q, rotate=90):
                    s.draw_path(piece, svg.COLORS[1])
                with s.transformation(shift=P + Q, rotate=180):
                    s.draw_path(piece, svg.COLORS[2])
                with s.transformation(shift=P - Q, rotate=270):
                    s.draw_path(piece, svg.COLORS[3])
                if piece == puzzle:
                    for i in range(4):
                        with s.transformation(shift=0, rotate=90 * i + 90):
                            with s.transformation(shift=-P - Q, rotate=0):
                                s.draw_path(mirror_hinge, svg.COLORS[i + 4])
