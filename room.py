from wall import *


class Room:

    def __init__(self, name, level, data, x, y):

        self.walls = []
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

            stichwort = ET.SubElement(aufmasszeile, 'AUFMASS')
            if self.data[tag]:
                stichwort.text = self.data[tag].split()[0]
        for wall in self.walls:
            wall.write_to_xml(root)
