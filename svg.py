import cmath
import jigsaw
import re

COLORS = [
    "pink",
    "lightblue",
    "lightgreen",
    "yellow",
    "orange",
    "red",
    "purple",
    "gray",
    "brown",
    "green",
    "fuchsia",
    "limegreen",
    "violet",
]


class Path:
    default_linear_tab_radius = 0.15
    default_linear_tab_left = True

    def __init__(self):
        self.path = []
        self.current = None
        self.vertices = []
        self.dxf_pts = []
        self.dxf_scale = 150

    def __init__(self, start: complex, scale_for_dxf: float = 60):
        self.path = ["M", start.real, start.imag]
        self.current = start
        self.vertices = [start]
        self.dxf_pts = []
        self.dxf_scale = scale_for_dxf

    def move(self, start: complex):
        self.path += ["M", start.real, start.imag]
        self.current = start
        self.vertices.append(start)
        self.dxf_pts = []
        return self

    def _dxf_line(self, start: complex, end: complex):
        if abs(start - end) < 1e-6:
            print("skip")
            return
        self.dxf_pts += ["10", self.dxf_scale * end.real, "20", self.dxf_scale * end.imag, "11", self.dxf_scale * end.real, "21", self.dxf_scale * end.imag]

    def _dxf_arc(self, center: complex, radius: float, start: complex, end: complex, long: bool = False, clockwise: bool = False):
        angle = cmath.phase((end - center) / (start - center))
        if long:
            if angle < 0:
                angle += 2*cmath.pi
            else:
                angle -= 2*cmath.pi
        n = 2 + 2 * int(abs(angle) * radius * self.dxf_scale)
        print(n)
        radial = cmath.exp((-1j if clockwise else 1j) * (angle/n))
        for i in range(n):
            p = center + (start-center) * (radial ** (i+1))
            self.dxf_pts += ["10", self.dxf_scale * p.real, "20", self.dxf_scale * p.imag]

    def line(self, end: complex):
        self.path += ["L", end.real, end.imag]
        self._dxf_line(self.current, end)
        self.current = end
        self.vertices.append(end)
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
        return self

    def linear_tab(self, end: complex, radius: float = None, left: bool = None, inside: bool = True):
        radius = radius if radius is not None else self.default_linear_tab_radius
        left = left if left is not None else self.default_linear_tab_left
        jigsaw.linear_tab(self.current, end, radius, self, left=left, inside=inside)
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

    def semicircular_tab(self, center: complex, radius: float, inwards: bool):
        middle = center + 1j * (self.current - center)
        end = center - (self.current - center)
        self.circular_tab(center, middle, middle, radius, inwards)
        return self.circular_tab(center, end, end, radius, inwards)
        
    def center(self):
        return sum(self.vertices) / len(self.vertices)

    def __str__(self):
        return " ".join(map(str, self.path))

    def to_dxf(self, name, suffix):
        n = name.split("/")[-1].split("\\")[-1].split(".")[0]
        with open(f"{n}-{suffix}.dxf", "w") as f:
            f.write("0\nSECTION\n2\nENTITIES\n0\nLWPOLYLINE\n")
            f.write(f"90\n{len(self.dxf_pts) // 4}\n70\n1\n")
            f.write("\n".join(map(str, self.dxf_pts)))
            f.write("\n0\nENDSEC\n0\nEOF\n")

def _take(s: str) -> tuple[str, str]:
    m = re.match(r"[A-Z0-9]*", s)
    return m[0], s[len(m[0]) :].strip()

def cuts(cuts: str, globs, tab_radius: float) -> list[Path]:
    result = []
    for part in map(str.strip, cuts.split(";")):
        if not part:
            continue
        start, part = _take(part)
        path = Path(eval(start, globs))
        while part:
            tab = part[0] if part[0] in "<>" else ""
            part = part[len(tab) :].strip()
            point, part = _take(part)
            p = eval(point, globs)
            if tab:
                path.linear_tab(p, left=tab == ">", radius=tab_radius)
            else:
                path.line(p)
        result.append(path)
    return result


class SVGTransformation:
    def __init__(
        self,
        svg: "SVG",
        shift: complex = 0,
        rotate: float = 0,
        mirror: bool = False,
        scale: float = 1,
    ):
        transformations_elements = [
            f"<g transform='translate({shift.real},{shift.imag})'>",
            f"<g transform='rotate({rotate})'>",
            f"<g transform='scale({-scale if mirror else scale},{scale})'>",
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
        self,
        center: complex,
        size: float,
        width: int,
        height: int,
        filename: str,
        suffix: str = "",
    ):
        self.center = center
        self.size = size
        self.width = width
        self.height = height
        if filename.endswith("py"):
            self.filename = filename[:-3] + suffix + ".svg"
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
        
    def basename(self) -> str:
        """Returns the full name, with backslashes doubled."""
        return self.filename.replace("\\", "\\\\")

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

    def mark_all_caps(self, named_points_dicts: list[dict], size: float = 0.2) -> None:
        for named_points_dict in named_points_dicts:
            for name, value in named_points_dict.items():
                if (
                    isinstance(value, complex)
                    or isinstance(value, int)
                    or isinstance(value, float)
                ) and name.isupper():
                    self.mark(value, name, "bc", size)

    def transformation(
        self,
        shift: complex = 0,
        rotate: float = 0,
        mirror: bool = False,
        scale: float = 1,
    ):
        return SVGTransformation(self, shift, rotate, mirror, scale)

    def __str__(self):
        return "\n".join(self.svg) + "\n" + "\n".join(self.marks) + "</g></g></g></svg>"

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        with open(self.filename, "w") as f:
            f.write(str(self))
