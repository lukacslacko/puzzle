import cmath
import math
import numpy

Path = "svg.Path"

def line_intersection(
    start1: complex, end1: complex, start2: complex, end2: complex
) -> complex:
    x1, y1 = start1.real, start1.imag
    x2, y2 = end1.real, end1.imag
    x3, y3 = start2.real, start2.imag
    x4, y4 = end2.real, end2.imag
    x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
        (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    )
    y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
        (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    )
    return complex(x, y)


def along(start: complex, end: complex, distance: float) -> complex:
    return start + (end - start) * distance / abs(end - start)

def perpendicular_projection(start: complex, end: complex, point: complex) -> complex:
    v_point = point - start
    v_end = end - start
    v_end /= abs(v_end)
    return along(start, end, (v_point/v_end).real)

def area(a, b, c):
    return (
        numpy.linalg.det(
            numpy.array([[a.real, a.imag, 1], [b.real, b.imag, 1], [c.real, c.imag, 1]])
        )
        / 2
    )

def linear_tab(
    start: complex, end: complex, radius: float, path: Path, *, left: bool, dxf_offset: float = 0.1, inside: bool = True, small_ratio: float=0.3
) -> complex:
    dxf_offset *= 1 if inside else -1
    dxf_offset /= path.dxf_scale
    middle = (start + end) / 2
    horizontal = end - start
    horizontal /= abs(horizontal)
    vertical = horizontal * (1j if left else -1j)
    tab_center = middle + vertical * (radius + dxf_offset)
    rounding_radius = radius * small_ratio
    touch_distance = cmath.sqrt(
        (radius + rounding_radius) ** 2 - (radius - rounding_radius) ** 2
    )
    rounding_radius += dxf_offset
    radius -= dxf_offset
    start_touch_point = middle - horizontal * touch_distance
    end_touch_point = middle + horizontal * touch_distance
    start_rounding_center = start_touch_point + vertical * rounding_radius
    end_rounding_center = end_touch_point + vertical * rounding_radius

    start_to_tab = along(start_rounding_center, tab_center, rounding_radius)
    end_to_tab = along(end_rounding_center, tab_center, rounding_radius)

    print("line to start touch")
    path.line(start_touch_point)
    print("done")
    path.arc(
        rounding_radius,
        start_to_tab,
        sweep=left,
    )
    
    path._dxf_arc(start_rounding_center, rounding_radius, start_touch_point, start_to_tab, long=False, clockwise=False)
    path._dxf_arc(tab_center, radius, start_to_tab, end_to_tab, long=True, clockwise=False)
    path._dxf_arc(end_rounding_center, rounding_radius, end_to_tab, end_touch_point, long=False, clockwise=False)
    
    path.arc(
        radius,
        end_to_tab,
        large_arc=True,
        sweep=not left,
    )
    path.arc(rounding_radius, end_touch_point, sweep=left)
    path.line(end)
    return end


def circular_tab(
    center: complex,
    start_direction: complex,
    end_direction: complex,
    towards: complex,
    corner_radius: float,
    radius: float,
    *,
    inwards: bool,
    path: Path
) -> complex:
    start_vector = start_direction - center
    start_vector /= abs(start_vector)
    end_vector = end_direction - center
    end_vector /= abs(end_vector)
    middle_vector = (start_vector + end_vector) / 2
    middle_vector /= abs(middle_vector)
    towards_vector = towards - center
    dot_product = (
        towards_vector.real * middle_vector.real
        + towards_vector.imag * middle_vector.imag
    )
    if dot_product < 0:
        middle_vector *= -1
    rounding_radius = radius * 0.2
    a = corner_radius - rounding_radius if inwards else corner_radius + rounding_radius
    b = corner_radius - radius if inwards else corner_radius + radius
    c = radius + rounding_radius
    gamma = cmath.acos((a**2 + b**2 - c**2) / (2 * a * b))
    tab_center = center + middle_vector * b
    start_touch_point = center + middle_vector * corner_radius * cmath.exp(-1j * gamma)
    start_rounding_center = center + middle_vector * a * cmath.exp(-1j * gamma)
    end_touch_point = center + middle_vector * corner_radius * cmath.exp(1j * gamma)
    end_rounding_center = center + middle_vector * a * cmath.exp(1j * gamma)
    path.arc(corner_radius, start_touch_point)
    path.arc(rounding_radius, along(start_rounding_center, tab_center, rounding_radius), sweep=inwards)
    path.arc(
        radius,
        along(end_rounding_center, tab_center, rounding_radius),
        large_arc=True,
        sweep=not inwards,
    )
    path.arc(rounding_radius, end_touch_point, sweep=inwards)
    path.arc(corner_radius, along(center, end_direction, corner_radius))
    return along(center, end_direction, corner_radius)
