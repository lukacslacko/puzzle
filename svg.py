import cmath
import jigsaw

COLORS = [
    "pink",
    "lightblue",
    "lightgreen",
    "yellow",
    "orange",
    "red",
    "purple",
    "gray",
]


class Path:
    default_linear_tab_radius = 0.15
    default_linear_tab_left = True

    def __init__(self):
        self.path = []
        self.current = None

    def __init__(self, start: complex):
        self.path = ["M", start.real, start.imag]
        self.current = start

    def move(self, start: complex):
        self.path += ["M", start.real, start.imag]
        self.current = start
        return self

    def line(self, end: complex):
        self.path += ["L", end.real, end.imag]
        self.current = end
        return self

    def arc(
        self, radius: float, end: complex, large_arc: bool = False, sweep: bool = True
    ):
        self.path += [
            "A",
            radius,
            radius,
            0,
            int(large_arc),
            int(sweep),
            end.real,
            end.imag,
        ]
        self.current = end

    def linear_tab(self, end: complex, radius: float = None, left: bool = None):
        radius = radius if radius is not None else self.default_linear_tab_radius
        left = left if left is not None else self.default_linear_tab_left
        jigsaw.linear_tab(self.current, end, radius, self, left=left)
        self.current = end
        return self

    def circular_tab(
        self,
        center: complex,
        end: complex,
        towards: complex,
        radius: float,
        inwards: bool,
    ):
        jigsaw.circular_tab(
            center,
            self.current,
            end,
            towards,
            abs(end - center),
            radius,
            inwards=inwards,
            path=self,
        )
        self.current = end
        return self

    def __str__(self):
        return " ".join(map(str, self.path))


class SVGTransformation:
    def __init__(
        self, svg: "SVG", shift: complex = 0, rotate: float = 0, mirror: bool = False
    ):
        transformations_elements = [
            f"<g transform='translate({shift.real},{shift.imag})'>",
            f"<g transform='rotate({rotate})'>",
            f"<g transform='scale({-1 if mirror else 1},1)'>",
        ]
        for element in transformations_elements:
            svg.svg.append(element)
            svg.marks.append(element)
        self.svg = svg

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.svg.svg.append("</g></g></g>")
        self.svg.marks.append("</g></g></g>")


class SVG:
    def __init__(
        self, center: complex, size: float, width: int, height: int, filename: str
    ):
        self.center = center
        self.size = size
        self.width = width
        self.height = height
        if filename.endswith("py"):
            self.filename = filename[:-2] + "svg"
        else:
            self.filename = filename
        self.svg = []
        self.marks = []
        self.svg.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
        self.svg.append(
            '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="%d" height="%d">'
            % (width, height)
        )
        scale = min(width, height) / 2
        self.svg.append(
            '<g transform="translate(%d,%d) scale(%d)">'
            % (width / 2, height / 2, scale)
        )
        self.svg.append(
            '<g transform="translate(%f,%f) scale(%f)">'
            % (center.real, center.imag, 1 / size)
        )
        self.svg.append(
            '<g transform="translate(%f,%f)">' % (-center.real, -center.imag)
        )

    def draw_path(
        self,
        path: str,
        fill: str,
        stroke: str = "black",
        stroke_width: float = 0.015,
        shift: complex = 0,
        rotate: float = 0,
    ):
        self.svg.append(f"<g transform='translate({shift.real},{shift.imag})'>")
        self.svg.append(f"<g transform='rotate({rotate})'>")
        self.svg.append(
            f"<path d='{path}' fill='{fill}' stroke='{stroke}' stroke-width='{stroke_width}' />"
        )
        self.svg.append("</g></g>")

    def mark(self, point: complex, name: str, align: str = "tl", size: float = 0.2):
        baseline = {"t": "auto", "m": "middle", "b": "hanging"}[align[0]]
        anchor = {"l": "end", "c": "middle", "r": "start"}[align[1]]
        font_size = size
        self.marks.append(
            '<text font-family="monospace" x="%f" y="%f" text-anchor="%s" dominant-baseline="%s" font-size="%f">%s</text>'
            % (point.real, point.imag, anchor, baseline, font_size, name)
        )

    def mark_all_caps(self, named_points_dicts: list[dict]) -> None:
        for named_points_dict in named_points_dicts:
            for name, value in named_points_dict.items():
                if (
                    isinstance(value, complex)
                    or isinstance(value, int)
                    or isinstance(value, float)
                ) and name.isupper():
                    self.mark(value, name, "bc")

    def transformation(
        self, shift: complex = 0, rotate: float = 0, mirror: bool = False
    ):
        return SVGTransformation(self, shift, rotate, mirror)

    def __str__(self):
        return "\n".join(self.svg) + "\n" + "\n".join(self.marks) + "</g></g></g></svg>"

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        with open(self.filename, "w") as f:
            f.write(str(self))
