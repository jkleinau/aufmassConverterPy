from aufmassZeile import AufmassZeile
from component import *


class Room:

    def __init__(self, name, level, data, x, y, components=None, uid=None, positions=None):

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

    def data_to_aufmasszeile(self, tag):
        return AufmassZeile(stichwort=self.level + ", " + self.name, text=tag + ", " + self.name,
                            aufmass=str(self.data[tag]).split()[0])

    def write_to_xml(self, root):
        for tag in self.data:
            AufmassZeile(stichwort=self.level + ", " + self.name, text=tag + ", " + self.name,
                         aufmass=str(self.data[tag]).split()[0]).write_to_xml(root)
        for component in self.components.values():
            component.write_to_xml(root)

    def create_sums(self):
        self.data['Deckenfläche'] = self.data['Bodenfläche']
        self.data['Wandfläche'] = self.create_wall_area()

    def create_wall_area(self):
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
