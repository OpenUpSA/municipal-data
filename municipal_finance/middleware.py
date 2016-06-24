import base64

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.conf import settings

from utils import jsonify

import logging

logger = logging.getLogger(__name__)


class ApiErrorHandler(object):
    """ Return API 500-level errors as JSON. """
    def process_exception(self, request, exception):
        if request.path.startswith('/api/'):
            status = getattr(exception, 'http_equiv', 500)
            logger.exception('Something went wrong!')
            return jsonify({
                'status': 'error',
                'message': exception.message,
            }, status=status)


def authenticated(request):
    # Check for valid basic auth header
    if settings.DEBUG:
        return True

    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2 and auth[0].lower() == "basic":
            uname, passwd = base64.b64decode(auth[1]).split(':')
            if uname == settings.HTTP_AUTH_USER and passwd == settings.HTTP_AUTH_PASS:
                return True


class SiteMiddleware(object):
    """ Toggle urls based on site.
    """
    def process_request(self, request):
        site = get_current_site(request)
        if site.name == 'Scorecard':
            # HACK http-basic auth
            if not authenticated(request):
                response = HttpResponse()
                response.status_code = 401
                response['WWW-Authenticate'] = 'Basic realm="private"'
                return response

            request.urlconf = 'scorecard.urls'
        else:
            request.urlconf = 'municipal_finance.urls'
