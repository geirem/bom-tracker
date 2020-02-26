class ConfigurationException(Exception):

    def __init__(self, message: str):
        self.__message =  message

    def __str__(self):
        return f'ConfigurationException: {self.__message}'
