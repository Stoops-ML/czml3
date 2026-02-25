from copy import deepcopy

import numpy as np
from colourings import Colour

from .properties import (
    Box,
    Color,
    Corridor,
    Cylinder,
    Ellipse,
    Ellipsoid,
    Material,
    Path,
    Point,
    Polygon,
    Polyline,
    Position,
    PositionList,
    PositionListOfLists,
    Rectangle,
    Wall,
)


def create_svgs(
    position: Position | None,
    point: Point | None,
    rectangle: Rectangle | None,
    box: Box | None,
    polyline: Polyline | None,
    corridor: Corridor | None,
    wall: Wall | None,
    path: Path | None,
    polygon: Polygon | None,
    ellipse: Ellipse | None,
    ellipsoid: Ellipsoid | None,
    cylinder: Cylinder | None,
) -> tuple[list[str], float, float, float, float]:
    factor = 100  # svg requires resolution greater than difference between most LLA points, therefore use factor
    start_num = 9999999.0
    x_min, x_max, y_min, y_max = start_num, -start_num, start_num, -start_num

    def calc_bounds(
        x_min_current: float,
        x_max_current: float,
        y_min_current: float,
        y_max_current: float,
        x_min_contender: float,
        x_max_contender: float,
        y_min_contender: float,
        y_max_contender: float,
    ) -> tuple[float, float, float, float]:
        if x_min_contender < x_min_current:
            x_min_current = x_min_contender
        if x_max_contender > x_max_current:
            x_max_current = x_max_contender
        if y_min_contender < y_min_current:
            y_min_current = y_min_contender
        if y_max_contender > y_max_current:
            y_max_current = y_max_contender
        return x_min_current, x_max_current, y_min_current, y_max_current

    svg_elements = []
    if (
        point
        and isinstance(point, Point)
        and position
        and isinstance(position, Position | PositionList | PositionListOfLists)
    ):
        deg_lon, deg_lat = position_to_geodetic(position, factor)
        c = extract_colour_from_color(point.color)
        svg_elements.append(
            f'<circle fill="{c}" cx="{deg_lon}" cy="{deg_lat}" r="1" />'
        )
        x_min, x_max, y_min, y_max = calc_bounds(
            x_min, x_max, y_min, y_max, deg_lon, deg_lon, deg_lat, deg_lat
        )
    if rectangle and isinstance(rectangle, Rectangle):
        if rectangle.coordinates.wsen:
            v = np.rad2deg(rectangle.coordinates.wsen).tolist()
        elif rectangle.coordinates.wsenDegrees:
            v = rectangle.coordinates.wsenDegrees
        deg_lon0, deg_lat0, deg_lon1, deg_lat1 = [x * factor for x in v]
        points = f"{deg_lon0},{deg_lat0} {deg_lon0},{deg_lat1} {deg_lon1},{deg_lat1} {deg_lon1},{deg_lat0} {deg_lon0},{deg_lat0}"
        c = extract_colour_from_color(rectangle.material.solidColor.color)
        svg_elements.append(f'<polyline stroke="{c}" fill="none" points="{points}" />')
        x_min, x_max, y_min, y_max = calc_bounds(
            x_min, x_max, y_min, y_max, deg_lon0, deg_lon1, deg_lat0, deg_lat1
        )
    if (
        box
        and isinstance(box, Box)
        and position
        and isinstance(position, Position | PositionList | PositionListOfLists)
    ):
        deg_lon0, deg_lat0 = position_to_geodetic(position, factor)
        c = extract_colour_from_material(box.material)
        x_length, y_length = box.dimensions.cartesian.values
        deg_lon1 = deg_lon0 + x_length / 111111
        deg_lat1 = deg_lat0 + y_length / 111111
        points = f"{deg_lon0},{deg_lat0} {deg_lon0},{deg_lat1} {deg_lon1},{deg_lat1} {deg_lon1},{deg_lat0} {deg_lon0},{deg_lat0}"
        svg_elements.append(f'<polyline stroke="{c}" fill="none" points="{points}" />')
        x_min, x_max, y_min, y_max = calc_bounds(
            x_min, x_max, y_min, y_max, deg_lon, deg_lon, deg_lat, deg_lat
        )
    if polyline and isinstance(polyline, Polyline):
        dd_coords = position_to_geodetic(polyline.positions, factor)
        coords = [
            f"{dd_coords[i]},{dd_coords[i + 1]}" for i in range(0, len(dd_coords), 2)
        ]
        d = f"M{coords[0]} L{' L'.join(coords[1:])} Z"
        c = extract_colour_from_material(polyline.material)
        svg_elements.append(f'<path fill="{c}" d="{d}"/>')
        x_min, x_max, y_min, y_max = calc_bounds(
            x_min,
            x_max,
            y_min,
            y_max,
            min(dd_coords[::2]),
            max(dd_coords[::2]),
            min(dd_coords[1::2]),
            max(dd_coords[1::2]),
        )
    if corridor and isinstance(corridor, Corridor):
        dd_coords = position_to_geodetic(corridor.positions, factor)
        coords = [
            f"{dd_coords[i]},{dd_coords[i + 1]}" for i in range(0, len(dd_coords), 2)
        ]
        d = f"M{coords[0]} L{' L'.join(coords[1:])} Z"
        c = extract_colour_from_material(corridor.material)
        svg_elements.append(f'<path fill="{c}" d="{d}"/>')
        x_min, x_max, y_min, y_max = calc_bounds(
            x_min,
            x_max,
            y_min,
            y_max,
            min(dd_coords[::2]),
            max(dd_coords[::2]),
            min(dd_coords[1::2]),
            max(dd_coords[1::2]),
        )
    if wall and isinstance(wall, Wall):
        dd_coords = position_to_geodetic(wall.positions, factor)
        coords = [
            f"{dd_coords[i]},{dd_coords[i + 1]}" for i in range(0, len(dd_coords), 2)
        ]
        d = f"M{coords[0]} L{' L'.join(coords[1:])} Z"
        c = extract_colour_from_material(wall.material)
        svg_elements.append(f'<path fill="{c}" d="{d}"/>')
        x_min, x_max, y_min, y_max = calc_bounds(
            x_min,
            x_max,
            y_min,
            y_max,
            min(dd_coords[::2]),
            max(dd_coords[::2]),
            min(dd_coords[1::2]),
            max(dd_coords[1::2]),
        )
    if (
        path
        and isinstance(path, Path)
        and position
        and isinstance(position, Position | PositionList | PositionListOfLists)
    ):
        dd_coords = position_to_geodetic(position, factor)
        coords = [
            f"{dd_coords[i]},{dd_coords[i + 1]}" for i in range(0, len(dd_coords), 2)
        ]
        d = f"M{coords[0]} L{' L'.join(coords[1:])} Z"
        c = extract_colour_from_material(path.material)
        svg_elements.append(f'<path fill="{c}" d="{d}"/>')
        x_min, x_max, y_min, y_max = calc_bounds(
            x_min,
            x_max,
            y_min,
            y_max,
            min(dd_coords[::2]),
            max(dd_coords[::2]),
            min(dd_coords[1::2]),
            max(dd_coords[1::2]),
        )
    if polygon and isinstance(polygon, Polygon):
        dd_coords = position_to_geodetic(polygon.positions, factor)
        coords = " ".join(
            [f"{dd_coords[i]},{dd_coords[i + 1]}" for i in range(0, len(dd_coords), 2)]
        )
        c = extract_colour_from_material(polygon.material)
        svg_elements.append(f'<polygon style="fill:{c};" points="{coords}" />')
        x_min, x_max, y_min, y_max = calc_bounds(
            x_min,
            x_max,
            y_min,
            y_max,
            min(dd_coords[::2]),
            max(dd_coords[::2]),
            min(dd_coords[1::2]),
            max(dd_coords[1::2]),
        )
        if polygon.holes and isinstance(polygon.holes, PositionListOfLists):
            dd_coords = position_to_geodetic(polygon.holes, factor)
            coords = " ".join(
                [
                    f"{dd_coords[i]},{dd_coords[i + 1]}"
                    for i in range(0, len(dd_coords), 2)
                ]
            )
            svg_elements.append(f'<polygon style="fill:white;" points="{coords}" />')
    if (
        ellipse
        and isinstance(ellipse, Ellipse)
        and position
        and isinstance(position, Position | PositionList | PositionListOfLists)
    ):
        deg_lon, deg_lat = position_to_geodetic(position, factor)
        c = extract_colour_from_material(ellipse.material)
        deg_rotate = 0 if ellipse.rotation is None else ellipse.rotation
        if ellipse.semiMajorAxis > ellipse.semiMinorAxis:
            rx = 1
            ry = ellipse.semiMinorAxis / ellipse.semiMajorAxis
        else:
            rx = ellipse.semiMajorAxis / ellipse.semiMinorAxis
            ry = 1
        svg_elements.append(
            f'<ellipse fill="{c}" cx="{deg_lon}" cy="{deg_lat}" rx="{rx}" ry="{ry}" transform="rotate({deg_rotate}, {deg_lon}, {deg_lat})" />'
        )
        x_min, x_max, y_min, y_max = calc_bounds(
            x_min, x_max, y_min, y_max, deg_lon, deg_lon, deg_lat, deg_lat
        )
    if (
        ellipsoid
        and isinstance(ellipsoid, Ellipsoid)
        and position
        and isinstance(position, Position | PositionList | PositionListOfLists)
    ):
        deg_lon, deg_lat = position_to_geodetic(position, factor)
        c = extract_colour_from_material(ellipsoid.material)
        semiMinorAxis, semiMajorAxis = ellipsoid.radii.cartesian.values[:2]
        semiMajorAxis = 0.1 if semiMajorAxis == 0 else semiMajorAxis
        semiMinorAxis = 0.1 if semiMinorAxis == 0 else semiMinorAxis
        if semiMajorAxis > semiMinorAxis:
            rx = 1
            ry = semiMinorAxis / semiMajorAxis
        else:
            rx = semiMajorAxis / semiMinorAxis
            ry = 1
        svg_elements.append(
            f'<ellipse fill="{c}" cx="{deg_lon}" cy="{deg_lat}" rx="{rx}" ry="{ry}" />'
        )
        x_min, x_max, y_min, y_max = calc_bounds(
            x_min, x_max, y_min, y_max, deg_lon, deg_lon, deg_lat, deg_lat
        )
    if (
        cylinder
        and isinstance(cylinder, Cylinder)
        and position
        and isinstance(position, Position | PositionList | PositionListOfLists)
    ):
        deg_lon, deg_lat = position_to_geodetic(position, factor)
        c = extract_colour_from_material(cylinder.material)
        if cylinder.topRadius > cylinder.bottomRadius:
            r_top = 1
            r_bottom = cylinder.topRadius / cylinder.bottomRadius
        else:
            r_top = cylinder.bottomRadius / cylinder.topRadius
            r_bottom = 1
        svg_elements.append(
            f'<circle fill="{c}" cx="{deg_lon}" cy="{deg_lat}" r="{r_top}" />'
        )
        svg_elements.append(
            f'<circle fill="{c}" cx="{deg_lon}" cy="{deg_lat}" r="{r_bottom}" />'
        )
        x_min, x_max, y_min, y_max = calc_bounds(
            x_min, x_max, y_min, y_max, deg_lon, deg_lon, deg_lat, deg_lat
        )

    return svg_elements, x_min, x_max, y_min, y_max


