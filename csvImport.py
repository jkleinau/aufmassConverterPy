import csv


def import_data():
    data = []
    with open('resources/Grundriss 3.csv', newline='', encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data.append(row)
    return data


def get_subsection(subsection, data):
    subsection_data = []
    header_found = False
    for entry in data:
        if not header_found:
            header_found = subsection in entry
        if entry and header_found:
            subsection_data.append(entry)
        else:
            header_found = False
    return subsection_data
