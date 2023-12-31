import cmath

import svg
import jigsaw


def edge(path: svg.Path, r: float = 0.5):
    path.move(1 + 0.75j)
    path.line(1)
    path.line(r)
    jigsaw.circular_tab(0, 1, 1j, 1 + 1j, r, r * 0.2, inwards=True, path=path)
    jigsaw.circular_tab(0, 1j, -1, -1 + 1j, r, r * 0.2, inwards=True, path=path)
    path.line(-1)
    path.line(-1 + 0.75j)


def connector(path: svg.Path, inwards: bool = True, r: float = 0.5):
    path.move(-r * 1j)
    jigsaw.circular_tab(0, -1j, 1, 1 - 1j, r, r * 0.2, inwards=inwards, path=path)
    jigsaw.circular_tab(0, 1, 1j, 1 + 1j, r, r * 0.2, inwards=inwards, path=path)
    path.line(-r * 1j)


with svg.SVG(1.2j, 2.05, 700, 600, "a.svg") as s:
    for y, inwards in [(0, True), (-2.2j, False)]:
        path = svg.Path()
        edge(path)
        s.draw_path(path, svg.COLORS[0], shift=-1.1 + y)
        s.draw_path(path, svg.COLORS[0], shift=1.1 + y)

        path = svg.Path()
        edge(path)
        s.draw_path(path, svg.COLORS[1], shift=-1.1 + y, rotate=180)
        s.draw_path(
            path, svg.COLORS[1], shift=1.1 - 0.2j + y, rotate=170
        )

        path = svg.Path()
        connector(path, inwards=inwards)
        s.draw_path(path, svg.COLORS[2], shift=-1.1 + y, rotate=180)
        s.draw_path(
            path, svg.COLORS[2], shift=1.1 - 0.2j + y, rotate=170 + 90
        )

        path = svg.Path()
        connector(path, inwards=inwards)
        s.draw_path(path, svg.COLORS[3], shift=-1.1 + y)
        s.draw_path(path, svg.COLORS[3], shift=1.1 + y, rotate=90)
