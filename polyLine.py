import math

from aufmassZeile import AufmassZeile
from component import Component


class PolyLine:

    def __init__(self, poly_id=None, uid=None, symbol=None, points=None,
                 wallIndex=None):
        """
            Constructor
        :param poly_id: ID for Polyline
        :param uid: Unique Id from XML
        :param symbol: smybol ID from XML
        :param points: List of points to construct Polyline
        :param wallIndex: Index of corresponding wall
        """
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
        """
        Turns Polyline to Aufmasszeile
        :param component: corresponding component to the Polyline
        :return: Aufmasszeile which represents the Polyline
        """
        if self.breite is None or self.hoehe is None:
            self.create_poly()
        return AufmassZeile(
            text=f'Benutzerdefinierter Bereich von {component}' if component is not None else 'Benutzerdefinierter Bereich',
            aufmass="{:.2f}*{:.2f}".format(self.breite, self.hoehe),
            stichwort=f"Polylinie in {component.room}" if component is not None else "Polyline")

    def create_poly(self) -> None:
        """
        Calculates width and height from the given Points in class variables
        """
        self.breite = distance_num(self.points[1][0], self.points[2][0], self.points[1][1], self.points[2][1])
        self.hoehe = distance_num(self.points[0][0], self.points[1][0], self.points[0][1], self.points[1][1])

    def __str__(self):
        return f'Benutzerdefinierter Bereich: {self.breite}*{self.hoehe}'


def distance_num(x1: str, x2: str, y1: str, y2: str) -> float:
    """
    Calculates distance between two points
    :param x1: X1
    :param x2: X2
    :param y1: Y1
    :param y2: Y2
    :return: Distance between two points
    """
    return math.sqrt((float(x2) - float(x1)) ** 2 + (float(y2) - float(y1)) ** 2)
