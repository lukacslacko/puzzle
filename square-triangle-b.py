import cmath
import svg
from jigsaw import along

triangle_edge = cmath.sqrt(4 / cmath.sqrt(3))
triangle_height = triangle_edge * cmath.sqrt(3) / 2

x = (triangle_height - 1) / 2
y = (1 - triangle_edge/2)/2

A = -1-1j
B = 1j*A
C = 1j*B
D = 1j*C
P = A+2j*y
R = A+4j*y
Q = C-2j*y
S = C-4j*y
T = R+2*x
U = S-2*x
W = U-Q
V = -W

pieces = [
    svg.Path(A).line(B).line(W).line(T).line(P).line(A),
    svg.Path(B).line(S).line(U).line(W).line(B),
    svg.Path(C).line(D).line(V).line(U).line(Q).line(C),
    svg.Path(D).line(R).line(T).line(V).line(D),
    svg.Path(P).line(T).line(R).line(P),
    svg.Path(S).line(Q).line(U).line(S),
]

tri_pieces = [
    svg.Path(A+V).line(B+V).line(W+V).line(T+V).line(P+V).line(A+V),
    svg.Path(B+V).line(S+V).line(U+V).line(W+V).line(B+V),
    svg.Path(C+W).line(D+W).line(V+W).line(U+W).line(Q+W).line(C+W),
    svg.Path(D+W).line(R+W).line(T+W).line(V+W).line(D+W),
    svg.Path(T).line(A+V).line(T+W).line(T),
    svg.Path(U).line(C+W).line(U+V).line(U),
]

def f(p):
    return -p.real - (-p.imag - triangle_edge)  * 1j

real_tri_pieces = [
    svg.Path(f(A+V)).line(f(B+V)).line(f(W+V)).line(f(T+V)).line(f(P+V)).line(f(A+V)),
    svg.Path(B+V).line(S+V).line(U+V).line(W+V).line(B+V),
    svg.Path(C+W).line(D+W).line(V+W).line(U+W).line(Q+W).line(C+W),
    svg.Path(f(D+W)).line(f(R+W)).line(f(T+W)).line(f(V+W)).line(f(D+W)),
    svg.Path(f(T)).line(f(A+V)).line(f(T+W)).line(f(T)),
    svg.Path(U).line(C+W).line(U+V).line(U),
]

with svg.SVG(0, 3.5, 700, 700, __file__) as s:
    with s.transformation(shift=-1.5-1j):
        s.mark_all_caps([globals(), locals()])
        for i, piece in enumerate(pieces):
            s.draw_path(piece, svg.COLORS[i])

    with s.transformation(shift=1.5-1j):
        for i, piece in enumerate(tri_pieces):
            s.draw_path(piece, svg.COLORS[i])

    with s.transformation(shift=1.5+1j):
        for i, piece in enumerate(real_tri_pieces):
            s.draw_path(piece, svg.COLORS[i])