import xml.etree.ElementTree as ET


class AufmassZeile():
    def __init__(self, stichwort: str = None, text: str = None, aufmass: str = None):
        self.text = text
        self.stichwort = stichwort
        self.aufmass = aufmass

    def __str__(self):
        return f"{self.text}, {self.aufmass}"

    def __eq__(self, other):
        if not isinstance(other, AufmassZeile):
            return NotImplemented
        return self.aufmass == other.aufmass and self.text == other.text

    def write_to_xml(self, root) -> None:
        """
        Writes Aufmasszeile to root XML Element
        :param root: Root XML Element
        """
        aufmasszeile = ET.SubElement(root, 'AUFMASSZEILE')

        stichwort = ET.SubElement(aufmasszeile, 'STICHWORT')
        stichwort.text = self.stichwort

        text = ET.SubElement(aufmasszeile, 'TEXT')
        text.text = self.text

        anzahl = ET.SubElement(aufmasszeile, 'ANZAHL')
        anzahl.text = ' '

        aufmass = ET.SubElement(aufmasszeile, 'LAENGE')
        aufmass.text = self.aufmass
