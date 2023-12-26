import cmath

from draw import Draw, line_intersection, angles

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

octa_r = 0.2

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
