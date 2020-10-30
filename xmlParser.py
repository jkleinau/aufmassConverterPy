import xml.etree.ElementTree as ET
from datetime import datetime

from room import Room
from wall import Wall


def write_data_to_xml(data_raume, data_waende, path, header_raume, header_waende):
    project = ET.Element('PROJEKT', attrib={"xmlns": "urn:in-software-com:IN-AUFMASS"})
    position = ET.SubElement(project, 'POSITION', attrib={"ID": "1.01"})

    rooms = create_rooms(data_raume, header_raume)
    # TODO rausnehmen wenn wände
    for room in rooms:
        create_walls_for_room(data_waende,room)
        room.write_to_xml(position)

    mydata = ET.tostring(project, encoding='ISO-8859-1')
    myfile = open(path + "\AUFMASS-" + str(datetime.now().date()) + ".xml", "wb")
    myfile.write(mydata)


def create_rooms(data, header):
    # create Iterator and skip first line
    rooms = []
    iterdata = iter(data)
    next(iterdata)
    room_data = {}
    for line in iterdata:
        if len(line) <= 2:
            level = line[0]
            continue
        name = line[0]
        for tag in header:
            room_data[header[tag]] = line[tag]
        rooms.append(Room(name, level, room_data))
    return rooms


def create_walls_for_room(data, room):
    # create Iterator and skip first line
    iterdata = iter(data)
    next(iterdata)
    for line in iterdata:
        if room.name == line[0]:
            room.walls.append(Wall(line[5], line[6], line[3], line[2], room))