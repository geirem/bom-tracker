from os import path, environ


class Project:

    def __init__(self):
        if self.__is_maven():
            (self.__name, self.__version) = self.__project_from_pom()
        else:
            self.__name = environ['GITHUB_REPOSITORY']
            self.__version = environ['GITHUB_SHA']

    def __str__(self):
        return f'{self.__name}:{self.__version}'

    def get_name(self) -> str:
        return self.__name

    def get_version(self) -> str:
        return self.__version

    @staticmethod
    def __is_maven() -> bool:
        return path.exists('pom.xml')

    @staticmethod
    def __project_from_pom():
        return 'foo', 'bar'
