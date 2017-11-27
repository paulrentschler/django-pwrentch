from django.contrib import messages
from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
)


def bad_request_response(request, msg, url, attention='Oops!'):
    """Return the appropriate bad request response depending on AJAX usage

    Arguments:
        request {object} -- HTTP request object
        msg {string} -- Error message to provide back to the user
        url {string} -- URL to redirect the user to if the request is not AJAX

    Keyword arguments:
        attention {string} -- Attention getting word(s) that are prepended
                              to `msg`. If `None` nothing is prepended to
                              `msg`. (Default: "Oops!")
    """
    if request.is_ajax:
        return HttpResponseBadRequest(msg, content_type='text/plain')
    else:
        if attention is not None:
            msg = "<strong>{0}</strong> {1}".format(attention, msg)
        messages.error(request, msg)
        return HttpResponseRedirect(url)


def js_required(request, attention='Heads up!', logger=None):
    """Message to inform the user that JavaScript is required

    Arguments:
        request {object} -- HTTP request object

    Keyword arguments:
        attention {string} -- Attention getting words that start the message.
                              (Default: "Heads up!")
        logger {object} -- Python logger to record this failure
    """
    msg = (
        "The feature you just requested requires JavaScript. "
        "Please verify that you have JavaScript enabled in your browser"
        "and if this problem persists, please contact the developers."
    )
    if attention is not None:
        msg = "<strong>{0}</strong> {1}".format(attention, msg)
    messages.warning(request, msg)

    if logger is not None:
        try:
            remote_addr = request.META['REMOTE_ADDR']
        except KeyError:
            remote_addr = 'unknown'
        try:
            http_referer = request.META['HTTP_REFERER']
        except KeyError:
            http_referer = 'unknown'
        logger.info("{0} {1} accessed via non-AJAX call by {2} via {3}".format(  # NOQA
            request.method,
            request.get_full_path(),
            remote_addr,
            http_referer
        ))
