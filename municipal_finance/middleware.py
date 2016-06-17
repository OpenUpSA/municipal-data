from django.contrib.sites.shortcuts import get_current_site

from utils import jsonify

import logging

import cProfile
import pstats

logger = logging.getLogger(__name__)


class ApiErrorHandler(object):
    """ Return API 500-level errors as JSON. """
    def process_exception(self, request, exception):
        if request.path.startswith('/api/'):
            status = getattr(exception, 'http_equiv', 500)
            logger.exception(exception.message)
            return jsonify({
                'status': 'error',
                'message': exception.message,
            }, status=status)


class SiteMiddleware(object):
    """ Toggle urls based on site.
    """
    def process_request(self, request):
        site = get_current_site(request)
        if site.name == 'Scorecard':
            request.urlconf = 'scorecard.urls'
        else:
            request.urlconf = 'municipal_finance.urls'


class ProfilingMiddleware(object):
    """
    Profiling Middleware
    """
    def process_request(self, request):
        request.profile = cProfile.Profile()
        request.profile.enable()

    def process_response(self, request, response):
        request.profile.disable()
        url = request.build_absolute_uri()
        sortby = 'cumulative'
        f = open(get_current_site(request).name + '-' + str(hash(url)) + '-profile.log', 'w+')
        f.write("\n%s\n" % url)
        ps = pstats.Stats(request.profile, stream=f).sort_stats(sortby)
        ps.print_stats()
        f.close()
        return response
