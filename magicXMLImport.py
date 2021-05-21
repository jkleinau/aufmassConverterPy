import math
import xml.etree.ElementTree as ET
import numpy as np
from component import Component
from polyLine import PolyLine
from position import Position
from room import Room
import uuid


def import_data(path=None, data=None):
    root = None
    if path:
        tree = ET.parse(path)
        root = tree.getroot()
    if data:
        root = ET.fromstring(data)

    interior_room_points = [elem for elem in root if elem.tag == 'interiorRoomPoints']
    interior_room_points = interior_room_points[0]
    floor = interior_room_points[0]
    data = dict()
    data['rooms'] = list()
    data['positions'] = list()
    # data['wallWidth'] = root[fl].attrib['exteriorWallWidth']
    data['level'] = 'Ergeschoss' if floor.attrib['floorType'] == '0' else floor.attrib['floorType'] + '. Stock'
    data['rooms'] = [elem for elem in floor if elem.tag == 'floorRoom']
    data['positions'] = [elem for elem in floor if
                         elem.tag == 'symbolInstance' and elem.attrib['id'].split('-')[0] == 'O']
    data['poly'] = [elem for elem in floor if
                    elem.tag == 'symbolInstance' and elem.attrib['symbol'].split('-')[0] == 'editablepolyline']
    return data


def build_data(data):
    positions = create_positions(data['positions'])
    poly_lines = create_polylines(data['poly'])
    rooms = create_rooms(data['rooms'], level=data['level'], positions=positions)
    rooms = link_position_to_component(rooms, poly=poly_lines)
    return rooms


def create_polylines(data):
    poly_lines = dict()
    for poly in data:
        values = [elem for elem in poly if elem.tag == 'values'][0]
        wall_index = [index for index in values if index.attrib['key'] == 'editablePolylineWallIndex'][0].text
        polyline_data = [elem for elem in poly if elem.tag == 'polylineData'][0]
        points = [(point.attrib['x'], point.attrib['y']) for point in polyline_data]
        poly_lines[poly.attrib['uid']] = PolyLine(uid=poly.attrib['uid'], poly_id=poly.attrib['id'],
                                                  symbol=poly.attrib['symbol'], points=points, wallIndex=wall_index)
    return poly_lines


def link_position_to_component(rooms, poly=None):
    for room in rooms:
        for pos in room.positions.values():
            if float(pos.menge) == round(float(room.data['Bodenfläche']), 1) or float(pos.menge) == round(
                    float(room.data['Bodenfläche']), 1) / 2:
                pos.aufmass_zeilen.append(room.data_to_aufmasszeile('Bodenfläche'))
            if pos.ceiling == '1':
                pos.aufmass_zeilen.append(room.data_to_aufmasszeile('Deckenfläche'))
            walls = [wall for wall in room.components.values() if wall.typ == 'Wand']
            for i, link in enumerate(pos.links):

                if i < len(walls):
                    link_id = "{}".format(link)
                    # link_id = "{}:{}".format(link, pos.links[(i + 1) % len(walls)])
                    if link_id in room.components.keys():
                        pos.aufmass_zeilen.append(room.components[link_id].to_aufmass_zeile())

                if link in poly:
                    # wall_index_corrected = str((int(poly[link].wallIndex) + (len(walls) - 1)) % len(walls))
                    component = [wall for wall in walls if str(wall.orga_number) == poly[link].wallIndex]
                    pos.aufmass_zeilen.append(poly[link].to_aufmass_zeile(component=component[0]))
                    try:
                        pos.aufmass_zeilen.remove(component[0].to_aufmass_zeile())
                    except ValueError:
                        pass
            if pos.surface and len(pos.aufmass_zeilen) == 0:
                pos.aufmass_zeilen.append(room.data_to_aufmasszeile('Bodenfläche'))
    return rooms


