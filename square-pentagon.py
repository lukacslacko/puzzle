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

r_G, rho_G, inwards_G = 0.15, 0.04, True

r_B = 0.08
rho_B = 0.02
inwards_B = True

r_F, rho_F, inwards_F = 0.15, 0.04, True
r_D, rho_D, inwards_D = 0.15, 0.04, True

EA = (E + A) / 2
EAA = along(EA, A, r_G)
FA = (A + F) / 2
FAF = along(FA, F, r_B)
FAA = along(FA, A, r_B)

AH = (A + H) / 2
AHH = along(AH, H, r_F)
HG = (H + G) / 2
HGG = along(HG, G, r_D)
HGH = along(HG, H, r_D)

BC = (B + C) / 2
BCC = along(BC, C, r_G)
KC = (K + C) / 2
KCK = along(KC, K, r_B)
KCC = along(KC, C, r_B)

FK = (F + K) / 2
FKK = along(FK, K, r_F)

CD1 = (C + 3 * D) / 4
CD2 = (3 * C + D) / 4
CD1D = along(CD1, D, r_D)
CD2D = along(CD2, D, r_D)

ED1 = along(E, D, abs(K - KC))
ED1E = along(ED1, E, r_B)
ED2 = along(D, E, abs(F - FA))
ED2E = along(ED2, E, r_B)


def piece_3():
    return (
        svg.Path(A)
        .line(EAA)
        .semicircular_tab(EA, rho_G, inwards_G)
        .line(E)
        .line(P)
        .line(F)
        .line(FAF)
        .semicircular_tab(FA, rho_B, inwards_B)
        .line(A)
    )


def piece_5():
    return (
        svg.Path(A)
        .line(FAA)
        .semicircular_tab(FA, rho_B, inwards_B)
        .line(G)
        .line(HGG)
        .semicircular_tab(HG, rho_D, inwards_D)
        .line(H)
        .line(AHH)
        .semicircular_tab(AH, rho_F, inwards_F)
        .line(A)
    )


def piece_4():
    return (
        svg.Path(G)
        .line(KCK)
        .semicircular_tab(KC, rho_B, inwards_B)
        .line(C)
        .line(BCC)
        .semicircular_tab(BC, rho_G, inwards_G)
        .line(B)
        .line(H)
        .line(HGH)
        .semicircular_tab(HG, rho_D, inwards_D)
        .line(G)
    )


def piece_2prime():
    return (
        svg.Path(F)
        .line(Q)
        .line(K)
        .line(FKK)
        .semicircular_tab(FK, rho_F, inwards_F)
        .line(F)
    )


def piece_2():
    return (
        svg.Path(C)
        .line(KCC)
        .semicircular_tab(KC, rho_B, inwards_B)
        .line(K)
        .line(Q)
        .line(D)
        .line(CD1D)
        .semicircular_tab(CD1, rho_D, inwards_D)
        .line(CD2D)
        .semicircular_tab(CD2, rho_D, inwards_D)
        .line(C)
    )


def piece_1():
    return (
        svg.Path(P)
        .line(E)
        .line(ED1E)
        .semicircular_tab(ED1, rho_B, inwards_B)
        .line(ED2E)
        .semicircular_tab(ED2, rho_B, inwards_B)
        .line(D)
        .line(P)
    )


def draw_penta():
    with svg.SVG(0, 1.2, 700, 700, __file__) as s:
        # s.mark_all_caps([globals(), locals()], size=0.1)
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
                0.003,
            )
        for i, piece in enumerate(
            [piece_3(), piece_5(), piece_4(), piece_2prime(), piece_2(), piece_1()]
        ):
            s.draw_path(piece, svg.COLORS[i], "black", 0.003)


def draw_render():
    with svg.SVG(0, 100, 700, 700, __file__, "render") as s:
        for piece, d in [
            (piece_3(), EA * 0.1),
            (piece_5(), (A + B) / 2 * 0.1),
            (piece_4(), (B + C) / 2 * 0.1),
            (piece_2prime(), 0),
            (piece_2(), (C + D) / 2 * 0.1),
            (piece_1(), (D + E) / 2 * 0.1),
        ]:
            with s.transformation(scale=100), s.transformation(shift=d):
                s.draw_path(piece, "transparent", "black", 0.005)


draw_penta()
draw_render()
