import math


class Draw:
    def __init__(self):
        self.lines = []

    def line(self, x1, y1, x2, y2):
        self.lines.append((x1, y1, x2, y2))

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

    def tab_out(self, x, y, a1, a2, R, r, rho, npts=48):
        a = R + r
        b = r + rho
        c = R + rho
        alpha = math.acos((b * b + c * c - a * a) / (2 * b * c))
        beta = math.acos((a * a + c * c - b * b) / (2 * a * c))
        gamma = math.acos((a * a + b * b - c * c) / (2 * a * b))
        middle = (a1 + a2) / 2
        if a2 - a1 <= 2 * beta:
            raise ValueError("Tab too wide")
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

    def tab_in(self, x, y, a1, a2, R, r, rho, npts=48):
        a = R - r
        b = r + rho
        c = R - rho
        alpha = math.acos((b * b + c * c - a * a) / (2 * b * c))
        beta = math.acos((a * a + c * c - b * b) / (2 * a * c))
        gamma = math.acos((a * a + b * b - c * c) / (2 * a * b))
        middle = (a1 + a2) / 2
        if a2 - a1 <= 2 * beta:
            raise ValueError("Tab too wide")
        u, v = self.shift(x, y, middle, a)
        p, q = self.shift(x, y, middle + beta, c)
        s, t = self.shift(x, y, middle - beta, c)
        self.arc(x, y, R, a1, middle - beta, npts)
        _,f=self.arc(s, t, rho, middle - beta, middle - beta + math.pi - alpha, npts)
        self.arc(u, v, r, middle + math.pi - gamma, middle + math.pi + gamma, npts)
        l,_=self.arc(p, q, rho, middle + beta - math.pi + alpha, middle + beta, npts)
        self.arc(x, y, R, middle + beta, a2, npts)
        #self.line(*f,*l)
        return (x + R * math.cos(a1), y + R * math.sin(a1)), (
            x + R * math.cos(a2),
            y + R * math.sin(a2),
        )

    def dxf(self, f):
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
