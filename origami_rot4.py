import cmath
import svg

P = svg.Path

outline = ["transparent", "black", 0.003]

def poly(v: list[complex], d=0) -> svg.Path:
    r = P(v[0]+d)
    for i in v[1:]:
        r.line(i+d)
    return r

def unit_a(d):
    return map(lambda v:poly(v,d), [
        [3,3+1j],[5+3j,4+3j],[2+5j,2+4j],[2j,1+2j],[1+2j,3+1j,4+3j,2+4j,1+2j]
    ])
def unit_a_back(d):
    return map(lambda v:poly(v,d), [
        [1j,3+1j],[4,4+3j],[5+4j,2+4j],[1+5j,1+2j]
    ])
def unit_b(d):
    return map(lambda v:poly(v,d), [
        [2,2+1j],[0+3j,1+3j],[3+5j,3+4j],[5+2j,4+2j],[4+2j,2+1j,1+3j,3+4j,4+2j]
    ])
def unit_b_back(d):
    return map(lambda v:poly(v,d), [
        [5+1j,2+1j],[1,1+3j],[0+4j,3+4j],[4+5j,4+2j]
    ])

n=3
o=["transparent","black",0.1]
with svg.SVG(0, 5*n, 700, 700, __file__, "front") as s:
    for i in range(n):
        for j in range(n):
            if (i+j)%2 == 0:
                for p in unit_a(5*(i+j*1j)):
                    s.draw_path(p,*o)
            else:
                for p in unit_b(5*(i+j*1j)):
                    s.draw_path(p,*o)

with svg.SVG(0, 5*n, 700, 700, __file__, "back") as s:
    for i in range(n):
        for j in range(n):
            if (i+j)%2 != 0:
                for p in unit_a_back(5*(i+j*1j)):
                    s.draw_path(p,*o)
            else:
                for p in unit_b_back(5*(i+j*1j)):
                    s.draw_path(p,*o)

with svg.SVG(0, 1, 700, 700, __file__, "grid") as s:
    for i in range(33):
        for j in range(33):
            s.draw_path(poly([i,i+32j]),*o)
            s.draw_path(poly([1j*i,1j*i+32]),*o)