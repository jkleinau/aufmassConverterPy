import math
import xml.etree.ElementTree as ET

from room import Room
from component import Component


def import_data(path):
    tree = ET.parse(path)
    root = tree.getroot()
    data = dict()
    data['rooms'] = list()
    data['wallWidth'] = root.attrib['exteriorWallWidth']
    data['level'] = 'Ergeschoss' if root[0].attrib['floorType'] == '0' else root[0].attrib['floorType'] + '. Stock'
    for room in root[0]:
        if room.tag == 'floorRoom':
            data['rooms'].append(room)
    return data


def create_rooms(data):
    rooms = list()
    for room in data['rooms']:
        tags = dict()
        tags['Bodenfläche'] = room.attrib['area']
        tags['Umfang'] = room.attrib['perimeter']
        temp_room = Room(room.attrib['type'], data['level'], tags, room.attrib['x'], room.attrib['y'])
        points = [datapoint for datapoint in room if datapoint.tag == 'point']
        components = [[datapoint for datapoint in room if datapoint.tag == 'door' or datapoint.tag == 'window']]
        components = create_components(components, temp_room)
        walls = create_walls(points, temp_room)
        temp_room.components = walls
        temp_room.components.extend(components)
        rooms.append(temp_room)
    return rooms


def create_components(data, room):
    components = list()
    for component in data[0]:
        components.append(
            Component(component.attrib['width'], component.attrib['height'], component.tag, room))
    return components


def create_walls(points, room, tag='Wand'):
    walls = list()
    for i, point in enumerate(points):
        walls.append(Component(distance(point, points[(i + 1) % len(points)]),
                               (float(point.attrib['height']) / 2 + float(
                                   points[(i + 1) % len(points)].attrib['height']) / 2),
                               tag, room))
    return walls


def distance(point1, point2):
    def distance_num(x1, x2, y1, y2):
        return math.sqrt((float(x2) - float(x1)) ** 2 + (float(y2) - float(y1)) ** 2)

    return distance_num(point1.attrib['snappedX'], point2.attrib['snappedX'], point1.attrib['snappedY'],
                        point2.attrib['snappedY'])


