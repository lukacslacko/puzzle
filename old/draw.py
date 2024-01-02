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

def dot(a, b):
    return a.real * b.real + a.imag * b.imag

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

    def arc_c(self, center, vstart, vend, prev, dir=1):
        p = cmath.phase((vend / vstart)**dir)
        print(f"----- {p}")
        if p < 0:
            p += 2 * math.pi
        print(f"..... {p}")
        e = cmath.exp(1j * p / 24)
        for i in range(24):
            nxt = center + vstart * (e ** (dir * (i+1)))
            self.cline(prev, nxt)
            prev = nxt
        return prev
    
    def along(self, center, start, radius, tab_radius, rounding_radius):
        vs = start - center
        return center + vs / abs(vs) * radius

    def out_tab(self, center, start, end, middle, radius, tab_radius, rounding_radius, prev):
        vs = start - center
        ve = end - center
        vs /= abs(vs)
        ve /= abs(ve)
        vm = (vs + ve) / 2
        vm /= abs(vm)
        if dot(vm, middle - center) < 0:
            vm *= -1
        vs *= radius
        ve *= radius
        a = radius + rounding_radius
        b = radius + tab_radius
        c = tab_radius + rounding_radius
        alpha = math.acos((b * b + c * c - a * a) / (2 * b * c))
        beta = math.acos((a * a + c * c - b * b) / (2 * a * c))
        gamma = math.acos((a * a + b * b - c * c) / (2 * a * b))
        vu = vm * cmath.exp(-1j * gamma) * radius
        vq = vm * cmath.exp(-1j * gamma) * a 
        vp = vm * b
        vv = vm * cmath.exp(1j * gamma) * radius
        vr = vm * cmath.exp(1j * gamma) * a 
        vqp = vp - vq
        vw = vq + vqp / abs(vqp) * rounding_radius
        vrp = vp - vr
        vt = vr + vrp / abs(vrp) * rounding_radius

        prev = self.arc_c(center, vs, vu, prev)
        prev = self.arc_c(center + vq, vu-vq, vw-vq, prev, dir=-1)
        prev = self.arc_c(center + vp, vw-vp, vt-vp, prev)
        prev = self.arc_c(center + vr, vt-vr, vv-vr, prev, dir=-1)
        prev = self.arc_c(center, vv, ve, prev)
        return prev

    def in_tab(self, center, start, end, middle, radius, tab_radius, rounding_radius, prev):
        vs = start - center
        ve = end - center
        vs /= abs(vs)
        ve /= abs(ve)
        vm = (vs + ve) / 2
        vm /= abs(vm)
        if dot(vm, middle - center) < 0:
            vm *= -1
        vs *= radius
        ve *= radius
        a = radius - rounding_radius
        b = radius - tab_radius
        c = tab_radius + rounding_radius
        alpha = math.acos((b * b + c * c - a * a) / (2 * b * c))
        beta = math.acos((a * a + c * c - b * b) / (2 * a * c))
        gamma = math.acos((a * a + b * b - c * c) / (2 * a * b))
        vu = vm * cmath.exp(-1j * gamma) * radius
        vq = vm * cmath.exp(-1j * gamma) * a / radius
        vp = vm * b
        vv = vm * cmath.exp(1j * gamma) * radius
        vr = vm * cmath.exp(1j * gamma) * a / radius
        vqp = vp - vq
        vs = vq + vqp / abs(vqp) * rounding_radius
        vrp = vp - vr
        vt = vr + vrp / abs(vrp) * rounding_radius

        prev = self.arc_c(center, vs, vu, prev)
        prev = self.arc_c(center, vu, vs, prev)
        prev = self.arc_c(center, vs, vt, prev, dir=-1)
        prev = self.arc_c(center, vt, vv, prev)
        prev = self.arc_c(center, vv, ve, prev)
        return prev
    
    def tab_line(self, start, end, radius, tab_radius, rounding_radius, dir=1):
        v = end - start
        v /= abs(v)
        m = (start + end) / 2
        n = v * 1j * dir
        d = cmath.sqrt((tab_radius + rounding_radius) ** 2 - (tab_radius - rounding_radius) ** 2)
        a = m - d*v
        b = m + d*v
        p = m + tab_radius*n
        q = a + rounding_radius*n
        r = b + rounding_radius*n
        vqp = p - q
        u = q + vqp / abs(vqp) * rounding_radius
        vrp = p - r
        t = r + vrp / abs(vrp) * rounding_radius
        self.cline(start, a)
        prev = self.arc_c(q, a-q, u-q, a, dir=dir)
        prev = self.arc_c(p, u-p, t-p, prev, dir=-dir)
        prev = self.arc_c(r, t-r, b-r, prev, dir=dir)
        self.cline(b, end)
        return end
    
    def svg(self, f):
        if isinstance(f, str):
            with open(f, "w") as f:
                self.svg_to_file(f)
        else:
            self.svg_to_file(f)

    def svg_to_file(self, f):
        f.write("<svg>")
        for line in self.lines:
            f.write(f"<line x1='{line[0]}' y1='{line[1]}' x2='{line[2]}' y2='{line[3]}' stroke='black'/>")
        f.write("</svg>")

    def dxf(self, f):
        if isinstance(f, str):
            with open(f, "w") as f:
                self.dxf_to_file(f)
        else:
            self.dxf_to_file(f)

    def dxf_to_file(self, f):
        self.dxf_header(f)
        for line in self.lines:
            self.dxf_line(*[c*100 for c in line], f)
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
        self.draw.svg(f"{self.basename}.svg")
        return False
