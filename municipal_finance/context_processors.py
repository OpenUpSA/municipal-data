from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from site_config.models import SiteNotice


def google_analytics(request):
    """
    Add the Google Analytics tracking ID and domain to the context for use when
    rendering tracking code.
    """
    ga_id = None

    if get_current_site(request).name == "Scorecard":
        ga_id = getattr(settings, "SCORECARD_GOOGLE_ANALYTICS_ID", None)
        gtag = getattr(settings, "SCORECARD_GOOGLE_TAG", None)
    else:
        ga_id = getattr(settings, "DATA_GOOGLE_ANALYTICS_ID", None)
        gtag = getattr(settings, 'DATA_GOOGLE_TAG', None)

    return {"GOOGLE_ANALYTICS_ID": ga_id, "GOOGLE_TAG": gtag}


def search_engine_index(request):
    """
    Prevent a specific site from being indexed by search engines
    """
    return {'NO_INDEX': settings.NO_INDEX}


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
    return {"site_notices": SiteNotice.objects.all()}
