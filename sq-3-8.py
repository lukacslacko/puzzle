import cmath

from draw import Draw, line_intersection, angles, DXF

eps = cmath.exp(2j * cmath.pi / 8)

A = 1
B = eps
C = eps ** 2
H = 1 / eps

P = (A + H) / 2
Q = (B + C) / 2

octaedge = abs(A-B)
d = abs(P - Q)
# d*d = x*x + (octaedge+x)*(octaedge+x)
# d*d = x*x + octaedge*octaedge + 2*x*octaedge + x*x
# d*d = 2*x*x + 2*x*octaedge + octaedge*octaedge
# 0 = 2*x*x + 2*x*octaedge + octaedge*octaedge - d*d
# x = (-2*octaedge + sqrt(4*octaedge*octaedge - 4*2*(octaedge*octaedge - d*d)))/4
x = (-2*octaedge + cmath.sqrt(4*octaedge*octaedge - 4*2*(octaedge*octaedge - d*d)))/4

alpha = cmath.atan(x/(octaedge+x))

T = (P-Q) * cmath.exp(-1j * alpha) * cmath.cos(alpha) + Q

X = B + (A - B) * (.5 + .5j)

I = P-X
E = A-X
H = B-X
L = Q-X
A = T-X
B = 1j*A
C = 1j*B
D = 1j*C
F = 1j*E
G = 1j*F
I = 1j*L
J = 1j*I
K = 1j*J

b = (3**.25-1)/2
c = (1-3**-.25)/2

h = B-A
v = D-A

P1 = A - b*h
P2 = A - 2*b*h + (1-2*c)*v
R = (P2+B)/2

S = -R

M = A + c*v
W = A + 2*c*v
Y = A + 2*c*v + b*h
X = -Y
Z = -W
N = -M

U = line_intersection(M,N, E,H)
V = line_intersection(M,N, F,G)
P = line_intersection(E,F, B,R)
Q = line_intersection(H,G, D,S)

simple_polys = [
    [A,I,E,U,M,A],
    [B,P,E,I,B],
    [J,F,P,B,J],
    [Z,X,V,F,J,Z],
    [N,X,Z,N],
    [C,K,G,V,N,C],
    [D,Q,G,K,D],
    [D,L,H,Q,D],
    [W,Y,U,H,L,W],
    [M,Y,W,M],
    [E,P,R,U,E],
    [F,V,R,P,F],
    [G,Q,S,V,G],
    [H,U,S,Q,H],
]

for i in range(len(simple_polys)):
    d = Draw()
    d.cpoly([simple_polys[i]])
    d.dxf(f"simple-sq-3-8-{i}.dxf")

octa = (0.12, 0.05, 0.01)
tri = (0.12, 0.02, 0.004)
mid = (0.17, 0.05, 0.01)

gap = 0.1
box = [[A-gap*h-gap*v, B+gap*h-gap*v, C+gap*h+gap*v, D-gap*h+gap*v]]
box = False

with DXF("438a") as d:
    # IE, IA = d.ctabout(I, angles(E, A, I, M), *octa)
    # MA, MY = d.ctabout(M, angles(A, Y, M, I), *octa)
    # d.cpoly([[MA,A,IA], [IE,E,U,MY]])
    IE = d.along(I, E, *octa)
    IA = d.out_tab(I, E, A, M, *octa, IE)
    d.cline(IA,A)
    MA = d.along(M, A, *octa)
    d.cline(A,MA)
    MU = d.out_tab(M, A, U, E, *octa, MA)
    d.cline(MU,U)
    d.cline(U,E)
    d.cline(E,IE)
    if box:
        d.cpoly(box)

with DXF("438b") as d:
    PE, PB = d.ctabin(P, angles(E, B, P, I), *mid)
    IB, _ = d.ctabout(I, angles(B, E, I, P), *octa)
    d.cpoly([[IB,B,PB], [PE,E,IE]])
    if box:
        d.cpoly(box)

