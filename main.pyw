# This is a sample Python script.
import csvImport
import xmlParser
import gui


# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def convert():
    data = csvImport.import_data(gui.import_textfield.get())
    data_subsection = csvImport.get_subsection('ATTRIBUTE DER RÄUME', data)
    xmlParser.write_data_to_xml(data_subsection, gui.export_textfield.get())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gui
