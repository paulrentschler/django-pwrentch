## Admin System components

The Django Admin System is incredibly powerful and useful but that's not to
say it couldn't stand some improvements.


## PwrentchAdminSite

A customized Django Admin System site class that incorporates the
`never_cache` decorator on all views and uses an optional `APPLICATION_NAME`
value in settings.py to update the various titles and names in the admin site.


### Example

    from pwrentch.admin.site import PwrentchAdminSite

    admin_site = PwrentchAdminSite(name='myadmin')



## Better User and Group admins

Display more information when listing users and allow users to be added when
editing a group.

The user and group admins aren't registered by default, so register them
once an instance of `AdminSite` has been defined (see above).


### Example

    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group
    from pwrentch.admin.auth import GroupAdmin, UserAdmin

    admin_site.register(Group, GroupAdmin)
    admin_site.register(get_user_model(), UserAdmin)



## Better select and multi-select values

Depending on how the models are defined, the choices presented for selecting
a foreign key or many-to-many value can be very cryptic. Thus
`DetailedChoiceField` and `DetailedMultipleChoiceField` provide a more
detailed choice to pick such that each entry follows the format:

    name (identifier)

Where _name_ is the `name` attribute of the object and _identifier_ is the
first of these attributes found:

* `code_value`
* `code_identifier`
* `identifier`


### Example

    from django import forms
    from django.contrib import admin
    from django.db import models
    from pwrentch.admin.fields import DetailedChoiceField

    class Address(models.Model):
        street1 = models.CharField(max_length=40)
        street2 = models.CharField(max_length=40)
        city = models.CharField(max_length=35)
        state = models.ForeignKey('State')
        postal_code = models.CharField(max_length=20)


    class State(models.Model):
        code_value = models.CharField(max_length=2)
        name = models.CharField(max_length=200)

        def __str__(self):
            return self.name


    class AddressForm(forms.ModelForm):
        state = DetailedChoiceField(
            queryset=State.objects.all(),
            required=False
        )


    class AddressAdmin(admin.ModelAdmin):
        form = AddressForm


Now instead of the state selector in the address admin being just a list of
names (e.g., Delaware, Maryland, New York, Pennsylvania) it will include the
state abbreviation (code_value) as well
(e.g., Delaware (DE), Maryland (MD), etc).
