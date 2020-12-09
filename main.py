# This is a sample Python script.
import csvImport
import gui
import xmlParser
from magicXMLImport import import_data, create_rooms, create_positions, build_data


def convert_to_xml(gui=None, api=None, export_path=None, param_data=None):
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
        param_data = csvImport.import_data(gui.import_path.get())
        data_subsection_raume = csvImport.get_subsection('ATTRIBUTE DER RÄUME', param_data)
        data_subsection_waende = csvImport.get_subsection('Wandeigenschaften', param_data)
        rooms = xmlParser.create_data(data_subsection_raume, data_subsection_waende, header_raueme)
        xmlParser.write_data_to_xml(rooms, gui.export_path.get())


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
