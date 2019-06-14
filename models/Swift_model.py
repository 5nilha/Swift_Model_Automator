
from enum import Enum

class Model_Type(Enum):
    class_type = "class"
    struct_type = "struct"

class Swift_Instance_Type(Enum):
    constant = "let"
    variable = "var"

class Swift_Model:
    __class_definition = []
    __constructor_head = ""
    __constructor_body = ""
    properties = {}

    def __init__(self, type, class_name):
        self.type = type
        self.class_name = class_name
        self.__class_definition.append(self.type + " " + self.class_name + " {")

    def __add_instance(self, Swift_Instance_Type, property_item, property_type, default_data, last_property):

        class_instance = property_item + ": " + property_type.capitalize()
        self.__class_definition.append(
            "\t" + Swift_Instance_Type + " " + class_instance + " = " + default_data)
        self.__set_constructor_body(property_item)
        if last_property:
            self.__set_constructor_head(class_instance, ") {\n")
        else:
            self.__set_constructor_head(class_instance, ", ")


    def __add_constructor(self):
        constructor_1 = "\n\tinit() {}\n"
        constructor_2 = self.__constructor_head + self.__constructor_body + "\t}"
        self.__class_definition.append(constructor_1)
        self.__class_definition.append(constructor_2)


    def __set_constructor_head(self, class_instance, delimiter):
        self.__constructor_head += "{}{}".format(class_instance, delimiter)



    def __set_constructor_body(self, property):
        self.__constructor_body += "\t\tself.{} = {}\n".format(property, property)


    def __close_class(self):
        self.__class_definition.append("}")

    def build_swift5_model(self, properties):
        self.__constructor_head = "\n\tinit("
        self.properties = properties

        property_length = len(properties)
        count = 0
        for property, property_type in properties.items():
            if property_type.lower() == "string":
                default_data = '""'
            elif property_type.lower() == "bool":
                default_data = "false"
            elif property_type.lower() == "int":
                default_data = "0"
            elif property_type.lower() == "double":
                default_data = "0.0"
            elif property_type.lower() == "date" or property_type == "timestamp":
                default_data = "Date()"
            else:
                default_data = "nil"

            if count < property_length - 1:
                is_last = False
            else:
                is_last = True

            self.__add_instance(Swift_Instance_Type.variable.value, property, property_type.lower(), default_data, is_last)
            count += 1

        if self.type == "class":
            self.__add_constructor()


        self.__close_class()

    def print_model(self):
        for line in self.__class_definition:
            print(line)

    def write_to_file(self):
        file = open('{}.swift'.format(self.class_name), 'w')
        for line in self.__class_definition:
            file.write("{}\n".format(line))
        file.close()