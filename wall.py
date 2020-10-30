import xml.etree.ElementTree as ET


class Wall:
    def __init__(self, breite, hoehe, oberflaeche, typ, room):
        self.room = room
        self.typ = typ
        self.breite = breite
        self.hoehe = hoehe
        self.oberflaeche = oberflaeche

    def write_to_xml(self, root):
        aufmasszeile = ET.SubElement(root, 'AUFMASSZEILE')

        stichwort = ET.SubElement(aufmasszeile, 'STICHWORT')
        stichwort.text = self.room.level + ", " + self.room.name + ", " + self.typ

        text = ET.SubElement(aufmasszeile, 'TEXT')
        text.text = "Oberfläche, " + self.room.name + ", " + self.typ

        aufmass = ET.SubElement(aufmasszeile, 'AUFMASS')
        aufmass.text = self.breite + "*" + self.hoehe
