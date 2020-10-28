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

def write_data_to_xml():
    project = ET.Element('PROJEKT', attrib={"xmlns": "urn:in-software-com:IN-AUFMASS"})
    position = ET.SubElement(project, 'POSITION', attrib={"ID": "01.01"})

    header = {
        0:"Raumname ",
        1:"Bodenoberfläche",
        2:"Volumen",
        3:"Boden Umfang",
        4:"Decke Umfang",
        6:"Wandfläche ohne Öffnung",
        7:"Umfang Türen",
        8:"Fensterflächen",
        9:"Raumhöhe "
    }

    # create Iterator and skip first line
    iterdata = iter(data)
    next(iterdata)
    for line in iterdata:
        name = ""
        if len(line) == 2:
            level = line[0]
            continue
        for i in range(len(line)):
            # Get Room description
            if name == "":
                name = line[i]
                continue

            if i in header:
                aufmasszeile = ET.SubElement(position, 'AUFMASSZEILE')

                stichwort = ET.SubElement(aufmasszeile, 'STICHWORT')
                stichwort.text = level + ", " + name

                text = ET.SubElement(aufmasszeile, 'TEXT')
                text.text = header[i] + ", " + name

                stichwort = ET.SubElement(aufmasszeile, 'AUFMASS')
                stichwort.text = line[i]

    mydata = ET.tostring(project,encoding='ISO-8859-1')
    myfile = open("AUFMASS.xml", "wb")
    myfile.write(mydata)