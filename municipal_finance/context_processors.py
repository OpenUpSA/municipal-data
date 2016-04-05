import urllib

from django.conf import settings
from django.core.urlresolvers import reverse

def google_analytics(request):
    """
    Add the Google Analytics tracking ID and domain to the context for use when
    rendering tracking code.
    """
    ga_tracking_id = getattr(settings, 'GOOGLE_ANALYTICS_ID', False)
    if not settings.DEBUG and ga_tracking_id:
        return {
            'GOOGLE_ANALYTICS_ID': ga_tracking_id,
        }
    return {}
