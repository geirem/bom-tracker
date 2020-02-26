import base64
import json
import pprint
from os import environ
from typing import Optional

import requests as requests

from lib.Project import Project
from lib.exceptions.ConfigurationException import ConfigurationException
from lib.exceptions.TrackCallException import TrackCallException


class Reporter:

    def __init__(self, base_url: str, project: Project):
        if 'TRACK_TOKEN' not in environ:
            raise ConfigurationException('Access token (TRACK_TOKEN) for dependency tracker not configured.')
        self.__base_url = base_url
        self.__headers = {
            'X-Api-Key': environ['TRACK_TOKEN'],
            'Content-Type': 'application/json',
        }
        self.__project = project

    def __assemble_url(self, local_part: str) -> str:
        return self.__base_url + local_part

    def send_bom(self, bom_file: str) -> None:
        with open(bom_file, 'r') as inimage:
            bom_data = base64.b64encode(inimage.read().encode('utf-8')).decode('ascii').replace('\n', '')
        data = {
            'bom': bom_data[0:100],
            'autoCreate': True,
            'projectVersion': self.__project.get_version(),
            'projectName': self.__project.get_name(),
        }
        pprint.pprint(data)
        response = requests.put(
            self.__assemble_url('/project'), data=data, headers=self.__headers
        )
        print(response)
        print(response.content)
        if 200 <= response.status_code < 300:
            return
        raise TrackCallException()

