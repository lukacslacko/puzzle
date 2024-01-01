import cmath

import svg
import jigsaw


A = 1
B = cmath.exp(cmath.pi * 2j / 5)
C = -1
D = -B


with svg.SVG(0, 3, 700, 500, "a.svg") as s:
    with s.transformation(shift=-2.2, rotate=0):
        path = svg.Path(2*A)
        path.line(A)
        path.linear_tab(B, 0.15, left=True)
        path.line(2*B)
        s.draw_path(path, svg.COLORS[0])

        path = svg.Path(2*B)
        path.line(B)
        path.linear_tab(C, 0.15, left=True)
        path.line(2*C)
        s.draw_path(path, svg.COLORS[1])

        path = svg.Path(2*C)
        path.line(C)
        path.linear_tab(D, 0.15, left=True)
        path.line(2*D)
        s.draw_path(path, svg.COLORS[2])

        path = svg.Path(2*D)
        path.line(D)
        path.linear_tab(A, 0.15, left=True)
        path.line(2*A)
        s.draw_path(path, svg.COLORS[3])

        path = svg.Path(A)
        path.linear_tab(B, 0.15, left=True)
        path.linear_tab(C, 0.15, left=True)
        path.line(A)
        s.draw_path(path, svg.COLORS[4])

        path = svg.Path(C)
        path.linear_tab(D, 0.15, left=True)
        path.linear_tab(A, 0.15, left=True)
        path.line(C)
        s.draw_path(path, svg.COLORS[5])

        s.mark(A, "A", "br")
        s.mark(B, "B", "bl")
        s.mark(C, "C", "tl")
        s.mark(D, "D", "tr")

    with s.transformation(shift=2.2, rotate=0):
        path = svg.Path(2*A)
        path.line(A)
        path.linear_tab(B, 0.15, left=True)
        path.line(2*B)
        s.draw_path(path, svg.COLORS[0])

        path = svg.Path(2*B)
        path.line(B)
        path.linear_tab(C, 0.15, left=True)
        path.line(2*C)
        s.draw_path(path, svg.COLORS[1])

        path = svg.Path(2*C)
        path.line(C)
        path.linear_tab(D, 0.15, left=True)
        path.line(2*D)
        s.draw_path(path, svg.COLORS[2])

        path = svg.Path(2*D)
        path.line(D)
        path.linear_tab(A, 0.15, left=True)
        path.line(2*A)
        s.draw_path(path, svg.COLORS[3])

        path = svg.Path(A)
        path.linear_tab(B, 0.15, left=True)
        path.line(D)
        path.linear_tab(A, 0.15, left=True)
        s.draw_path(path, svg.COLORS[4])

        path = svg.Path(C)
        path.linear_tab(D, 0.15, left=True)
        path.line(B)
        path.linear_tab(C, 0.15, left=True)
        s.draw_path(path, svg.COLORS[5])
