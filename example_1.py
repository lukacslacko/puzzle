import cmath

from svg import SVG, Path
import jigsaw

eps = cmath.exp(cmath.pi * 2j / 5)

path = Path()
path.move(1)
for i in range(5):
    jigsaw.linear_tab(eps**i, eps**(i+1), 0.15, path, left=False)

with SVG(0, 1.2, 500, 500, "a.svg") as s:
    s.draw_path(path, "pink", "black", 0.01)
    for i in range(5):
        s.mark(eps**i, f"P{i}", "br")
