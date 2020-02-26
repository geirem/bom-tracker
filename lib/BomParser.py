from typing import List

from lib import Component


class BomParser:

    def __init__(self, file: str):
        self.__file = file
        self.__components = []

    def get_components(self) -> list:
        return self.__components

    def parse(self):
        return self