def extract_colour_from_material(material: Material | None) -> str:
    if material is None or not isinstance(material, Material):
        return extract_colour_from_color(None)
    return extract_colour_from_color(material.solidColor.color)


def extract_colour_from_color(color: Color | None) -> str:
    if color is None or not isinstance(color, Color):
        c = list(Colour("black").rgba)
    elif color.rgba:
        c = deepcopy(color.rgba.values)
    elif color.rgbaf:
        c = list(Colour(rgbaf=color.rgbaf).rgba)
    else:
        c = list(Colour("black").rgba)
    c[3] /= 255
    return f"rgba({','.join(map(str, c))})"


def position_to_geodetic(
    position: Position | PositionList | PositionListOfLists, factor
) -> list[float]:
    if isinstance(position, PositionListOfLists) and position.cartesian:
        raise NotImplementedError
        from pyproj import Transformer

        transformer = Transformer.from_crs("EPSG:4978", "EPSG:4326", always_xy=True)
        lon, lat, alt = transformer.transform(x, y, z)
        v = [x / 111111 for x in position.cartesian.values]
    if isinstance(position, PositionListOfLists) and position.cartographicDegrees:
        raise NotImplementedError
        v = position.cartographicDegrees.values
    if isinstance(position, PositionListOfLists) and position.cartographicRadians:
        raise NotImplementedError
        v = np.rad2deg(position.cartographicRadians.values).tolist()
    elif position.cartesian:
        raise NotImplementedError
        v = position.cartesian.values
    elif position.cartographicDegrees:
        v = position.cartographicDegrees.values
    elif position.cartographicRadians:
        v = np.rad2deg(position.cartographicRadians.values).tolist()

    if len(v) % 4 == 0:
        return [
            x * factor for i, x in enumerate(v) if (i + 1) % 4 != 0 or (i + 1) % 3 != 0
        ]
    elif len(v) % 3 == 0:
        return [x * factor for i, x in enumerate(v) if (i + 1) % 3 != 0]
    else:
        raise ValueError


def create_bounds(
    x_min: float, x_max: float, y_min: float, y_max: float
) -> tuple[float, float, float, float, float, float, float, float]:
    if x_min == x_max and y_min == y_max:
        x_min *= 0.99
        y_min *= 0.99
        x_max *= 1.01
        y_max *= 1.01
    else:
        expand = 0.04
        widest_part = max([x_max - x_min, y_max - y_min])
        expand_amount = widest_part * expand
        x_min -= expand_amount
        y_min -= expand_amount
        x_max += expand_amount
        y_max += expand_amount
    dx = x_max - x_min
    dy = y_max - y_min
    width = min([max([100.0, dx]), 300])
    height = min([max([100.0, dy]), 300])
    return x_min, x_max, y_min, y_max, dx, dy, width, height


def make_svg(
    x_min: float,
    y_min: float,
    y_max: float,
    dx: float,
    dy: float,
    width: float,
    height: float,
    svg_elements: list[str],
) -> str:
    svg_start = f'<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" width="{width}" height="{height}" viewBox="{x_min} {y_min} {dx} {dy}"><g transform="matrix(1,0,0,-1,0,{y_min + y_max})">'
    return "".join((svg_start, "".join(svg_elements), "</g></svg>"))
