# This is a sample Python script.
import csvImport
import xmlParser
import gui


# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def convert():
    header_raueme = {
        0: "Raumname ",
        1: "Bodenoberfläche",
        2: "Volumen",
        3: "Boden Umfang",
        4: "Decke Umfang",
        6: "Wandfläche ohne Öffnung",
        7: "Umfang Türen",
        8: "Fensterflächen",
        9: "Raumhöhe "
    }

    header_waende = {
        3: "Oberfläche",
        5: "Breite",
        6: "Höhe",

    }

    data = csvImport.import_data(gui.import_textfield.get())
    data_subsection_raume = csvImport.get_subsection('ATTRIBUTE DER RÄUME', data)
    data_subsection_waende = csvImport.get_subsection('Wandeigenschaften', data)
    xmlParser.write_data_to_xml(data_subsection_raume,data_subsection_waende, gui.export_textfield.get(), header_raueme, header_waende)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gui
