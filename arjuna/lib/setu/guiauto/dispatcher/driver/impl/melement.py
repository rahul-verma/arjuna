
class MultiElement:

    def __init__(self, elements):
        self.__elements = elements

    def get_instance_count(self):
        return len(self.__elements)

    def get_element_at_index(self, index):
        return self.__elements[index]