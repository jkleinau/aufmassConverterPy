import math
import xml.etree.ElementTree as ET

from room import Room
from component import Component


def get_translation(tag):
    translations = {
        'Kitchen': 'Küche',
        'Dining Room': 'Esszimmer',
        'Living Room': 'Wohnzimmer',
        'Hall': 'Diele',
        'Master Bedroom': 'Elternschlafzimmer',
        'Bedroom': 'Schlafzimmer',
        'Bathroom': 'Badezimmer',
        'Closet': 'Wandschrank',
        'Study': 'Arbeitszimmer',
        'Music Room': 'Musikzimmer',
        'Balcony': 'Balkon',
        'Garage': 'Garage',
        'Corridor': 'Korridor',
        'Laundry Room': 'Waschküche',
        'Playroom': 'Spielzimmmer',
        'Cellar': 'Keller',
        'Workshop': 'Werkraum',
        'Stairway': 'Treppenhaus',
        'Furnace Room': 'Heizungsraum',
        'Toilet': 'Toilette',
        'Vestibule': 'Innenhof',
        'Other': 'Sonstiges',
        'Hatched Room': 'Durchreiche',
        'Private Office': 'Arbeitszimmer',
        'Shared Office': 'Großraumbüro',
        'Open Space': 'Offener Raum',
        'Meeting Room': 'Besprechungsraum',
        'Conference Room': 'Konferenzraum',
        'Reception': 'Empfang',
        'Kitchenette': 'Kochnische',
        'Cafeteria': 'Cafeteria',
        'Lounge': 'Lounge',
        'Waiting Room': 'Wartezimmer',
        'Training Room': 'Schulungsraum',
        'Maintenance Room': 'Wartungsraum',
        'Storage': 'Lagerraum',
        'Archives': 'Archiv',
        'Photocopy Room': 'Kopierraum',
        'Lab': 'Labor',
        'Server Room': 'Server-Raum',
        'Elevators': 'Aufzug',
        'door': 'Tür',
        'window': 'Fenster'
    }
    return translations[tag] if tag in translations.keys() else tag


def import_data(path):
    root = ET.fromstring(path)
    data = dict()
    data['rooms'] = list()
    # data['wallWidth'] = root[fl].attrib['exteriorWallWidth']
    data['level'] = 'Ergeschoss' if root[1].attrib['floorType'] == '0' else root[1].attrib['floorType'] + '. Stock'
    for room in root[1]:
        if room.tag == 'floorRoom':
            data['rooms'].append(room)
    return data


def create_rooms(data):
    rooms = list()
    for room in data['rooms']:
        tags = dict()
        tags['Bodenfläche'] = room.attrib['area']
        tags['Umfang'] = room.attrib['perimeter']
        temp_room = Room(get_translation(room.attrib['type']), data['level'], tags, room.attrib['x'], room.attrib['y'])
        points = [datapoint for datapoint in room if datapoint.tag == 'point']
        components = [datapoint for datapoint in room if datapoint.tag == 'door' or datapoint.tag == 'window']
        components = create_components(components, temp_room)
        walls = create_walls(points, temp_room)
        temp_room.components = walls
        temp_room.components.extend(components)
        temp_room.create_sums()
        rooms.append(temp_room)
    return rooms


def create_components(data, room):
    components = list()
    for component in data:
        components.append(
            Component(component.attrib['width'], component.attrib['height'], get_translation(component.tag), room))
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
