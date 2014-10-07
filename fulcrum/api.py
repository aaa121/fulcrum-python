import json

import requests

from .exceptions import NotFoundException, UnauthorizedException, InternalServerErrorException
from .mixins import Findable, Deleteable, Createable, Searchable, Updateable

supported_versions = [2]


class APIConfig(object):
    def __init__(self, key, uri):
        self.key = key
        self.api_root = '{0}/api/v2/'.format(uri)


class BaseAPI(object):
    http_exception_map = {
        401: UnauthorizedException,
        404: NotFoundException,
        500: InternalServerErrorException,
    }

    def __init__(self, api_config):
        self.api_config = api_config

    def call(self, method, path, data=None, extra_headers=None, params=None):
        full_path = self.api_config.api_root + path
        headers = {'X-ApiToken': self.api_config.key}
        if extra_headers is not None:
            headers.update(extra_headers)
        
        kwargs = {'headers': headers}

        if data is not None:
            kwargs['data'] = json.dumps(data)

        if params is not None:
            kwargs['params'] = params

        resp = getattr(requests, method)(full_path, **kwargs)

        if resp.status_code in self.http_exception_map:
            raise self.http_exception_map[resp.status_code]

        if method != 'delete':
            return resp.json()


class Forms(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'forms'


class Records(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'records'


class Webhooks(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'webhooks'


class Photos(BaseAPI, Findable, Searchable):
    path = 'photos'

class Videos(BaseAPI, Findable, Searchable):
    path = 'videos'

class Memberships(BaseAPI, Searchable):
    path = 'memberships'


class Roles(BaseAPI, Searchable):
    path = 'roles'

class ChoiceLists(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'choice_lists'

class ClassificationSets(BaseAPI, Findable, Deleteable, Createable, Searchable, Updateable):
    path = 'classification_sets'

class Projects(BaseAPI, Searchable):
    path = 'projects'
