import math

from aufmassZeile import AufmassZeile


class PolyLine:
    def __init__(self, poly_id=None, uid=None, symbol=None, points=None):
        self.breite = None
        self.hoehe = None
        self.poly_id = poly_id
        self.uid = uid
        self.symbol = symbol
        self.points = points
        if points is None:
            points = list()

    def to_aufmass_zeile(self):
        if self.breite is None or self.hoehe is None:
            self.create_poly()
        return AufmassZeile(text='Benutzerdefinierter Bereich', aufmass="{:.2f}*{:.2f}".format(self.breite, self.hoehe), stichwort="Polylinie")

    def create_poly(self):
        self.breite = distance_num(self.points[0][0], self.points[1][0], self.points[0][1], self.points[1][0])
        self.hoehe = distance_num(self.points[1][0], self.points[2][0], self.points[1][1], self.points[2][0])


def distance_num(x1, x2, y1, y2):
    return math.sqrt((float(x2) - float(x1)) ** 2 + (float(y2) - float(y1)) ** 2)
