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

d = Draw()
v = [T-X,P-X,A-X,B-X,Q-X,T-X]
d.cpoly([[x*1j**i for x in v] for i in range(4)])

S1 = T - X
S2 = -1j * S1
S3 = -1j * S2
S4 = -1j * S3

SA = (S1 + S4) / 2

b = (3**.25-1)/2
c = (1-3**-.25)/2
SA = T-X
SB = 1j * SA
SC = 1j * SB
SD = 1j * SC

h = SB-SA
v = SD-SA
SP = SA - b*h
ST = SA - 2*b*h + (1-2*c)*v
SR = (ST+SB)/2

TA = A-X
TB = B-X

SU = line_intersection(SA+c*v,SR,A-X,B-X)
SR1 = SU + abs(SR-SU)/abs(TB-SU)*(TB-SU)
SR3 = SU - abs(SR-SU)/abs(TB-SU)*(TB-SU)
SR2 = SU - (SR-SU)

d.cpoly([[SA,SA+c*v, SR2],[SR,SB,SA],[SR,SA+h+(1-c)*v,SA+h,SA],[SA+c*v,SA+2*c*v+b*h,SA+2*c*v,SA+c*v]])
# d.linear_tab(SR1,SR,0.03,0.01)
d.linear_tab(SR,SR3,0.03,0.01)
# d.linear_tab(SR3,SR2,0.03,0.01)
d.linear_tab(SR2,SR1,0.03,0.01)

d.ctabout(SU, angles(SR,SR1,SU,(SR+SR1)/2), abs(SR-SU), 0.03, 0.01)
d.ctabout(SU, angles(SR2,SR3,SU,(SR2+SR3)/2), abs(SR-SU), 0.03, 0.01)
# d.ctabin(SU, angles(SR1,SR2,SU,(SR2+SR1)/2), abs(SR-SU), 0.03, 0.01)
# d.ctabin(SU, angles(SR3,SR,SU,(SR+SR3)/2), abs(SR-SU), 0.03, 0.01)

d.dxf("sq-3-8-a.dxf")
