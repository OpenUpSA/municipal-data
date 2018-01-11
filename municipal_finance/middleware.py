from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponsePermanentRedirect

from .utils import jsonify

import logging

logger = logging.getLogger(__name__)


class ApiErrorHandler(object):
    """ Return API 500-level errors as JSON. """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    
    def process_exception(self, request, exception):
        if request.path.startswith('/api/'):
            status = getattr(exception, 'http_equiv', 500)
            logger.exception('Something went wrong!')
            return jsonify({
                'status': 'error',
                'message': exception.message,
            }, status=status)


class SiteMiddleware(object):
    """ Toggle urls based on site.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)
    
    def process_request(self, request):
        site = get_current_site(request)
        if site.name == 'Scorecard':
            request.urlconf = 'scorecard.urls'
        else:
            request.urlconf = 'municipal_finance.urls'

class RedirectsMiddleware(object):
    """Always redirect www.host to host"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if response is None:
            return self.get_response(request)
        else:
            return response
    
    def process_request(self, request):
        host = request.get_host()
        if host.startswith("www."):
            return HttpResponsePermanentRedirect("https://%s/" % host[4:])
