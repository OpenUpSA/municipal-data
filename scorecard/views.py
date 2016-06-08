from django.shortcuts import redirect, render_to_response
from django.core.urlresolvers import reverse
from wkhtmltopdf.views import PDFResponse
from wkhtmltopdf.utils import wkhtmltopdf

from wazimap.geo import geo_data
from wazimap.views import GeographyDetailView


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


class GeographyPDFView(GeographyDetailView):
    def get(self, request, *args, **kwargs):
        # render as pdf
        url = '/profiles/%s-%s-%s?pdf=1' % (self.geo_level, self.geo_code, self.geo.slug)
        url = request.build_absolute_uri(url)
        pdf = wkhtmltopdf(url, zoom=0.7)

        return PDFResponse(pdf, filename='foo.pdf')
