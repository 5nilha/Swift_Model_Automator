import csv
from models.Swift_model import Swift_Model, Model_Type






with open('modeling.csv', 'r') as modelFile:
    models_reader = csv.reader(modelFile,  delimiter=',')
    class_properties = {}
    for index, line in enumerate(models_reader):
        # print("%d %s" %(index, line))
        if index > 0:
            item = line[0]
            item_type = line[1]
            class_properties[item] = item_type

newClass = Swift_Model(Model_Type.class_type.value, "User")
newClass.build_swift5_model(class_properties)
# newClass.print_model()
newClass.write_to_file()

