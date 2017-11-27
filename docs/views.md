# View helpers

## bad_request_response(request, msg, url, attention='Oops!')

Return the appropriate HTTP Bad Response (400 error) to the browser based on
whether the call was made via AJAX. For an AJAX request, `msg` is returned
as the only response as plain text. Otherwise it prepends `attention` to `msg`
and creates an error message via the Django messages system before redirecting
the browser to `url`. If `attention` is `None` then `msg` is used without
prepending anything.


### Example

    from django.core.urlresolvers import reverse
    from pwrentch.views.util import bad_request_response

    def example_view(request):
        if 'name' not in request.POST:
            return bad_request_response(
                request,
                "You must specify a name",
                reverse('example_form'),
            )



## js_required(request, attention='Heads up!', logger=None)

Generates a message to the user indicating that JavaScript is required.
Typically used by views that are designed to only work when called via AJAX.

If `attention` is not `None`, it is prepended to `msg` and used to create
warning message via the Django messages system.

If `logger` specifies a Python logger, the details of the request will be
logged for future use in debugging or security audits.


### Example

    from django.core.urlresolvers import reverse
    from django.http import HttpResponseRedirect, JsonResponse
    from pwrentch.views.util import js_required

    def ajax_only_view(request):
        if not request.is_ajax():
            js_required()
            return HttpResponseRedirect(reverse('index'))

        # view code for an AJAX request
        return JsonResponse(results)

