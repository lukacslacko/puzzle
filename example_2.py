import cmath

from svg import SVG, Path
import jigsaw

eps = cmath.exp(cmath.pi * 2j / 5)

with SVG(0, 1.2, 500, 500, "a.svg") as s:
    path = Path()
    path.move(1)
    s.mark(1, "A", "bc")
    path.line(0.5)
    s.mark(0, "O", "mc")
    jigsaw.circular_tab_inwards(0, 1, 1j, 1 + 1j, 0.5, 0.15, path)
    path.line(1j)
    s.mark(1j, "C", "bc")
    jigsaw.linear_tab(1j, -1, 0.15, path, left=True)
    path.line(-1j)
    path.line(1)
    s.draw_path(path, "pink", "black", 0.01)
