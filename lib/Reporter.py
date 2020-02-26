import json
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
        self.__header = {
            'X-Api-Key': environ['TRACK_TOKEN'],
        }
        self.__project = project

    def __assemble_url(self, local_part: str) -> str:
        return self.__base_url + local_part

    def find_project_key(self) -> Optional[str]:
        response = requests.get(
            self.__assemble_url('/project/lookup'),
            params={'name': self.__project.get_name(), 'version': self.__project.get_version()},
            headers=self.__header
        )
        if response.status_code == 404:
            return None
        if response.status_code == 200:
            return response.json().get('uuid')
        raise TrackCallException()

    def create_project(self):
        data = {'name': self.__project.get_name(), 'version': self.__project.get_version()}
        headers = {**self.__header, **{'Content-Type': 'application/json'}}
        response = requests.put(
            self.__assemble_url('/project'), data=json.dumps(data), headers=headers
        )
        if response.status_code == 404:
            return None
        if response.status_code == 201:
            return response.json().get('uuid')
        raise TrackCallException()
