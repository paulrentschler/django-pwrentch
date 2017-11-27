# Decorators

## @login_required

View decorator that checks that the current user is both logged in **and**
an active user otherwise they are redirected to the login page.

### Example

    from django.http import HttpResponse
    from pwrentch.decorators import login_required

    @login_required
    def secured_page_view(request):
        return HttpResponse("Only for logged in, active users")



## @never_cache

View decorator to prevent the client (browser) from caching the content by
providing the appropriate HTTP response headers.

### Example

    from django.http import HttpResponse
    from pwrentch.decorators import never_cache

    @never_cache
    def not_cached_page_view(request):
        return HttpResponse("Your browser should never cache this")
