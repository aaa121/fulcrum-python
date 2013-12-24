import logging
import unittest

import httpretty

from fulcrum import Fulcrum
from fulcrum.api import APIConfig
from fulcrum.exceptions import NotFoundException, InvalidAPIVersionException, InvalidObjectException, InternalServerErrorException

key = 'super_secret_key'
api_root = 'https://api.fulcrumapp.com/api/v2'
valid_form = {
    'form': {
        'name': 'whatever',
        'elements': [
            {
                'name': 'element1'
            }
        ]
    }
}


class APIConfigTest(unittest.TestCase):
    def test_invalid_version(self):
        exc = None
        try:
            APIConfig(key='foo', version=99)
        except Exception as exc:
            pass
        self.assertIsInstance(exc, InvalidAPIVersionException)


class FormTest(unittest.TestCase):
    
    def setUp(self):
        self.fulcrum_api = Fulcrum(key=key)

    @httpretty.activate
    def test_all(self):
        httpretty.register_uri(httpretty.GET, api_root + '/forms',
            body='{"forms": [{"id": 1},{"id": 2}], "total_count": 2, "current_page": 1, "total_pages": 1, "per_page": 20000}',
            status=200)

        forms = self.fulcrum_api.form.all()
        self.assertIsInstance(forms, dict)
        self.assertEqual(len(forms['forms']), 2)

    @httpretty.activate
    def test_find(self):
        httpretty.register_uri(httpretty.GET, api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778',
            body='{"record_count": 4, "description": "Food Carts and Trucks in Denver", "id": "5b656cd8-f3ef-43e9-8d22-84d015052778"}',
            status=200)
        form = self.fulcrum_api.form.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
        self.assertIsInstance(form, dict)
        self.assertEqual(form['id'], '5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_find_not_found(self):
        httpretty.register_uri(httpretty.GET, api_root + '/forms/lobster', status=404)
        exc = None
        try:
            self.fulcrum_api.form.find('lobster')
        except Exception as exc:
            pass
        self.assertIsInstance(exc, NotFoundException)

    @httpretty.activate
    def test_delete(self):
        httpretty.register_uri(httpretty.DELETE, api_root + '/forms/5b656cd8-f3ef-43e9-8d22-84d015052778', status=200)
        self.fulcrum_api.form.delete('5b656cd8-f3ef-43e9-8d22-84d015052778')

    @httpretty.activate
    def test_create_500(self):
        httpretty.register_uri(httpretty.POST, api_root + '/forms', status=500)
        exc = None
        try:
            self.fulcrum_api.form.create(valid_form)
        except Exception as exc:
            pass
        self.assertIsInstance(exc, InternalServerErrorException)

    def test_create_needs_form(self):
        exc = None
        try:
            self.fulcrum_api.form.create({'cats': True})
        except Exception as exc:
            pass
        self.assertIsInstance(exc, InvalidObjectException)
        self.assertEqual(str(exc), 'form must exist and not be empty.')

    def test_create_invalid_form_name(self):
        try:
            self.fulcrum_api.form.create({'form': {'name': ''}})
        except Exception as exc:
            pass
        self.assertIsInstance(exc, InvalidObjectException)
        self.assertEqual(str(exc), 'form name must exist and not be empty.')

    def test_create_invalid_form_elements(self):
        try:
            self.fulcrum_api.form.create({'form': {'name': 'cats', 'elements': []}})
        except Exception as exc:
            pass
        self.assertIsInstance(exc, InvalidObjectException)
        self.assertEqual(str(exc), 'form elements must exist and not be empty.')





    """
    def test_create_valid_form(self):
        try:
            self.fulcrum_api.form.create({'form': {'name': 'cats', 'elements': [{'foo': 'bar'}]}})
        except Exception as exc:
            pass
        self.assertIsInstance(exc, InvalidObjectException)
        self.assertEqual(str(exc), 'form elements must exist and not be empty.')
    """
