import cmath

import svg
import jigsaw


with svg.SVG(0, 2.5, 700, 500, "a.svg") as s:
    with s.transformation(shift=-1.5, rotate=0):
        path = svg.Path()
        path.move(1 - 2j)
        path.line(1 + 1j)
        jigsaw.linear_tab(1 + 1j, -1 - 1j, 0.3, path, left=True)
        path.line(-1 - 2j)
        s.draw_path(path, svg.COLORS[0])

        path = svg.Path()
        path.move(1 + 2j)
        path.line(1 + 1j)
        jigsaw.linear_tab(1 + 1j, -1 - 1j, 0.3, path, left=True)
        path.line(-1 + 2j)
        s.draw_path(path, svg.COLORS[1])

    with s.transformation(shift=1.5, rotate=0):
        path = svg.Path()
        path.move(2 + 1j)
        path.line(1 + 1j)
        jigsaw.linear_tab(1 + 1j, -1 - 1j, 0.3, path, left=True)
        path.line(2 - 1j)
        s.draw_path(path, svg.COLORS[0])

        path = svg.Path()
        path.move(1 + 2j)
        path.line(1 + 1j)
        jigsaw.linear_tab(1 + 1j, -1 - 1j, 0.3, path, left=True)
        path.line(-1 + 2j)
        s.draw_path(path, svg.COLORS[1])
