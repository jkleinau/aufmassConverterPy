import xml.etree.ElementTree as ET


class Component:
    def __init__(self, breite, hoehe, typ, room, vector=None):
        self.vector = vector
        self.room = room
        self.typ = typ
        self.breite = breite
        self.hoehe = hoehe

    def write_to_xml(self, root):
        aufmasszeile = ET.SubElement(root, 'AUFMASSZEILE')

        stichwort = ET.SubElement(aufmasszeile, 'STICHWORT')
        stichwort.text = self.room.level + ", " + self.room.name + ", " + self.typ

        text = ET.SubElement(aufmasszeile, 'TEXT')
        text.text = "Oberfläche, " + self.room.name + ", " + self.typ

        aufmass = ET.SubElement(aufmasszeile, 'AUFMASS')
        aufmass.text = "{:.2f}*{:.2f}".format(float(self.breite), float(self.hoehe))
