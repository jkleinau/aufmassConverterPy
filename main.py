# This is a sample Python script.
import csvImport
import xmlParser

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = csvImport.import_data()
    data_subsection = csvImport.get_subsection('ATTRIBUTE DER RÄUME', data)
    xmlParser.write_data_to_xml(data_subsection)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
