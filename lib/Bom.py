import xml.etree.ElementTree as ET

from lib.Component import Component


class Bom:

    def __init__(self, file: str):
        self.__file = file
        self.__components = []

    def get_components(self) -> list:
        return self.__components

    def parse(self):
        ns = {
            'cyclone10': 'http://cyclonedx.org/schema/bom/1.0',
            'cyclone11': 'http://cyclonedx.org/schema/bom/1.1',
        }
        tree = ET.parse(self.__file)
        root = tree.getroot()
        version = 'cyclone11' if root.find('cyclone11:components', ns) else 'cyclone10'
        bom_components = root.find(f'{version}:components', ns)
        for bom_component in bom_components.findall(f'{version}:component', ns):
            purl = bom_component.find(f'{version}:purl', ns).text
            component = Component(purl)
            component.set_name(bom_component.find(f'{version}:name', ns).text)
            component.set_version(bom_component.find(f'{version}:version', ns).text)
            self.__components.append(component)
        return self
