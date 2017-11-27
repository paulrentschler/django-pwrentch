from django import forms


class DetailedChoiceField(forms.ModelChoiceField):
    """Name and code_value labels for choice fields

    Extends:
        forms.ModelChoiceField
    """
    def label_from_instance(self, obj):
        try:
            label = obj.name
        except AttributeError:
            return str(obj)
        else:
            code_fields = (
                'code_value',
                'code_identifier',
                'identifier'
            )
            for code_field in code_fields:
                try:
                    label = "%s (%s)" % (label, getattr(obj, code_field))
                except AttributeError:
                    pass
            return label




class DetailedMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Name and code_value labels for multiple choice fields

    Extends:
        forms.ModelMultipleChoiceField
    """
    def label_from_instance(self, obj):
        try:
            label = obj.name
        except AttributeError:
            return str(obj)
        else:
            code_fields = (
                'code_value',
                'code_identifier',
                'identifier'
            )
            for code_field in code_fields:
                try:
                    label = "%s (%s)" % (label, getattr(obj, code_field))
                except AttributeError:
                    pass
            return label




class DetailedUserChoiceField(forms.ModelChoiceField):
    """User's full name and username for choice fields

    Extends:
        forms.ModelChoiceField
    """
    def label_from_instance(self, obj):
        return '%s (%s)' % (obj.get_full_name(), obj.username)




class DetailedUserMultipleChoiceField(forms.ModelMultipleChoiceField):
    """User's full name and username for multiple choice fields

    Extends:
        forms.ModelMultipleChoiceField
    """
    def label_from_instance(self, obj):
        return '%s (%s)' % (obj.get_full_name(), obj.username)
