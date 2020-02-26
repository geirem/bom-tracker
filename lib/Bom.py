import xml.etree.ElementTree as ET

from lib.Component import Component


class Bom:

    def __init__(self, file: str):
        self.__file = file
        self.__components = []

    def get_components(self) -> list:
        return self.__components

    def parse(self):
        ns = {'cyclone': 'http://cyclonedx.org/schema/bom/1.1'}
        tree = ET.parse(self.__file)
        root = tree.getroot()
        for bom_component in root.find('cyclone:components', ns).findall('cyclone:component', ns):
            component = Component(bom_component.attrib['bom-ref'])
            component.set_name(bom_component.get('name'))
            self.__components.append(component)
        return self
