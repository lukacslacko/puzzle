import math
import cmath
import numpy


def area(a, b, c):
    return (
        numpy.linalg.det(
            numpy.array([[a.real, a.imag, 1], [b.real, b.imag, 1], [c.real, c.imag, 1]])
        )
        / 2
    )


def angles(start, end, center=0, middle=1):
    print(f"angles({start}, {end}, {center}, {middle})")
    s = start - center
    e = end - center
    m = middle - center
    print(f"s={s}, e={e}, m={m}")
    a = cmath.phase(s / m)
    b = cmath.phase(e / m)
    p = cmath.phase(m)
    print(f"a={a}, b={b}, p={p}")
    return a + p, b + p

def line_intersection(a1, a2, b1, b2):
    x1, y1 = a1.real, a1.imag
    x2, y2 = a2.real, a2.imag
    x3, y3 = b1.real, b1.imag
    x4, y4 = b2.real, b2.imag
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    print(f"d={d}")
    if d == 0:
        return None
    x = (
        (x1 * y2 - y1 * x2) * (x3 - x4)
        - (x1 - x2) * (x3 * y4 - y3 * x4)
    ) / d
    y = (
        (x1 * y2 - y1 * x2) * (y3 - y4)
        - (y1 - y2) * (x3 * y4 - y3 * x4)
    ) / d
    return x + y * 1j