def create_positions(data):
    positions = dict()

    for position in data:
        try:
            links = [link.attrib['uid'] for link in position if link.tag == 'linkedTo']
            symbol = position.attrib['symbol']
            pos_id = [position.attrib['id']]
            uid = [position.attrib['uid']]
            values = [elem for elem in position if elem.tag == 'values'][0]
            artikel_nr = [elem for elem in values if elem.attrib['key'] == 'sku'][0].text
            pricing_model = [elem for elem in values if elem.attrib['key'] == 'pricingModel'][0].text

            if pricing_model == 'item':
                if symbol in positions.keys():
                    positions[symbol].menge += 1
                    positions[symbol].pos_id.extend(pos_id)
                    positions[symbol].uid.extend(uid)
                else:
                    positions[symbol] = Position(menge=1, artikel_nr=artikel_nr, pos_id=pos_id, uid=uid, symbol=symbol,
                                                 links=links)
            if pricing_model == 'surface':
                try:
                    menge = [elem for elem in values if elem.attrib['key'] == 'totalsurface'][0].text
                except:
                    menge = '1'
                try:
                    ceiling = [elem for elem in values if elem.attrib['key'] == 'surfaceReferenceCeiling'][0].text
                except:
                    ceiling = '0'
                positions[symbol] = Position(menge=menge, artikel_nr=artikel_nr, pos_id=pos_id, uid=uid, symbol=symbol,
                                             links=links, ceiling=ceiling, surface=True)
        except:
            print("Der Artikel konnte nicht korrekt eingelesen werden:\t" + str(position))
            pass

    return positions


def create_rooms(data, level='0', positions=None):
    rooms = list()
    for room in data:
        tags = dict()
        tags['Bodenfläche'] = room.attrib['area']
        tags['Umfang'] = room.attrib['perimeter']

        temp_room = Room(get_translation(room.attrib['type']), level, tags, room.attrib['x'], room.attrib['y'])

        points = [datapoint for datapoint in room if datapoint.tag == 'point']

        try:
            estimate = [est for est in room if est.tag == 'estimate'][0]
        except:
            pass
        temp_positions = dict()
        for item in estimate:
            for pos in positions:
                if item.attrib['id'] in positions[pos].pos_id:
                    if pos not in temp_positions:
                        temp_positions[pos] = positions[pos]

        components = [datapoint for datapoint in room if datapoint.tag == 'door' or datapoint.tag == 'window']
        components = create_components(components, temp_room)

        walls = create_walls(points, temp_room)

        temp_room.positions = temp_positions
        temp_room.components = walls
        temp_room.components.update(components)
        temp_room.create_sums()
        rooms.append(temp_room)
    return rooms


def create_components(data, room):
    components = dict()
    for i, component in enumerate(data):
        try:
            uid = component.attrib['uid']
        except:
            uid = uuid.uuid1()
        components[uid] = Component(component.attrib['width'], component.attrib['height'],
                                    get_translation(component.tag), room,
                                    uid=uid, orga_number=i)
    return components


def create_walls(points, room, tag='Wand'):
    walls = dict()
    for i, point in enumerate(points):
        uid = "{}".format(point.attrib['uid'])
        # uid = "{}:{}".format(point.attrib['uid'], points[(i + 1) % len(points)].attrib['uid'])
        walls[uid] = Component(distance(point, points[(i + 1) % len(points)]),
                               (float(point.attrib['height']) / 2 + float(
                                   points[(i + 1) % len(points)].attrib['height']) / 2),
                               tag, room, vector_points(point, points[(i + 1) % len(points)]),
                               uid=uid, orga_number=i, show_id=True)
    return walls


def distance(point1, point2):
    def distance_num(x1, x2, y1, y2):
        return math.sqrt((float(x2) - float(x1)) ** 2 + (float(y2) - float(y1)) ** 2)

    return distance_num(point1.attrib['snappedX'], point2.attrib['snappedX'], point1.attrib['snappedY'],
                        point2.attrib['snappedY'])


def vector_points(point1, point2):
    return np.asarray(
        [float(point2.attrib['snappedX']) - float(point1.attrib['snappedX']),
         float(point2.attrib['snappedY']) - float(point1.attrib['snappedY'])])


def get_file_urls(xml, filetype=None):
    """
    returns a dict with files for a magicplan plan like dict['name':'url']
    :param xml: XML with file list
    :param filetype: type as 'pdf'
    :return: dict with files
    """
    root = ET.fromstring(xml)
    files = dict()
    for node in root:
        if node.tag == 'file':
            if filetype:
                if node.attrib['type'] == filetype:
                    files[node.attrib['name']] = node.attrib['url']
            else:
                files[node.attrib['name']] = node.attrib['url']
    return files


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
        'Vestibule': 'Flur',
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
