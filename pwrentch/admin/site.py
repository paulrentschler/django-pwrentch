from django.conf import settings
from django.contrib.admin import AdminSite

from pwrentch.decorators import never_cache


class PwrentchAdminSite(AdminSite):
    """Uncached custom named Django admin site

    Extends:
        AdminSite
    """
    def __init__(self, name='admin'):
        """Set site title and header based on settings.APPLICATION_NAME"""
        super(PwrentchAdminSite, self).__init__(name)
        try:
            app_name = settings.APPLICATION_NAME
        except AttributeError:
            pass
        else:
            if app_name:
                self.site_title = app_name
                self.site_header = "{0} Settings".format(app_name)
                self.index_title = "Application settings"


    def admin_view(self, view, cacheable=False):
        """Apply @never_cache to the AdminSite.admin_view() functional view"""
        view_function = super(PwrentchAdminSite, self).admin_view(view, cacheable)  # NOQA
        return never_cache(view_function)


    @never_cache
    def app_index(self, request, app_label, extra_context=None):
        return super(PwrentchAdminSite, self).app_index(request, app_label, extra_context)  # NOQA


    @never_cache
    def index(self, request, extra_context=None):
        return super(PwrentchAdminSite, self).index(request, extra_context)


    @never_cache
    def login(self, request, extra_context=None):
        return super(PwrentchAdminSite, self).login(request, extra_context)


    @never_cache
    def logout(self, request, extra_context=None):
        return super(PwrentchAdminSite, self).logout(request, extra_context)


    @never_cache
    def password_change(self, request, extra_context=None):
        return super(PwrentchAdminSite, self).password_change(request, extra_context)  # NOQA


    @never_cache
    def password_change_done(self, request, extra_context=None):
        return super(PwrentchAdminSite, self).password_change_done(request, extra_context)  # NOQA
