from aufmassZeile import AufmassZeile
from component import *


class Room:

    def __init__(self, name, level, data, x, y,
                 components=None, uid=None,
                 positions=None):

        if positions is None:
            positions = dict()
        self.positions = positions

        self.uid = uid

        if components is None:
            components = dict()
        self.components = components

        self.level = level
        self.data = data
        self.name = name
        self.y = y
        self.x = x

    def __str__(self):
        return f"{self.level}, {self.name}"

    def data_to_aufmasszeile(self, tag: str):
        """
        Turns a Datapoint by a given tag into an Aufmasszeile
        :param tag: tag for corresponding Datapoint
        :return: Aufmasszeile
        """
        return AufmassZeile(stichwort=self.level + ", " + self.name, text=tag + ", " + self.name,
                            aufmass=str(self.data[tag]).split()[0])

    def write_to_xml(self, root) :
        """
        Writes the whole room with each Datapoint to a given root Element.
        Calls write_to_xml() on all components
        :param root: root XML Element
        """
        for tag in self.data:
            AufmassZeile(stichwort=self.level + ", " + self.name, text=tag + ", " + self.name,
                         aufmass=str(self.data[tag]).split()[0]).write_to_xml(root)
        for component in self.components.values():
            component.write_to_xml(root)

    def create_sums(self):
        """
        Creates all the sums for the room like wall area
        """
        self.data['Deckenfläche'] = self.data['Bodenfläche']
        self.data['Wandfläche'] = self.create_wall_area()

    def create_wall_area(self) -> str:
        """
        Creates wall area as a String in format: 2*(width*length)*height
        where width, height and length are the max of the room
        :return: String equation of wall area
        """
        walls = [component for component in self.components.values() if component.typ == 'Wand']
        breite = float()
        laenge = float()
        for i, line in enumerate(walls):
            if i == 0:
                breite = sum([wall.breite for wall in walls if abs(wall.vector.dot(line.vector)) > 0.1]) / 2
            if i == 1:
                laenge = sum([wall.breite for wall in walls if abs(wall.vector.dot(line.vector)) > 0.1]) / 2
            if i > 1:
                break
        return "2*({}+{})*{}".format(round(breite, 2), round(laenge, 2), round(walls[0].hoehe, 2))
