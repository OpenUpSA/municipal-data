from django.shortcuts import redirect, render_to_response
from django.core.urlresolvers import reverse


from wazimap.geo import geo_data


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
