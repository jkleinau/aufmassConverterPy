import xml.etree.ElementTree as ET
from datetime import datetime


def write_data_to_xml(data_raume, data_waende, path, header_raume, header_waende):
    project = ET.Element('PROJEKT', attrib={"xmlns": "urn:in-software-com:IN-AUFMASS"})
    position = ET.SubElement(project, 'POSITION', attrib={"ID": "1.01"})

    write_data_to_xml_raume(data_raume, header_raume, position)
    #TODO rausnehmen wenn wände
    #write_data_to_xml_waende(data_waende, header_waende, position)

    mydata = ET.tostring(project, encoding='ISO-8859-1')
    myfile = open(path + "\AUFMASS-" + str(datetime.now().date()) + ".xml", "wb")
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
                name = line[i]
                continue

            if i in header:
                aufmasszeile = ET.SubElement(root, 'AUFMASSZEILE')

                stichwort = ET.SubElement(aufmasszeile, 'STICHWORT')
                stichwort.text = level + ", " + name + ", " + line[8]

                text = ET.SubElement(aufmasszeile, 'TEXT')
                text.text = header[i] + ", " + name + ", " + line[2]

                aufmass = ET.SubElement(aufmasszeile, 'AUFMASS')
                if line[i]:
                    aufmass.text = line[5]+"*"+line[6]
