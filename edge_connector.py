import cmath

import svg
import jigsaw


def edge(r: float = 0.5) -> svg.Path:
    path = svg.Path(1 + 0.75j)
    path.line(1)
    path.line(r)
    jigsaw.circular_tab(0, 1, 1j, 1 + 1j, r, r * 0.2, inwards=True, path=path)
    jigsaw.circular_tab(0, 1j, -1, -1 + 1j, r, r * 0.2, inwards=True, path=path)
    path.line(-1)
    path.line(-1 + 0.75j)
    return path

def connector(inwards: bool = True, r: float = 0.5) -> svg.Path:
    path = svg.Path(-r * 1j)
    jigsaw.circular_tab(0, -1j, 1, 1 - 1j, r, r * 0.2, inwards=inwards, path=path)
    jigsaw.circular_tab(0, 1, 1j, 1 + 1j, r, r * 0.2, inwards=inwards, path=path)
    path.line(-r * 1j)
    return path


with svg.SVG(1.2j, 2.05, 700, 600, __file__) as s:
    for y, inwards in [(0, True), (-2.2j, False)]:
        path = edge()
        s.draw_path(path, svg.COLORS[0], shift=-1.1 + y)
        s.draw_path(path, svg.COLORS[0], shift=1.1 + y)

        path = edge()
        s.draw_path(path, svg.COLORS[1], shift=-1.1 + y, rotate=180)
        s.draw_path(
            path, svg.COLORS[1], shift=1.1 - 0.2j + y, rotate=170
        )

        path = connector(inwards=inwards)
        s.draw_path(path, svg.COLORS[2], shift=-1.1 + y, rotate=180)
        s.draw_path(
            path, svg.COLORS[2], shift=1.1 - 0.2j + y, rotate=170 + 90
        )

        path = connector(inwards=inwards)
        s.draw_path(path, svg.COLORS[3], shift=-1.1 + y)
        s.draw_path(path, svg.COLORS[3], shift=1.1 + y, rotate=90)
