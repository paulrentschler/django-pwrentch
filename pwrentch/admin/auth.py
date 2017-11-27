from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import (
    GroupAdmin as auth_GroupAdmin,
    UserAdmin as auth_UserAdmin,
)

from pwrentch.admin.fields import DetailedUserMultipleChoiceField


class GroupAdminForm(forms.ModelForm):
    """Display username and full name when selecting Users

    Extends:
        forms.ModelForm
    """
    users_queryset = get_user_model().objects.order_by('last_name', 'first_name')  # NOQA
    users = DetailedUserMultipleChoiceField(
        users_queryset,
        widget=admin.widgets.FilteredSelectMultiple('Users', False),
        required=False,
    )


    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            initial_users = self.instance.user_set.values_list('pk', flat=True)  # NOQA
            self.initial['users'] = initial_users


    def save(self, *args, **kwargs):
        kwargs['commit'] = True
        return super(GroupAdminForm, self).save(*args, **kwargs)


    def save_m2m(self):
        self.instance.user_set.clear()
        self.instance.user_set.add(*self.cleaned_data['users'])




class GroupAdmin(auth_GroupAdmin):
    form = GroupAdminForm




class UserAdmin(auth_UserAdmin):
    """Display more data and make more things clickable in the list view

    Extends:
        auth_UserAdmin
    """
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_display_links = ('username', 'first_name', 'last_name')
