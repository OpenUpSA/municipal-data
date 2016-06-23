from django.shortcuts import redirect, render_to_response
from django.views.generic.base import TemplateView
from django.http import Http404
from django.core.urlresolvers import reverse
from wkhtmltopdf.views import PDFResponse
from wkhtmltopdf.utils import wkhtmltopdf

from wazimap.geo import geo_data
from wazimap.data.utils import LocationNotFound

from scorecard.profiles import get_profile


def locate(request):
    lat = request.GET.get('lat', None)
    lon = request.GET.get('lon', None)
    nope = False

    if lat and lon:
        place = None
        places = geo_data.get_locations_from_coords(latitude=lat, longitude=lon)

        if places:
            place = places[0]

            # if multiple, prefer the metro/local municipality if available
            if len(places) > 1:
                places = [p for p in places if p.geo_level == 'municipality']
                if places:
                    place = places[0]

            return redirect(reverse('geography_detail', kwargs={'geography_id': place.geoid}))
        nope = True

    return render_to_response('locate.html', {
        'nope': nope,
        'lat': lat,
        'lon': lon,
    })


class GeographyDetailView(TemplateView):
    template_name = 'profile/profile_detail.html'

    def dispatch(self, *args, **kwargs):
        self.geo_id = self.kwargs.get('geography_id', None)

        try:
            self.geo_level, self.geo_code = self.geo_id.split('-', 1)
            self.geo = geo_data.get_geography(self.geo_code, self.geo_level)
        except (ValueError, LocationNotFound):
            raise Http404

        # check slug
        if kwargs.get('slug') or self.geo.slug:
            if kwargs['slug'] != self.geo.slug:
                kwargs['slug'] = self.geo.slug
                url = '/profiles/%s-%s-%s' % (self.geo_level, self.geo_code, self.geo.slug)
                return redirect(url, permanent=True)

        return super(GeographyDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        page_context = {}

        profile = get_profile(self.geo_code, self.geo_level)
        page_context.update(profile)

        profile['geography'] = self.geo.as_dict()
        page_context['profile_data'] = profile
        page_context['geography'] = self.geo

        # is this a head-to-head view?
        if 'head2head' in self.request.GET:
            page_context['head2head'] = 'head2head'

        return page_context


class GeographyPDFView(GeographyDetailView):
    def get(self, request, *args, **kwargs):
        # render as pdf
        url = '/profiles/%s-%s-%s?print=1' % (self.geo_level, self.geo_code, self.geo.slug)
        url = request.build_absolute_uri(url)
        pdf = wkhtmltopdf(url, zoom=0.7)
        filename = '%s-%s-%s.pdf' % (self.geo_level, self.geo_code, self.geo.slug)

        return PDFResponse(pdf, filename=filename)


class GeographyCompareView(TemplateView):
    template_name = 'profile/head2head.html'

    def get_context_data(self, geo_id1, geo_id2):
        page_context = {
            'geo_id1': geo_id1,
            'geo_id2': geo_id2,
        }

        try:
            level, code = geo_id1.split('-', 1)
            page_context['geo1'] = geo_data.get_geography(code, level)

            level, code = geo_id2.split('-', 1)
            page_context['geo2'] = geo_data.get_geography(code, level)
        except (ValueError, LocationNotFound):
            raise Http404

        return page_context
