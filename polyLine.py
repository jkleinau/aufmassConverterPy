import math

from aufmassZeile import AufmassZeile


class PolyLine:
    def __init__(self, poly_id=None, uid=None, symbol=None, points=None, wallIndex=None):
        self.wallIndex = wallIndex
        self.breite = None
        self.hoehe = None
        self.poly_id = poly_id
        self.uid = uid
        self.symbol = symbol
        self.points = points
        if points is None:
            self.points = list()

    def to_aufmass_zeile(self, component=None):
        if self.breite is None or self.hoehe is None:
            self.create_poly()
        return AufmassZeile(
            text=f'Benutzerdefinierter Bereich von {component}' if component is not None else 'Benutzerdefinierter Bereich',
            aufmass="{:.2f}*{:.2f}".format(self.breite, self.hoehe),
            stichwort=f"Polylinie in {component.room}" if component is not None else "Polyline")

    def create_poly(self):
        self.breite = distance_num(self.points[1][0], self.points[2][0], self.points[1][1], self.points[2][1])
        self.hoehe = distance_num(self.points[0][0], self.points[1][0], self.points[0][1], self.points[1][1])

    def __str__(self):
        return f'Benutzerdefinierter Bereich: {self.breite}*{self.hoehe}'


def distance_num(x1, x2, y1, y2):
    return math.sqrt((float(x2) - float(x1)) ** 2 + (float(y2) - float(y1)) ** 2)
