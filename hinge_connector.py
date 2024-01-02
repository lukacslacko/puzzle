import cmath

import svg
import jigsaw


def triangle(angle: float, inwards: bool) -> svg.Path:
    dir = cmath.exp(angle * 1j)
    path = svg.Path(1)
    path.line(0.5)
    jigsaw.circular_tab(0, 1, dir, dir + 1, 0.5, 0.1, inwards=inwards, path=path)
    path.line(dir)
    return path


def corner(angle_up: float, angle_down: float, inwards: bool) -> svg.Path:
    dir_up = cmath.exp(angle_up * 1j)
    dir_down = cmath.exp(-angle_down * 1j)
    path = svg.Path(0)
    path.line(0.5 * dir_down)
    jigsaw.circular_tab(
        0, dir_down, 1, 1 + dir_down, .5, 0.1, inwards=inwards, path=path
    )
    jigsaw.circular_tab(0, 1, dir_up, 1 + dir_up, .5, 0.1, inwards=inwards, path=path)
    path.line(0)
    return path

with svg.SVG(-.4+.8j, 1.6, 700, 700, __file__) as s:
    for y, inwards in [(0, True), (-1.5j, False)]:
        path = triangle(cmath.pi / 3, inwards)
        s.draw_path(path, svg.COLORS[0], shift=-1.1 + y)
        s.draw_path(path, svg.COLORS[0], shift= y)

        path = triangle(cmath.pi / 5, inwards)
        s.draw_path(path, svg.COLORS[1], shift=-1.1 + y, rotate=60)
        s.draw_path(path, svg.COLORS[1], shift= y, rotate=-36)

        path = corner(cmath.pi / 5, cmath.pi / 3, inwards)
        s.draw_path(path, svg.COLORS[2], shift=-1.1 + y, rotate=60)

        path = corner(cmath.pi / 3, cmath.pi / 5, inwards)
        s.draw_path(path, svg.COLORS[2], shift=y, rotate=0)
