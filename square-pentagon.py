import cmath
import svg
from jigsaw import along, area, perpendicular_projection


eps = cmath.exp(2j * cmath.pi / 5)
penta_scale = 1 / abs(1 - eps)
A = 1j * penta_scale
B = A * eps
C = B * eps
D = C * eps
E = D * eps

square_edge = cmath.sqrt(5 * area(0, A, B))

# gamma = 72 degrees
# c = square_edge
# a = 1
# c^2 = a^2 + b^2 - 2ab cos(gamma)
# 0 = b^2 - 2*cos(gamma)*b + 1 - square_edge^2
# b = cos(gamma) +- sqrt(cos(gamma)^2 - 1 + square_edge^2)
gamma = 72 * cmath.pi / 180
b = cmath.cos(gamma) + cmath.sqrt(cmath.cos(gamma) ** 2 - 1 + square_edge**2)

print(square_edge, b)
F = along(C, A, b)
G = (A + C) / 2
P = perpendicular_projection(D, F, E)
H = along(A, B, abs(A - G))
K = along(F, C, abs(A - G))
Q = perpendicular_projection(F, D, K)

with svg.SVG(0, 1.2, 700, 700, __file__) as s:
    s.mark_all_caps([globals(), locals()], size=0.1)
    for path in [
        svg.Path(A).line(B).line(C).line(D).line(E).line(A).line(C),
        svg.Path(H).line(G),
        svg.Path(F).line(D),
        svg.Path(K).line(Q),
        svg.Path(P).line(E),
    ]:
        s.draw_path(
            path,
            "transparent",
            "black",
            0.01,
        )
