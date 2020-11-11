import math

from component import *


class Room:

    def __init__(self, name, level, data, x, y, components=None):

        if components is None:
            components = list()
        self.components = components
        self.level = level
        self.data = data
        self.name = name
        self.y = y
        self.x = x

    def write_to_xml(self, root):
        for tag in self.data:
            aufmasszeile = ET.SubElement(root, 'AUFMASSZEILE')

            stichwort = ET.SubElement(aufmasszeile, 'STICHWORT')
            stichwort.text = self.level + ", " + self.name

            text = ET.SubElement(aufmasszeile, 'TEXT')
            text.text = tag + ", " + self.name

            aufmass = ET.SubElement(aufmasszeile, 'AUFMASS')
            if self.data[tag]:
                aufmass.text = str(self.data[tag]).split()[0]
        for component in self.components:
            component.write_to_xml(root)

    def create_sums(self):
        self.data['Deckenfläche'] = self.data['Bodenfläche']
        self.data['Wandfläche'] = round(sum([component.breite*component.hoehe for component in self.components if component.typ == 'Wand']),2)