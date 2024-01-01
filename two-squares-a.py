import cmath
import svg
from jigsaw import along

R = 0.6
RHO = 0.15


def corner(center: complex, direction: complex, s: svg.SVG) -> svg.Path:
    A = center
    B = center + direction * R
    C = center + direction * R * cmath.exp(1j * cmath.pi / 4)
    D = center + direction * R * cmath.exp(2j * cmath.pi / 4)
    path = svg.Path(A)
    path.line(B)
    path.circular_tab(A, C, C, RHO, inwards=False)
    path.circular_tab(A, D, D, RHO, inwards=False)
    path.line(A)
    return path


def edge(center: complex, direction: complex) -> svg.Path:
    A = center
    B = center + direction
    C = center + direction * (-1j)
    BA = along(B, A, R)
    BC = along(B, C, R)
    CB = along(C, B, R)
    CA = along(C, A, R)
    path = svg.Path(A)
    path.line(BA)
    path.circular_tab(B, BC, BC, RHO, inwards=False)
    path.line(CB)
    path.circular_tab(C, CA, CA, RHO, inwards=False)
    path.line(A)
    return path


with svg.SVG(0, 1.1, 700, 300, __file__) as s:
    for i in range(4):
        with s.transformation(shift=-1.5, rotate=90*i):
            s.draw_path(edge(0, 1 + 1j), svg.COLORS[2*(i%2)])
            s.draw_path(corner(1+1j, -1, s), svg.COLORS[2*(i%2)+1])
    
    with s.transformation(shift=1+1j, rotate=-90):
        s.draw_path(edge(0, 1+1j), svg.COLORS[0])
    with s.transformation(shift=1-1j, rotate=90):
        s.draw_path(edge(0, 1+1j), svg.COLORS[0])
    with s.transformation(shift=2, rotate=-45):
        s.draw_path(corner(0, -1, s), svg.COLORS[1])
    with s.transformation(shift=0, rotate=180-45):
        s.draw_path(corner(0, -1, s), svg.COLORS[1])