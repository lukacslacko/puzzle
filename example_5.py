import cmath

import svg
import jigsaw


def triangle(path: svg.Path, angle: float, inwards: bool):
    dir = cmath.exp(angle * 1j)
    path.move(1)
    path.line(0.5)
    jigsaw.circular_tab(0, 1, dir, dir + 1, 0.5, 0.1, inwards=inwards, path=path)
    path.line(dir)


def corner(path: svg.Path, angle_up: float, angle_down: float, inwards: bool):
    dir_up = cmath.exp(angle_up * 1j)
    dir_down = cmath.exp(-angle_down * 1j)
    path.move(0)
    path.line(0.5 * dir_down)
    jigsaw.circular_tab(
        0, dir_down, 1, 1 + dir_down, .5, 0.1, inwards=inwards, path=path
    )
    jigsaw.circular_tab(0, 1, dir_up, 1 + dir_up, .5, 0.1, inwards=inwards, path=path)
    path.line(0)


with svg.SVG(-.4+.8j, 1.6, 700, 700, "a.svg") as s:
    for y, inwards in [(0, True), (-1.5j, False)]:
        path = svg.Path()
        triangle(path, cmath.pi / 3, inwards)
        s.draw_path(path, svg.COLORS[0], shift=-1.1 + y)
        s.draw_path(path, svg.COLORS[0], shift= y)

        path = svg.Path()
        triangle(path, cmath.pi / 5, inwards)
        s.draw_path(path, svg.COLORS[1], shift=-1.1 + y, rotate=60)
        s.draw_path(path, svg.COLORS[1], shift= y, rotate=-36)

        path = svg.Path()
        corner(path, cmath.pi / 5, cmath.pi / 3, inwards)
        s.draw_path(path, svg.COLORS[2], shift=-1.1 + y, rotate=60)

        path = svg.Path()
        corner(path, cmath.pi / 3, cmath.pi / 5, inwards)
        s.draw_path(path, svg.COLORS[2], shift=y, rotate=0)
