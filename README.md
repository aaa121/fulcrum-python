# fulcrum-python

[![Build Status](https://api.travis-ci.org/fulcrumapp/fulcrum-python.png)](https://travis-ci.org/fulcrumapp/fulcrum-python)&nbsp;[![PyPI version](https://img.shields.io/pypi/v/fulcrum.svg)](https://pypi.python.org/pypi/fulcrum/)

A library for working with [Fulcrum API](http://fulcrumapp.com/developers/api/)

## Installation

Install via pip:

    pip install fulcrum

or from local sources:

    python setup.py install

## Dependencies

Just one - [Requests](http://docs.python-requests.org/en/latest/) takes care of our HTTP chatting, and is automatically installed when using the steps above.

## Supported Resources and Methods

| Resource            | Methods                              |
|---------------------|--------------------------------------|
| Forms               | find, search, create, update, delete |
| Records             | find, search, create, update, delete |
| Photos              | find, search                         |
| Projects            | find, search, create, update, delete |
| Changesets          | find, search, create, update, close  |
| Choice Lists        | find, search, create, update, delete |
| Classification Sets | find, search, create, update, delete |
| Webhooks            | find, search, create, update, delete |
| Videos              | find, search                         |
| Memberships         | search                               |
| Roles               | search                               |

## Usage

Create a fulcrum client with your API key.

```python
from fulcrum import Fulcrum
fulcrum = Fulcrum(key='super-secret-key')
```

Various methods are available for each of the resources. Check the table above for details. Results are returned as python-equivalent dicts of the JSON returned from the API. Check the [Fulcrum API Docs](http://fulcrumapp.com/developers/api/) for examples of returned objects.

### Find

Finds a single resource. The single parameter is a resource id.

```python
form = fulcrum.forms.find('5b656cd8-f3ef-43e9-8d22-84d015052778')
print(form['form']['name'])  # Denver Street Food
```

### Search

Search for resources. The single parameter is `url_params` which should be passed as a dict, and will be properly url encoded. These will vary depending on the resource, but [pagination parameters](http://www.fulcrumapp.com/developers/api/introduction/#notes) are always accepted.

```python
records = fulcrum.records.search(url_params={'form_id': 'a1cb3ac7-146f-491a-a4a2-47737fb12074'})
print(len(records['records']))  # 9
print(records['records'][0]['id'])  # c90b0edf-0299-42df-bed4-524446d63f40
```

### Create

Create an object. The single parameter is a dict representation of a JSON object that will be POSTed to the API. Check the [Fulcrum API Docs](http://fulcrumapp.com/developers/api/) for examples of resource objects.

```python
a_record = {
    'record': {
        'form_values': {
            'cbaf': 'A field value'
        },
        'form_id': 'a1cb3ac7-146f-491a-a4a2-47737fb12074'
    }
}
record = fulcrum.records.create(a_record)
print(record['record']['id'])  # e58e80a8-9376-4a31-8e31-3cba95af0b4b
```

### Update

Update an object. Parameters are an id, and dict representation of the JSON object that will be updated.

```python
an_updated_record = {
    'record': {
        'form_values': {
            'cbaf': 'An updated field value'
        },
        'form_id': 'a1cb3ac7-146f-491a-a4a2-47737fb12074'
    }
}
record = fulcrum.records.update('e58e80a8-9376-4a31-8e31-3cba95af0b4b', an_updated_record)
print(record['record']['form_values']['cbaf'])  # An updated field value
```

### Delete

Delete a resource. Delete returns `None` on success and raises `fulcrum.exceptions.NotFoundException` if the API returns a 404 (no resource found).

```python
fulcrum.records.delete('e58e80a8-9376-4a31-8e31-3cba95af0b4b')  # Returns None (assuming the record is found and deleted)
fulcrum.records.delete('a-bogus-resource-id')  # Raises fulcrum.exceptions.NotFoundException
```

## Testing

You'll need some additional things to run tests, so:

    pip install -r test_requirements.txt

Run the tests:

    nosetests

You can get coverage too.

    nosetests --with-coverage --cover-package fulcrum

View coverage.

    coverage html
