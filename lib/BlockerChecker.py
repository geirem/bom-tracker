import json

from lib.Component import Component


class BlockerChecker:

    def __init__(self, file: str):
        self.__blocked = {}
        self.__populate_blocked_list(file)

    def __populate_blocked_list(self, file: str):
        with open(file, 'r') as inimage:
            blocked_list = json.load(inimage)
            for blocked in blocked_list:
                component = Component(blocked['jurl'])
                self.__blocked[component.get_ref()] = component

    def check(self, components: list) -> list:
        return [x for x in components if x.get_ref() in self.__blocked]
