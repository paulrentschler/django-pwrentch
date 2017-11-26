# Serializers

Serializers allow model instances to be converted to native Python datatypes
that can then be easily rendered into JSON, XML, or other content types.


## ToDict(instance, **options)

Serializer to convert a model instance to a Python dict containing only native
Python datatypes which can then be converted to JSON, XML, or other content
formats as necessary.

The class has numerous options and is module to allow for subclassing.


### Options

#### exclude=[]

Optionally provide a list of model fields that **should** not be included in
the resulting Python dict.

This can also be specified directly in the model by defining a
`_todict_exclude_fields` attribute. Passing the option will override the
model's attribute.


#### fields=[]

Optional list of the **only** model fields to include in the resulting Python
dict. Fields listed in the `exclude` option or the `_todict_exclude_fields`
attribute will **not** be included even if listed here.


#### html_safe=True/False

When set to `True` all text values will be escaped to ensure that it is safe
to be included in an HTML document without introducing HTML code.

The default is `False`.


#### recursive=True/False

When set to `True` all referenced objects (i.e., foreign keys, many-to-many
relationships, etc) are also converted to Python dicts.

When set to `False` all referenced objects are specified by just their primary
key value. In the case of many-to-many relationships, they are specified as a
list of primary key values.

The default is `True`.


#### todict=True/False

Indicates the class is being instanciated from a model
instance's `to_dict()` method.

The default is `False`.

Allows a model to define a `to_dict()` method that uses this `ToDict()`
serializer without creating a cyclic reference provided `todict=True` is
used when the `to_dict()` instanciates `ToDict`.


#### Basic usage example

    x = MyModel.objects.get(pk=1)
    x_dict = ToDict(x).data


#### Advanced usage examples

    state_college = City(
        id=1,
        name='State College',
        postal_code='16801',
    )
    x = Business(
        name="Barnes & Noble",
        city=state_college,
        grand_opening_date=datetime(2001, 1, 1),
    )
    # output the converted dict with no special options
    ToDict(x).data
    {
        'name': 'Barnes & Noble',
        'city': {
            'id': 1,
            'name': 'State College',
            'postal_code': '16801',
        },
        grand_opening_date: '2001-01-01T00:00:00',
    }

    # escape the text so it's HTML safe
    ToDict(x, html_safe=True).data
    {
        'name': 'Barnes &amp; Noble',
        'city': {
            'id': 1,
            'name': 'State College',
            'postal_code': '16801',
        },
        grand_opening_date: '2001-01-01T00:00:00',
    }

    # don't include the recursive objects
    ToDict(x, recursive=False).data
    {
        'name': 'Barnes & Noble',
        'city': 1,
        grand_opening_date: '2001-01-01T00:00:00',
    }

    # only output the name as html safe text
    ToDict(x, fields=('name',), html_safe=True).data
    {
        'name': 'A&amp;P Supermarket',
    }

    # exclude the grand opening date
    ToDict(x, exclude=['grand_opening_date']).data
    {
        'name': 'Barnes & Noble',
        'city': {
            'name': 'State College',
            'postal_code': '16801',
        },
    }
