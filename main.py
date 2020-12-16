# This is a sample Python script.
import csvImport
import gui
import xmlParser
from magicXMLImport import import_data, create_rooms, create_positions, build_data


def convert_to_xml(api=None, export_path=None, param_data=None):
    """

    :param param_data:
    :param gui: GUI instance where it gets the path or xml string
    :param api: Boolean checker for import with API or from csv file
    :param export_path: If import from csv file this is the path
    """
    header_raueme = {
        1: "Bodenoberfläche",
        2: "Volumen",
        3: "Boden Umfang",
        4: "Decke Umfang",
        5: "Wandfläche mit Öffnung",
        7: "Umfang Türen",
        8: "Fensterflächen",
        9: "Raumhöhe "
    }
    if api:
        data = import_data(data=param_data)
        rooms = build_data(data)
        xmlParser.write_data_to_xml_schrift(rooms, export_path)

    else:
        return None


def save_to_file(gui, name):
    with open("resources/" + name + ".xml", 'w') as f:
        for line in gui.xml:
            f.write(line)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # data = ""
    # with open('resources/Büro Hoppegarten.xml', 'r') as f:
    #     for line in f:
    #         data += line
    # convert_to_xml(param_data=data, api=True)

    gui = gui.GUI()
