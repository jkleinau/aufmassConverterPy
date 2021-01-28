import xml.etree.ElementTree as ET
from aufmassZeile import *


class Position:
    def __init__(self, menge: str = None, artikel_nr: str = None, positions_nr: str = None, pos_id: str = None, uid: str = None, symbol: str = None,
                 aufmass_zeilen: list[AufmassZeile] = None, links: dict[str,str] = None, ceiling: str = None) -> Position:
        self.ceiling = ceiling
        self.symbol = symbol
        self.pos_id = pos_id
        self.uid = uid
        self.menge = menge
        self.artikel_nr = artikel_nr
        self.positions_nr = positions_nr
        self.aufmass_zeilen = aufmass_zeilen
        if aufmass_zeilen is None:
            self.aufmass_zeilen = list()
        self.links = links
        if links is None:
            self.links = dict()

    def __str__(self):
        return f"Position {self.artikel_nr}, mit {len(self.aufmass_zeilen)} Aufmasszeilen"

    def write_to_xml(self, root: xml.etree.ElementTree.Element) -> None:
        """
        Writes the Position to the given root Element in XML
        :param root: Root Element
        """
        material_position = ET.SubElement(root, 'MATERIALPOSITION')

        if self.positions_nr:
            positions_nr = ET.SubElement(material_position, 'POSITIONSNUMMER')
            positions_nr.text = str(self.positions_nr)

        if len(self.aufmass_zeilen) > 0:
            aufmass = ET.SubElement(material_position, 'AUFMASS')
            in_meng_uebernehmen = ET.SubElement(aufmass, 'IN_MENGE_UEBERNEHMEN')
            in_meng_uebernehmen.text = '1'

            for aufmass_zeile in self.aufmass_zeilen:
                aufmass_zeile.write_to_xml(aufmass)

        menge = ET.SubElement(material_position, 'MENGE')
        menge.text = str(self.menge)

        artikel_nr = ET.SubElement(material_position, 'ARTIKELNUMMER')
        artikel_nr.text = str(self.artikel_nr)