with DXF("438c") as d:
    JF, JB = d.ctabout(J, angles(F, B, J, P), *octa)
    PB, PF = d.ctabout(P, angles(B, F, P, J), *mid)
    d.cpoly([[PF,F,JF], [JB,B,PB]])
    if box:
        d.cpoly(box)

with DXF("438d") as d:
    XV, XZ = d.ctabout(X, angles(V, Z, X, J), *octa)
    JZ, JF = d.ctabout(J, angles(Z, F, J, X), *octa)
    d.cpoly([[JZ,Z], [XV,V,F,JF]])
    d.linear_tab(XZ, Z, tri[1], tri[2])
    if box:
        d.cpoly(box)

with DXF("438e") as d:
    NX, NZ = d.ctabout(N, angles(X, Z, N, J), *tri)
    XZ, XN = d.ctabout(X, angles(Z, N, X, J), *tri)
    d.cpoly([[XN,NX], [Z,NZ]])
    d.linear_tab(XZ, Z, tri[1], tri[2])
    if box:
        d.cpoly(box)

with DXF("438f") as d:
    MY, MW = d.ctabout(M, angles(Y, W, M, H), *tri)
    YW, YM = d.ctabout(Y, angles(W, M, Y, (M+W)/2), *tri)
    d.cpoly([[YM,MY], [MW,W]])
    d.linear_tab(W, YW, tri[1], tri[2])
    if box:
        d.cpoly(box)

with DXF("438g") as d:
    YU, YW = d.ctabout(Y, angles(U, W, Y, L), *octa)
    LW, LH = d.ctabout(L, angles(W, H, L, Y), *octa)
    d.cpoly([[W,LW], [LH,H,U,YU]])
    d.linear_tab(W, YW, tri[1], tri[2])
    if box:
        d.cpoly(box)

with DXF("438h") as d:
    PR, PE = d.ctabout(P, angles(R, E, P, U), *mid)
    d.cpoly([[PR,R,U,E,PE]])
    if box:
        d.cpoly(box)

with DXF("438i") as d:
    PF, PR = d.ctabin(P, angles(F, R, P, V), *mid)
    d.cpoly([[PF,F,V,R,PR]])
    if box:
        d.cpoly(box)

with DXF("438j") as d:
    # IB, IE = d.ctabout(I, angles(B, E, I, P), *octa)
    # IE, IA = d.ctabout(I, angles(E, A, I, M), *octa)
    # d.cpoly([[IA,IB]])
    # if box:
    #     d.cpoly(box)

    IB = d.along(I, B, *octa)
    IE = d.out_tab(I, B, E, P, *octa, IB)
    IA = d.out_tab(I, E, A, M, *octa, IE)
    d.cline(IA, IB)
    if box:
        d.cpoly(box)

with DXF("438k") as d:
    MA, MY = d.ctabout(M, angles(A, Y, M, I), *octa)
    MY, MW = d.ctabout(M, angles(Y, W, M, H), *tri)
    d.cpoly([[MW,MA]])
    if box:
        d.cpoly(box)

with DXF("438l") as d:
    YU, YW = d.ctabout(Y, angles(U, W, Y, L), *octa)
    YW, YM = d.ctabout(Y, angles(W, M, Y, (M+W)/2), *tri)
    d.cpoly([[YM,YU]])
    if box:
        d.cpoly(box)

with DXF("438m") as d:
    PR, PE = d.ctabout(P, angles(R, E, P, U), *mid)
    PE, PB = d.ctabin(P, angles(E, B, P, I), *mid)
    d.cpoly([[PB,PR]])
    if box:
        d.cpoly(box)

with DXF("438n") as d:
    JZ, JF = d.ctabout(J, angles(Z, F, J, X), *octa)
    JF, JB = d.ctabout(J, angles(F, B, J, P), *octa)
    d.cpoly([[JB,JZ]])
    if box:
        d.cpoly(box)
        