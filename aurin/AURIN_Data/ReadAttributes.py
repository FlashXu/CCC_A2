def read_metadata(filepath, genfile_path):
    import json
    import csv
    f = open(filepath, 'r', encoding='UTF-8')
    c = open(genfile_path, "w", newline='')
    writer = csv.writer(c)
    attributes = json.load(f)['selectedAttributes']
    f.close()

    line_list = []
    line_list.append("Name")
    line_list.append("Type")
    line_list.append("Title")
    writer.writerow(line_list)

    for i in range(len(attributes)):
        line = attributes[i]
        line_list = []
        line_list.append(line["name"])
        line_list.append(line["type"])
        line_list.append(line["title"])
        writer.writerow(line_list)
    c.close()



read_metadata("metadataSA3_Melb_Income.json", "Income_Attributes.csv")
read_metadata("metadataSA3_Melb_Population.json", "Population_Attributes.csv")