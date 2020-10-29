import xml.etree.ElementTree as ET


# # create the file structure
# data = ET.Element('data')
# items = ET.SubElement(data, 'items')
# item1 = ET.SubElement(items, 'item')
# item2 = ET.SubElement(items, 'item')
# item1.set('name', 'item1')
# item2.set('name', 'item2')
# item1.text = 'item1abc'
# item2.text = 'item2abc'
#
# # create a new XML file with the results
def write_data_to_xml(data_raume,data_waende, path, header_raume, header_waende):
    project = ET.Element('PROJEKT', attrib={"xmlns": "urn:in-software-com:IN-AUFMASS"})
    position = ET.SubElement(project, 'POSITION', attrib={"ID": "01.01"})

    write_data_to_xml_raume(data_raume, header_raume, position)
    write_data_to_xml_waende(data_waende, header_waende, position)

    mydata = ET.tostring(project, encoding='ISO-8859-1')
    myfile = open(path + "\AUFMASS.xml", "wb")
    myfile.write(mydata)


def write_data_to_xml_raume(data, header, root):
    # create Iterator and skip first line
    iterdata = iter(data)
    next(iterdata)
    for line in iterdata:
        name = ""
        if len(line) <= 2:
            level = line[0]
            continue
        for i in range(len(line)):
            # Get Room description
            if name == "":
                name = line[i]
                continue

            if i in header:
                aufmasszeile = ET.SubElement(root, 'AUFMASSZEILE')

                stichwort = ET.SubElement(aufmasszeile, 'STICHWORT')
                stichwort.text = level + ", " + name

                text = ET.SubElement(aufmasszeile, 'TEXT')
                text.text = header[i] + ", " + name

                stichwort = ET.SubElement(aufmasszeile, 'AUFMASS')
                if line[i]:
                    stichwort.text = line[i].split()[0]


def write_data_to_xml_waende(data, header, root):


    # create Iterator and skip first line
    iterdata = iter(data)
    next(iterdata)
    for line in iterdata:
        name = ""
        if len(line) <= 2:
            level = line[0]
            continue
        for i in range(len(line)):
            # Get Room description
            if name == "":
                name = line[i] + ", " + line[i + 2]
                continue

            if i in header:
                aufmasszeile = ET.SubElement(root, 'AUFMASSZEILE')

                stichwort = ET.SubElement(aufmasszeile, 'STICHWORT')
                stichwort.text = level + ", " + name

                text = ET.SubElement(aufmasszeile, 'TEXT')
                text.text = header[i] + ", " + name

                stichwort = ET.SubElement(aufmasszeile, 'AUFMASS')
                if line[i]:
                    stichwort.text = line[i].split()[0]

