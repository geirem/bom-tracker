import base64
import json
from os import environ
import logging

import requests as requests

from lib.Project import Project
from lib.exceptions.ConfigurationException import ConfigurationException
from lib.exceptions.TrackCallException import TrackCallException


# TODO: REMOVE TEST SCAFFOLDING.
logging.basicConfig(level=logging.DEBUG)


class Reporter:

    def __init__(self, base_url: str, project: Project):
        if 'TRACK_TOKEN' not in environ:
            raise ConfigurationException(
                'Token (TRACK_TOKEN) for dependency tracker missing.'
            )
        self.__base_url = base_url
        self.__headers = {
            'X-Api-Key': environ['TRACK_TOKEN'].strip(),
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        self.__project = project

    def __assemble_url(self, local_part: str) -> str:
        return self.__base_url + local_part

    def ensure_project_exists(self) -> None:
        data = {
            'name': self.__project.get_name(),
            'version': self.__project.get_version(),
        }
        response = requests.get(
            self.__assemble_url('/project/lookup'),
            params=data,
            headers=self.__headers
        )
        if response.status_code == 200:
            return
        if response.status_code != 404:
            raise TrackCallException(
                f'Unable to verify project status: {response.status_code}.'
            )
        data['tags'] = [
            {'name': 'untracked_dependencies'}
        ]
        response = requests.put(
            self.__assemble_url('/project'),
            data=json.dumps(data),
            headers=self.__headers
        )
        if response.status_code == 201:
            return
        raise TrackCallException(
            f'Unable to create new project: {response.status_code}.'
        )

    def send_bom(self, bom_file: str) -> None:
        with open(bom_file, 'r') as inimage:
            bom_data = base64.b64encode(
                inimage.read().encode('utf-8')
            ).decode('ascii').replace('\n', '')
        data = {
            'bom': bom_data,
            'autoCreate': True,
            'projectVersion': self.__project.get_version(),
            'projectName': self.__project.get_name(),
        }
        response = requests.put(
            self.__assemble_url('/bom'),
            data=json.dumps(data),
            headers=self.__headers
        )
        if 200 <= response.status_code < 300:
            return
        raise TrackCallException(f'Unable to send bom: {response.status_code}.')
