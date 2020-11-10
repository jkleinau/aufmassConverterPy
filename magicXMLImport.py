import xml.etree.ElementTree as ET

from room import Room


def import_data(path):
    tree = ET.parse(path)
    root = tree.getroot()
    data = []
    for room in root[0]:
        if room.tag == 'floorRoom':
            data.append(room)
    return data

def create_rooms(data):
    rooms = []
    for room in data:
        rooms.append(Room())