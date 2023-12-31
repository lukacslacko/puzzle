import cmath

class Path:
    def __init__(self):
        self.path = []

    def move(self, start: complex):
        self.path += ["M", start.real, start.imag]

    def line(self, end: complex):
        self.path += ["L", end.real, end.imag]

    def arc(self, radius: float, end: complex, large_arc: bool = False, sweep: bool = True):
        self.path += ["A", radius, radius, 0, int(large_arc), int(sweep), end.real, end.imag]

    def __str__(self):
        return " ".join(map(str, self.path))

class SVG:
    def __init__(self, center: complex, size: float, width: int, height: int, filename: str):
        self.center = center
        self.size = size
        self.width = width
        self.height = height
        self.filename = filename
        self.svg = []
        self.svg.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
        self.svg.append('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="%d" height="%d">' % (width, height))
        self.svg.append('<g transform="translate(%d,%d) scale(%d,%d)">' % (width / 2, height / 2, width / 2, height / 2))
        self.svg.append('<g transform="translate(%f,%f) scale(%f)">' % (center.real, center.imag, 1/size))
        self.svg.append('<g transform="translate(%f,%f)">' % (-center.real, -center.imag))

    def draw_path(self, path: str, fill: str, stroke: str, stroke_width: float):
        self.svg.append(f"<path d='{path}' fill='{fill}' stroke='{stroke}' stroke-width='{stroke_width}' />")

    def mark(self, point: complex, name: str, align: str = "tl", size: float = 0.2):
        baseline = {"t": "auto", "m": "middle", "b": "hanging"}[align[0]]
        anchor = {"l": "end", "c": "middle", "r": "start"}[align[1]] 
        font_size = size
        self.svg.append('<text x="%f" y="%f" text-anchor="%s" dominant-baseline="%s" font-size="%f">%s</text>' % (point.real, point.imag, anchor, baseline, font_size, name))

    def __str__(self):
        self.svg.append('</g>')
        self.svg.append('</g>')
        self.svg.append('</g>')
        self.svg.append('</svg>')
        return "\n".join(self.svg)

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        with open(self.filename, "w") as f:
            f.write(str(self))
