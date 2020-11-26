import xml.etree.ElementTree as ET


class Position:
    def __init__(self, menge=None, artikel_nr=None, positions_nr=None):
        self.menge = menge
        self.artikel_nr = artikel_nr
        self.positions_nr = positions_nr

    def write_to_xml(self, root):
        material_position = ET.SubElement(root, 'MATERIALPOSITION')

        menge = ET.SubElement(material_position, 'MENGE')
        menge.text = str(self.menge)

        artikel_nr = ET.SubElement(material_position, 'ARTIKELNUMMER')
        artikel_nr.text = str(self.artikel_nr)

        if self.positions_nr:
            positions_nr = ET.SubElement(material_position, 'POSITIONSNUMMER')
            positions_nr.text = str(self.positions_nr)
