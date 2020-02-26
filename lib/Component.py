class Component:

    def __init__(self, ref: str):
        self.__ref = ref
        self.__name = None

    def __str__(self):
        return self.__ref

    def __repr__(self):
        return self.__str__()

    def get_ref(self) -> str:
        return self.__ref

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name
