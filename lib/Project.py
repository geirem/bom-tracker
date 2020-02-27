from os import path, environ
import xml.etree.ElementTree as ET
from typing import List, Optional, Tuple


class Project:

    __POM_NAME = 'pom.xml'
    __POM_NS = {'maven': 'http://maven.apache.org/POM/4.0.0'}

    def __init__(self):
        (self.__name, self.__version) = Project.__from_pom() if Project.__is_maven() else Project.__from_vars()

    def __str__(self):
        return f'{self.__name}:{self.__version}'

    def get_name(self) -> str:
        return self.__name

    def get_version(self) -> str:
        return self.__version

    @staticmethod
    def __is_maven() -> bool:
        return path.exists(Project.__POM_NAME)

    @staticmethod
    def __from_pom() -> Tuple[str, str]:
        tree = ET.parse(Project.__POM_NAME)
        root = tree.getroot()
        group_id = Project.__safe_read_xml_value('groupId', root)
        if group_id is None:
            group_id = Project.__safe_read_xml_value(root.find('maven:parent', Project.__POM_NS), root)
        artifact_id = Project.__safe_read_xml_value('artifactId', root)
        version = Project.__safe_read_xml_value('version', root)
        if None in (group_id, artifact_id, version):
            return Project.__from_vars()
        return f'{group_id}/{artifact_id}', version

    @staticmethod
    def __safe_read_xml_value(tag: str, element: ET.Element) -> Optional[str]:
        try:
            value = element.find(f'maven:{tag}', Project.__POM_NS).text
        except AttributeError:
            return None
        return value

    @staticmethod
    def __from_vars() -> Tuple[str, str]:
        return str(environ['GITHUB_REPOSITORY']), str(environ['GITHUB_SHA'])
