from aufmassZeile import AufmassZeile


class Component:
    def __init__(self, breite: float, hoehe: float, typ: str, room: room.Room, vector: str = None, uid: str = None,
                 orga_number: int = None, show_id: bool = False) -> component.Component:
        self.orga_number = orga_number
        self.show_id = show_id
        self.uid = uid
        self.vector = vector
        self.room = room
        self.typ = typ
        self.breite = breite
        self.hoehe = hoehe

    def __str__(self):
        return f"{self.typ} {self.orga_number + 1}"

    def write_to_xml(self, root: xml.etree.ElementTree.Element) -> None:
        """
        Writes Component as a Aufmasszeile to a Root XML ELement
        :param root: Root XML Element
        """
        self.to_aufmass_zeile().write_to_xml(root)

    def to_aufmass_zeile(self) -> aufmassZeile.AufmassZeile:
        """
        creates Aufmasszeile for the Component
        :return: Aufmasszeile
        """
        return AufmassZeile(stichwort=f"{self.room.level}, {self.room.name}, {self.typ}",
                            text=f"Oberfläche, {self.room.name}, {self}" if self.show_id else
                            f"Oberfläche, {self.room.name}, {self.typ}",
                            aufmass="{:.2f}*{:.2f}".format(float(self.breite), float(self.hoehe)))
