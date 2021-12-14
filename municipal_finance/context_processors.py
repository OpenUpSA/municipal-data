from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from municipal_finance import models


def google_analytics(request):
    """
    Add the Google Analytics tracking ID and domain to the context for use when
    rendering tracking code.
    """
    ga_id = None
    if not settings.DEBUG:
        if get_current_site(request).name == 'Scorecard':
            ga_id = getattr(settings, 'SCORECARD_GOOGLE_ANALYTICS_ID', None)
        else:
            ga_id = getattr(settings, 'DATA_GOOGLE_ANALYTICS_ID', None)

    return {'GOOGLE_ANALYTICS_ID': ga_id}


def sentry_dsn(request):
    """
    Add the Sentry DSN to the context for use when rendering error reporting code.
    """
    return {'SENTRY_DSN': settings.SENTRY_DSN}


def api_details(request):
    return {
        'DATA_PORTAL_URL': settings.DATA_PORTAL_URL,
        'API_URL': settings.API_URL,
    }

def site_notices(request):
    return {"site_notices": models.Notice.objects.all()}
