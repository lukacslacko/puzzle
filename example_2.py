import cmath

from svg import SVG, Path
import jigsaw

eps = cmath.exp(cmath.pi * 2j / 5)

with SVG(0, 1.2, 500, 500, __file__) as s:
    path = Path(1)
    s.mark(1, "A", "bc")
    path.line(0.5)
    s.mark(0, "O", "mc")
    jigsaw.circular_tab(0, 1, 1j, 1 + 1j, 0.5, 0.15, inwards=True, path=path)
    path.line(1j)
    s.mark(1j, "C", "bc")
    jigsaw.linear_tab(1j, -1, 0.15, path, left=True)
    jigsaw.linear_tab(-1, -1j, 0.15, path, left=False)
    jigsaw.circular_tab(0, -1j, 1, 1-1j, 1, 0.15, inwards=False, path=path)
    s.draw_path(path, "pink", "black", 0.01)
