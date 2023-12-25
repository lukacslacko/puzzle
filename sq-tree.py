import cmath

from draw import Draw, angles

x = (8 - cmath.sqrt(24)) / 2

A = 1.5j
B = 3j
C = 6j
D = 4 - 2 * x
E = 4 - 2 * x + 1.5j * x / (4 - x)
F = 4 - x
G = 4
H = 2 + 2j
I = 3 + 2j
J = 2 + 3j
K = 1 + 4j
L = 2 + 4j

d = Draw()
d.linear_tab(A, 0, 0.15, 0.03)
q, p = d.ctabin(E, angles(A, D, E, 0), 0.5, 0.15, 0.03)
d.cpoly([[0, D, p], [q, A]])
d.dxf("sq-tree-a.dxf")

d = Draw()
d.linear_tab(0,A, 0.15, 0.03)
q, p = d.ctabin(E, angles(A, D, E, 0), 0.5, 0.15, 0.03)
d.cpoly([[0, D, p], [q, A]])
d.dxf("sq-tree-a2.dxf")


d = Draw()
e, f = d.ctabout(E, angles(D, F, E, (D + F) / 2), 0.5, 0.15, 0.03)
q, p = d.ctabout(F, angles(E, D, F, (D + E) / 2), 0.75, 0.15, 0.03)
d.cpoly([[q, f], [e, D, p]])
d.dxf("sq-tree-b.dxf")

d = Draw()
q, p = d.ctabin(E, angles(A, D, E, 0), 0.5, 0.15, 0.03)
e, f = d.ctabout(E, angles(D, F, E, (D + F) / 2), 0.5, 0.15, 0.03)
d.cpoly([[q, f]])
d.dxf("sq-tree-c.dxf")

d = Draw()
p, q = d.ctabin(F, angles(G, A, F, H), 0.75, 0.15, 0.03)
s, r = d.ctabin(J, angles(B, I, J, 0), 0.75, 0.15, 0.03)
d.linear_tab(B, A, 0.15, 0.03)
d.cpoly([[A, q], [p, G, H, I, r], [s, B]])
d.dxf("sq-tree-d.dxf")

d = Draw()
p, q = d.ctabin(F, angles(G, A, F, H), 0.75, 0.15, 0.03)
s, r = d.ctabin(J, angles(B, I, J, 0), 0.75, 0.15, 0.03)
d.linear_tab(A, B, 0.15, 0.03)
d.cpoly([[A, q], [p, G, H, I, r], [s, B]])
d.dxf("sq-tree-d2.dxf")

d = Draw()
p, q = d.ctabin(J, angles(K, B, J, (B+K)/2), 0.75, 0.15, 0.03)
d.cpoly([[p,K,L,C,B,q]])
d.dxf("sq-tree-e.dxf")

d = Draw()
p, q = d.ctabin(J, angles(K, B, J, (B+K)/2), 0.75, 0.15, 0.03)
s, r = d.ctabin(J, angles(B, I, J, 0), 0.75, 0.15, 0.03)
d.cpoly([[p,r]])
d.dxf("sq-tree-f.dxf")

d = Draw()
p, q = d.ctabin(F, angles(G, A, F, H), 0.75, 0.15, 0.03)
r, s = d.ctabout(F, angles(E, D, F, (D + E) / 2), 0.75, 0.15, 0.03)
d.cpoly([[p,s]])
d.dxf("sq-tree-g.dxf")