class Draw:
    def __init__(self):
        self.lines = []

    def clines(self, pts):
        for i in range(len(pts) - 1):
            self.cline(pts[i], pts[i + 1])

    def cline(self, a, b):
        self.line(a.real, a.imag, b.real, b.imag)

    def cpoly(self, lines):
        for line in lines:
            self.clines(line)

    def line(self, x1, y1, x2, y2):
        self.lines.append((x1, y1, x2, y2))

    def carc(self, center, radius, a1, a2, npts=48):
        p, q = self.arc(center.real, center.imag, radius, a1, a2, npts)
        return (p[0] + p[1] * 1j, q[0] + q[1] * 1j)

    def arc(self, x, y, r, a1, a2, npts=48):
        da = (a2 - a1) / npts
        for i in range(npts):
            a = a1 + i * da
            x1 = x + r * math.cos(a)
            y1 = y + r * math.sin(a)
            a += da
            x2 = x + r * math.cos(a)
            y2 = y + r * math.sin(a)
            self.line(x1, y1, x2, y2)
        # Returns the first and last points of the arc.
        return (x + r * math.cos(a1), y + r * math.sin(a1)), (
            x + r * math.cos(a2),
            y + r * math.sin(a2),
        )

    def shift(self, x, y, a, r):
        x1 = x + r * math.cos(a)
        y1 = y + r * math.sin(a)
        return x1, y1

    def ctabout(self, p, a, R, r, rho):
        u, v = self.tab_out(p.real, p.imag, a[0], a[1], R, r, rho)
        return u[0] + u[1] * 1j, v[0] + v[1] * 1j

    def ctabin(self, p, a, R, r, rho):
        u, v = self.tab_in(p.real, p.imag, a[0], a[1], R, r, rho)
        return u[0] + u[1] * 1j, v[0] + v[1] * 1j

    def ctab_out(self, p, a, b, R, r, rho, npts=48):
        a1 = cmath.phase(a - p)
        a2 = cmath.phase(b - p)
        u, v = self.tab_out(p.real, p.imag, a1, a2, R, r, rho, npts)
        return u[0] + u[1] * 1j, v[0] + v[1] * 1j

    def tab_out(self, x, y, a1, a2, R, r, rho, npts=48):
        a = R + r
        b = r + rho
        c = R + rho
        alpha = math.acos((b * b + c * c - a * a) / (2 * b * c))
        beta = math.acos((a * a + c * c - b * b) / (2 * a * c))
        gamma = math.acos((a * a + b * b - c * c) / (2 * a * b))
        middle = (a1 + a2) / 2
        #if a2 - a1 <= 2 * beta:
        #    raise ValueError("Tab too wide")
        u, v = self.shift(x, y, middle, a)
        p, q = self.shift(x, y, middle + beta, c)
        s, t = self.shift(x, y, middle - beta, c)
        f, _ = self.arc(x, y, R, a1, middle - beta, npts)
        self.arc(
            s,
            t,
            rho,
            (middle - beta) - math.pi,
            -alpha + (middle - beta) - math.pi,
            npts,
        )
        self.arc(u, v, r, middle - (math.pi - gamma), middle + (math.pi - gamma), npts)
        self.arc(
            p,
            q,
            rho,
            alpha + (middle + beta) - math.pi,
            (middle + beta) - math.pi,
            npts,
        )
        _, l = self.arc(x, y, R, middle + beta, a2, npts)
        return f, l

    def ctab_in(self, p, a, b, R, r, rho, phase=0, npts=48):
        a1 = cmath.phase(a - p)
        a2 = cmath.phase(b - p) + phase
        u, v = self.tab_in(p.real, p.imag, a1, a2, R, r, rho, npts)
        return u[0] + u[1] * 1j, v[0] + v[1] * 1j

    def tab_in(self, x, y, a1, a2, R, r, rho, npts=48):
        a = R - r
        b = r + rho
        c = R - rho
        alpha = math.acos((b * b + c * c - a * a) / (2 * b * c))
        beta = math.acos((a * a + c * c - b * b) / (2 * a * c))
        gamma = math.acos((a * a + b * b - c * c) / (2 * a * b))
        middle = (a1 + a2) / 2
        # if a2 - a1 <= 2 * beta:
        #     raise ValueError("Tab too wide")
        u, v = self.shift(x, y, middle, a)
        p, q = self.shift(x, y, middle + beta, c)
        s, t = self.shift(x, y, middle - beta, c)
        self.arc(x, y, R, a1, middle - beta, npts)
        _, f = self.arc(s, t, rho, middle - beta, middle - beta + math.pi - alpha, npts)
        self.arc(u, v, r, middle + math.pi - gamma, middle + math.pi + gamma, npts)
        l, _ = self.arc(p, q, rho, middle + beta - math.pi + alpha, middle + beta, npts)
        self.arc(x, y, R, middle + beta, a2, npts)
        # self.line(*f,*l)
        return (x + R * math.cos(a1), y + R * math.sin(a1)), (
            x + R * math.cos(a2),
            y + R * math.sin(a2),
        )

    def linear_tab(self, start, end, tab_radius, rounding_radius, npts=48):
        middle = (start + end) / 2
        normal = (end - start) / abs(end - start) * 1j
        d = math.sqrt(
            (tab_radius + rounding_radius) ** 2 - (tab_radius - rounding_radius) ** 2
        )

        def xy(x, y):
            return middle + (y + 1j * x) * normal

        arcs = []

        arcs.append(
            self.carc(
                xy(d, rounding_radius),
                rounding_radius,
                *angles(xy(d, 0), xy(0, tab_radius), xy(d, rounding_radius), xy(0, 0)),
            )
        )
        arcs.append(
            self.carc(
                xy(0, tab_radius),
                tab_radius,
                *angles(
                    xy(d, rounding_radius),
                    xy(-d, rounding_radius),
                    xy(0, tab_radius),
                    xy(0, 2 * tab_radius),
                ),
            )
        )
        arcs.append(
            self.carc(
                xy(-d, rounding_radius),
                rounding_radius,
                *angles(
                    xy(0, tab_radius), xy(-d, 0), xy(-d, rounding_radius), xy(0, 0)
                ),
            )
        )
        self.cline(start, arcs[0][0])
        self.cline(end, arcs[-1][-1])
        for i in range(len(arcs) - 1):
            self.cline(arcs[i][-1], arcs[i + 1][0])

    def dxf(self, f):
        if isinstance(f, str):
            with open(f, "w") as f:
                self.dxf_to_file(f)
        else:
            self.dxf_to_file(f)

    def dxf_to_file(self, f):
        self.dxf_header(f)
        for line in self.lines:
            self.dxf_line(*line, f)
        self.dxf_footer(f)

    def dxf_line(self, x1, y1, x2, y2, f):
        f.write("0\n")
        f.write("LINE\n")
        f.write("8\n")
        f.write("Polygon\n")
        f.write("10\n")
        f.write(f"{x1}\n")
        f.write("20\n")
        f.write(f"{y1}\n")
        f.write("11\n")
        f.write(f"{x2}\n")
        f.write("21\n")
        f.write(f"{y2}\n")

    def dxf_header(self, f):
        f.write("0\n")
        f.write("SECTION\n")
        f.write("2\n")
        f.write("ENTITIES\n")

    def dxf_footer(self, f):
        f.write("0\n")
        f.write("ENDSEC\n")
        f.write("0\n")
        f.write("EOF\n")

class DXF:
    def __init__(self, basename):
        self.basename = basename
        self.draw = Draw()
    
    def __enter__(self):
        return self.draw
    
    def __exit__(self, type, value, traceback):
        self.draw.dxf(f"{self.basename}.dxf")
        return False
