import xml.etree.ElementTree as ET

from component import Component
from room import Room


def write_data_to_xml_schrift(rooms, path):
    project = ET.Element('SCHRIFTSTUECKE', attrib={"xmlns": "urn:in-software-com:IN-SCHRIFTSTUECKE"})

    schriftstueck = ET.SubElement(project, "SCHRIFTSTUECK")
    kopf = ET.SubElement(schriftstueck, "KOPF")
    positionen = ET.SubElement(schriftstueck, 'POSITIONEN')
    main_pos = ET.SubElement(positionen, 'MATERIALPOSITION')
    main_pos_nr = ET.SubElement(main_pos, 'POSITIONSNUMMER')
    main_pos_nr.text = '01.01'
    aufmass = ET.SubElement(main_pos, 'AUFMASS')
    in_menge = ET.SubElement(aufmass, 'IN_MENGE_UEBERNEHMEN')
    in_menge.text = '1'

    for room in rooms:
        room.write_to_xml(aufmass)
    ET.SubElement(main_pos, 'MENGE').text = '1'

    for room in rooms:
        for pos in room.positions.values():
            pos.write_to_xml(positionen)

    mydata = ET.tostring(project, encoding='ISO-8859-1')
    myfile = open(path, "wb")
    myfile.write(mydata)


def write_data_to_xml(rooms, path):
    project = ET.Element('PROJEKT', attrib={"xmlns": "urn:in-software-com:IN-AUFMASS"})
    position = ET.SubElement(project, 'POSITION', attrib={"ID": "1.01"})

    for room in rooms:
        room.write_to_xml(position)
    mydata = ET.tostring(project, encoding='ISO-8859-1')
    myfile = open(path, "wb")
    myfile.write(mydata)
