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

T = (A+H)/2
U = (B+C)/2
V = (C+D)/2
W = (A+E)/2

rho = 0.25
r = 0.05

GA = along(G, A, rho)
GH = along(G, H, rho)
GC = along(G, C, rho)

TA = along(T, A, rho)
TH = along(T, H, rho)
S = T + (TH-T)*eps

UB = along(U, B, rho)
UC = along(U, C, rho)
UU = U+1j*(UC-U)

VC = along(V, C, rho)
VD = along(V, D, rho)
R = V+(VC-V)/eps

DC = along(D, C, rho)
DP = along(D, P, rho)
DE = along(D, E, rho)

ED = along(E, D, rho)
EP = along(E, P, rho)
EA = along(E, A, rho)

WE = along(W, E, rho)
WA = along(W, A, rho)
WW = W+1j*(WA-W)

ang_E = (A-E)/(Q-E)
ang_E /= abs(ang_E)

KC = along(K, C, rho)
Y = K + (KC-K)/ang_E

ang_D = (P-D)/(C-D)
ang_D /= abs(ang_D)
FA = along(F, A, rho)
X = F + (FA-F)*ang_D

print(ang_E, ang_D)

QK = along(Q, K, 2*rho)
QF = along(Q, F, 2*rho)
QQ = (QK+QF)/2
QV = QQ+(Q-QF)
QW = QQ+(Q-QK)

#pieces = [
#    svg.Path(H).line(GH).circular_tab(G, GC, GC, r, True).line(C).line(B).line(H),
#    svg.Path(A).line(GA).circular_tab(G, GH, GH, r, True).line(H).line(TH).circular_tab(T,S,S,r,True).circular_tab(T,TA,TA,r,True).line(A),
#]
pieces = [
    svg.Path(H).line(GH).linear_tab(GC,r).line(C).line(UC).linear_tab(UU,r).linear_tab(UB,r).line(B).line(H),
    svg.Path(A).line(GA).linear_tab(GH,r).line(H).line(TH).linear_tab(S,r).linear_tab(TA,r).line(A),
    svg.Path(Q).line(DP).linear_tab(DC,r,False).linear_tab(R,r).linear_tab(VC,r).line(C).line(KC).linear_tab(Y,r).line(K).line(QK).linear_tab(QV,r).linear_tab(Q,r),
    svg.Path(A).line(WA).linear_tab(WW,r).linear_tab(WE,r).line(EA).linear_tab(EP,r).line(P).line(Q).linear_tab(QW,r).linear_tab(QF,r).line(F).line(X).linear_tab(FA,r,False).line(A),
    svg.Path(F).line(QF).linear_tab(QQ,r).linear_tab(QK,r).line(K).line(GC).linear_tab(GH,r,False).linear_tab(GA,r,False).line(F),
    svg.Path(P).line(EP).linear_tab(ED,r,False).line(DE).linear_tab(DP,r,False).line(P),
    svg.Path(QQ).line(QW).linear_tab(Q,r,False).linear_tab(QV,r,False).line(QQ),
]

def draw_penta():
    with svg.SVG(0, 1.2, 700, 700, __file__) as s:
        #s.mark_all_caps([globals(), locals()], size=0.1)
        for path in [
            svg.Path(A).line(B).line(C).line(D).line(E).line(A),
        ]:
            s.draw_path(
                path,
                "transparent",
                "black",
                0.003,
            )
        for i, p in enumerate(pieces):
            s.draw_path(p, svg.COLORS[i], "black", 0.003)

def draw_square():
    with svg.SVG(-5+2j, 1.2, 700, 700, __file__, "-square") as s:
        for p in [
            svg.Path(P).line(P+D-F).line(P+(1+1j)*(D-F)).line(P+1j*(D-F)).line(P),
            svg.Path(WW+D-F).line(2*W-WW+D-F),
            svg.Path(R+E-K).line(2*V-R+E-K),
        ]:
            s.draw_path(p, "transparent", "black", 0.003)
#        for i, p in enumerate(pieces):
#            s.draw_path(p, svg.COLORS[i], "black", 0.003)
        s.draw_path(pieces[5], svg.COLORS[5], "black", 0.003)
        with s.transformation(shift=D-F):
            s.draw_path(pieces[3], svg.COLORS[3], "black", 0.003)
        with s.transformation(shift=E-K):
            s.draw_path(pieces[2], svg.COLORS[2], "black", 0.003)
        with s.transformation(shift=D-K+E-F):
            s.draw_path(pieces[4], svg.COLORS[4], "black", 0.003)
            with s.transformation(shift=(Q+QQ)/2), s.transformation(rotate=180), s.transformation(shift=-(Q+QQ)/2):
                s.draw_path(pieces[6], svg.COLORS[6], "black", 0.003)
        with s.transformation(shift=V+E-K), s.transformation(rotate=36), s.transformation(shift=-G):
            s.draw_path(pieces[0], svg.COLORS[0], "black", 0.003)
            with s.transformation(shift=G), s.transformation(rotate=180), s.transformation(shift=-G):
                s.draw_path(pieces[1], svg.COLORS[1], "black", 0.003)

draw_penta()
draw_square()
