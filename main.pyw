# This is a sample Python script.
import csvImport
import xmlParser
from magicXMLImport import import_data, create_rooms
import gui


class Main:
    @staticmethod
    def convert_to_xml(gui):
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
        data = import_data(gui.xml)
        rooms = create_rooms(data)
        xmlParser.write_data_to_xml(rooms, gui.export_path.get())
        """
            data = csvImport.import_data(gui.import_path.get())
            data_subsection_raume = csvImport.get_subsection('ATTRIBUTE DER RÄUME', data)
            data_subsection_waende = csvImport.get_subsection('Wandeigenschaften', data)
            rooms = xmlParser.create_data(data_subsection_raume,data_subsection_waende,header_rauem)
            xmlParser.write_data_to_xml(rooms, gui.export_path.get())
        """


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gui = gui.GUI()
