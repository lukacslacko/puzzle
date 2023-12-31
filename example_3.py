import cmath

from svg import SVG, Path
import jigsaw

eps = cmath.exp(cmath.pi * 2j / 5)

with SVG(0, 1.2, 500, 500, "a.svg") as s:
    path = Path()
    path.move(1)
    for i in range(5):
        jigsaw.circular_tab(
            0,
            eps**i,
            eps ** (i + 1),
            eps ** (i + 0.5),
            1,
            0.15,
            inwards=False,
            path=path,
        )
    s.draw_path(path, "pink", "black", 0.01)
