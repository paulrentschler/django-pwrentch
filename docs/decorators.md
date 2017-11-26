# Decorators

## @login_required

View decorator that checks that the current user is both logged in **and**
an active user otherwise they are redirected to the login page.

### Example

    from pwrentch.decorators import login_required

    @login_required
    def secured_page_view(request):
        return HttpResponse("Only for logged in, active users")
