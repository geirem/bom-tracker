class Component:

    def __init__(self, purl: str):
        self.__purl = purl
        self.__name = None
        self.__version = None

    def __str__(self) -> str:
        return self.__purl

    def __repr__(self) -> str:
        return self.__str__()

    def get_purl(self) -> str:
        return self.__purl

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_version(self, version: str) -> None:
        self.__version = version
