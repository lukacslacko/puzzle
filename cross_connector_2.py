import cmath

import svg
import jigsaw


A = 1
B = cmath.exp(cmath.pi * 2j / 5)
C = -1
D = -B
A *= 0.7
B *= 0.7
C *= 0.7
D *= 0.7
AA = 3*A
BB = 3*B
CC = 3*C
DD = 3*D

with svg.SVG(0, 2, 700, 300, __file__) as s:
    with s.transformation(shift=-2.5, rotate=0):
        path = svg.Path(AA)
        path.line(A)
        path.circular_tab(0, B, B, 0.15, inwards=False)
        path.line(BB)
        s.draw_path(path, svg.COLORS[0])

        path = svg.Path(BB)
        path.line(B)
        path.circular_tab(0, C, C, 0.15, inwards=False)
        path.line(CC)
        s.draw_path(path, svg.COLORS[1])

        path = svg.Path(CC)
        path.line(C)
        path.circular_tab(0, D, D, 0.15, inwards=False)
        path.line(DD)
        s.draw_path(path, svg.COLORS[2])

        path = svg.Path(DD)
        path.line(D)
        path.circular_tab(0, A, A, 0.15, inwards=False)
        path.line(AA)
        s.draw_path(path, svg.COLORS[3])

        path = svg.Path(A)
        path.circular_tab(0, B, B, 0.15, inwards=False)
        path.circular_tab(0, C, C, 0.15, inwards=False)
        path.line(A)
        s.draw_path(path, svg.COLORS[4])

        path = svg.Path(C)
        path.circular_tab(0, D, D, 0.15, inwards=False)
        path.circular_tab(0, A, A, 0.15, inwards=False)
        path.line(C)
        s.draw_path(path, svg.COLORS[5])

        with s.transformation(shift=4.5, rotate=0):
            path = svg.Path(AA)
            path.line(A)
            path.circular_tab(0, B, B, 0.15, inwards=False)
            path.line(BB)
            s.draw_path(path, svg.COLORS[0])

            path = svg.Path(BB)
            path.line(B)
            path.circular_tab(0, C, C, 0.15, inwards=False)
            path.line(CC)
            s.draw_path(path, svg.COLORS[1])

            path = svg.Path(CC)
            path.line(C)
            path.circular_tab(0, D, D, 0.15, inwards=False)
            path.line(DD)
            s.draw_path(path, svg.COLORS[2])

            path = svg.Path(DD)
            path.line(D)
            path.circular_tab(0, A, A, 0.15, inwards=False)
            path.line(AA)
            s.draw_path(path, svg.COLORS[3])

            path = svg.Path(A)
            path.circular_tab(0, B, B, 0.15, inwards=False)
            path.line(D)
            path.circular_tab(0, A, A, 0.15, inwards=False)
            s.draw_path(path, svg.COLORS[4])

            path = svg.Path(C)
            path.circular_tab(0, D, D, 0.15, inwards=False)
            path.line(B)
            path.circular_tab(0, C, C, 0.15, inwards=False)
            s.draw_path(path, svg.COLORS[5])
