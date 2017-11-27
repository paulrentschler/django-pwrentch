from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import available_attrs

from functools import wraps


def login_required(function=None,
                   redirect_field_name=REDIRECT_FIELD_NAME,
                   login_url=None):
    """Require a logged in AND active user

    Extends the Django login_required decorator to not only check to ensure
    the current user is logged in but also that the user is "active",
    otherwise the visitor is redirected to the login page.

    Keyword Arguments:
        function {obj} -- the function being decorated (default: {None})
        redirect_field_name {str} -- the field name to be included in the
                                     redirect to login page url
                                     (default: {REDIRECT_FIELD_NAME})
        login_url {str} -- the url for the login page (default: {None})

    Returns:
        obj -- the original function wrapped in this decorator
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.is_active,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def never_cache(view_func):
    """Add headers to a view function's HTTP response to avoid caching

    Improves upon Django's built in @never_cache decorator by specifying
    an expiration date in the past and providing the 'Pragma' header.

    Arguments:
        view_func {object} -- the view function being decorated
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        if response.status_code not in (301, 302):
            response['Cache-Control'] = 'no-cache,no-store'
            response['Pragma'] = 'no-cache'
            response['Expires'] = 'Tue, 01 Jan 1980 1:00:00 GMT'
        return response
    return _wrapped_view_func
