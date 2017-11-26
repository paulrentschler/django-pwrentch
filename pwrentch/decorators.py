from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


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
