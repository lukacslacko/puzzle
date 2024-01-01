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


def octa_piece(plain: bool = False) -> svg.Path:
    if plain:
        p = svg.Path(A)
        p.line(P)
        p.line(T)
        p.line(U)
        p.line(Q)
        p.line(A)
        return p


with svg.SVG(0, 2, 700, 300, __file__) as s:
    with s.transformation(shift=-1.5):
        for i in range(4):
            with s.transformation(rotate=90 * i):
                s.draw_path(octa_piece(), svg.COLORS[i])

    with s.transformation(shift=1.5):
        with s.transformation(shift=-P - Q, rotate=0):
            s.draw_path(octa_piece(), svg.COLORS[0])
        with s.transformation(shift=-P + Q, rotate=90):
            s.draw_path(octa_piece(), svg.COLORS[1])
        with s.transformation(shift=P + Q, rotate=180):
            s.draw_path(octa_piece(), svg.COLORS[2])
        with s.transformation(shift=P - Q, rotate=270):
            s.draw_path(octa_piece(), svg.COLORS[3])
