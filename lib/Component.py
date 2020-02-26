class Component:

    def __init__(self, key: str):
        self.__key = key

    def get_key(self) -> str:
        return self.__key
