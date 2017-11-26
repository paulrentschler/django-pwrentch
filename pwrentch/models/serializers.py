from django.utils.html import escape


class ToDict(object):
    """Convert a model instance to a Python dict

    Usage:
        x = MyModel.objects.get(pk=1)
        x_dict = ToDict(x).data
    """

    # Model fields that could contain unsafe HTML characters
    html_unsafe_fields = (
        'CharField',
        'EmailField',
        'PhoneNumberField',
        'SlugField',
        'TextField',
        'URLField',
        'UUIDField',
    )


    def __init__(self, instance, **options):
        """Initialize the instance

        Orchestrates the conversion of `instance` into a Python dict which is
        available via `self.data`

        Arguments:
            instance {object} -- Model instance to convert to a Python dict

        Keyword Arguments (options):
            'exclude' {list} -- list of field names to exclude from the dict
                                representation. Overrides excluded fields
                                specified via the model's
                                `_todict_exclude_fields` attribute.
                                Excludes fields even if listed in `fields`.
            'fields' {list} -- if provided, only the fields listed will be
                               included in the generated dict
            'html_safe' {boolean} -- indicates if the dict values should be
                                     escaped to make them safe for displaying
                                     as HTML. (Default: False)
            'recursive' {boolean} -- when True referenced objects are also
                                     converted to dict recursively. When
                                     False, just the referenced object's
                                     primary key is specified. (Default: True)
            'todict' {boolean} -- when True indicates that the serializer
                                  is being called from `instance.to_dict()`
                                  and the check for a `to_dict` method is
                                  skipped to avoid an infinite loop problem.
                                  (Default: False)
        """
        try:
            self.exclude_fields = instance._meta.model._todict_exclude_fields
        except AttributeError:
            self.exclude_fields = []
        try:
            self.exclude_fields = options['exclude']
        except KeyError:
            pass
        try:
            self.fields = options['fields']
        except KeyError:
            self.fields = []
        self.html_safe = True if options['html_safe'] is True else False
        self.recursive = False if options['recursive'] is False else True
        self._use_to_dict = False if options['todict'] is False else True
        self.serialize(instance)


    @property
    def data(self):
        try:
            return self._data
        except AttributeError:
            return {}


    def _filter_fields(self):
        """Filter `self._data` to only include `self.fields`"""
        if self.fields:
            for field in self._data.keys():
                if field not in self.fields:
                    del self._data[field]


    def _get_field_value(self, instance, field):
        """Returns the value of the field specified

        Arguments:
            instance {object} -- Model instance that has `field`
            field {object} -- The field object on `instance`

        Returns:
            {various} -- Returns the value of `instance`.`field`. When `field`
                         is a foreign key field, the object referenced is
                         returned.
        """
        try:
            value = field.value_from_object(instance)
        except AttributeError:
            return None
        if field.many_to_many or not field.is_relation:
            return value
        try:
            value.pk
        except AttributeError:
            klass = field.related_model
            try:
                value = klass.objects.get(pk=value)
            except (AttributeError, KeyError, klass.DoesNotExist):
                value = None
        return value


    def _get_file_reference(self, file_obj):
        """Python dict representation of a FileField/ImageField file

        Arguments:
            file_obj {object} -- The value from a FileField or ImageField

        Returns:
            {dict} -- Python dict of the FileField/ImageField file
        """
        try:
            return {
                'url': file_obj.url,
                'name': file_obj.name if not self.html_safe else escape(file_obj.name),  # NOQA
                'size': file_obj.size,
            }
        except ValueError:
            return None


    def _get_foreign_key_reference(self, instance):
        """Python dict representation of a foreign key value

        Arguments:
            instance {object} -- the model instance referenced by the
                                 foreign key field

        Returns:
            {dict} -- Python dict of the referenced model instance
        """
        if not self.recursive:
            return instance.pk
        options = {
            'html_safe': self.html_safe,
            'recursive': self.recursive,
            'todict': False,
        }
        return ToDict(instance, **options).data


    def _get_many_to_many_references(self, instances):
        """List of Python dict representations of the many-to-many values

        Arguments:
            instances {list} -- list of referenced model instances to be
                                converted to Python dicts

        Returns:
            {list} -- List of Python dicts for each of the referenced model
                      instances
        """
        if not self.recursive:
            return [instance.pk for instance in instances]
        return [
            self._get_foreign_key_reference(instance)
            for instance in instances
        ]


    def __model2dict_user(self, instance, **kwargs):
        """Custom model to dict conversion for User model

        This is a custom conversion method used to limit the default fields
        output for a User model instance so sensitive data isn't exposed.

        Arguments:
            instance {object} -- Model instance to convert to a Python dict
        """
        if not self.fields and not self.exclude_fields:
            self.fields = [
                'id',
                'username',
                'first_name',
                'last_name',
                'email',
                'is_active',
            ]
            self.exclude_fields = ['password', 'groups', 'user_permissions']
        self._model_to_dict(instance)


    def _model_to_dict(self, instance):
        """Orchestrate the work of converting the model instance to a dict

        Arguments:
            instance {object} -- Model instance to convert to a Python dict
        """
        for field in instance._meta.get_fields():
            if self.fields and field.name not in self.fields:
                continue
            if self.exclude_fields and field.name in self.exclude_fields:
                continue
            try:
                field_type = field.get_internal_type()
            except AttributeError:
                # skips reverse relationship fields
                continue
            value = self._get_field_value(instance, field)
            if value is not None:
                try:
                    # convert date-related objects to ISO strings
                    value = value.isoformat()
                except AttributeError:
                    if field_type in ('FileField', 'ImageField'):
                        value = self._get_file_reference(value)
                    elif field.many_to_many:
                        value = self._get_many_to_many_references(value)
                    elif field.is_relation:
                        value = self._get_foreign_key_reference(value)
                    elif field_type in self.html_unsafe_fields:
                        value = escape(value)
            self._data[field.name] = value


    def _remove_excluded_fields(self):
        """Removes `self.exclude_fields` fields from `self._data`"""
        for field in self.exclude_fields:
            del self._data[field]


    def serialize(self, instance):
        """Convert from model instance to Python dict using various methods

        This is called from self.__init__()

        Arguments:
            instance {object} -- Model instance to convert to a Python dict
        """
        self._data = {}
        if self._use_to_dict:
            try:
                self._data = instance.to_dict(html_safe=self.html_safe)
            except AttributeError:
                # instance.to_dict() doesn't exist
                pass
            except TypeError:
                try:
                    self._data = instance.to_dict()
                except AttributeError:
                    # instance.to_dict() doesn't exist
                    pass
        if self._data:
            # apply the serializer options even if to_dict() didn't
            self._remove_excluded_fields()
            self._filter_fields()
            self._simplify_recursive_references()
        else:
            # build the dict representation
            try:
                custom_method = '__model2dict_' + instance._meta.model.name
                getattr(self, custom_method)(instance)
            except AttributeError:
                self._model_to_dict(instance)


    def _simplify_recursive_references(self):
        """Replaces recursive references with the primary key value

        Replaces fields with dict values with the dict's `pk` or `id` key's
        value. If none is found, the value is left untouched as is the case
        with FileField/ImageField values.
        """
        if not self.recursive:
            for field, value in self._data.iteritems():
                if isinstance(value, dict):
                    try:
                        self._data[field] = value['pk']
                    except KeyError:
                        try:
                            self._data[field] = value['id']
                        except KeyError:
                            pass
