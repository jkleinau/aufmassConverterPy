import xml.etree.ElementTree as ET


class AufmassZeile():
    def __init__(self, stichwort=None, text=None, aufmass=None):
        self.text = text
        self.stichwort = stichwort
        self.aufmass = aufmass

    def write_to_xml(self, root):
        aufmasszeile = ET.SubElement(root, 'AUFMASSZEILE')

        stichwort = ET.SubElement(aufmasszeile, 'STICHWORT')
        stichwort.text = self.stichwort

        text = ET.SubElement(aufmasszeile, 'TEXT')
        text.text = self.text

        aufmass = ET.SubElement(aufmasszeile, 'AUFMASS')
        aufmass.text = self.aufmass
