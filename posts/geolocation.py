import django.db.models
from django.contrib.gis.geoip2 import GeoIP2
from folium.map import Icon
from geopy import Photon
from geopy import location
import folium
from ediblepickle import checkpoint
from django.template.defaultfilters import slugify, time
import os
from django.urls import reverse

def get_geo_from_ip(ip) -> tuple:
    """Get geometrical info from an IP address based on GeoLite2 databases.

    :param ip: user IP address
    :type ip: str
    :return: geometrical data
    """

    try:
        g = GeoIP2()
        country = g.country(ip)
        city = g.city(ip)
        lat, lon = g.lat_lon(ip)
    except Exception:
        # could be more precise with type of exception (AddressNotFoundException)
        country, city, lat, lon = get_geo_from_ip('89.74.26.21')  # Katowice
        
    return country, city, lat, lon


def get_client_ip(request) -> str:
    """Get user IP address from user request.

    :param request: user request
    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def key_namer(args, kwargs) -> str:
    """Create a key value for checkpoint by slugifying address query.

    :param args: location address needed to create cache file name.
    :param kwargs: not used, but without it passed TypeError exception is thrown
    """

    return ''.join([slugify(args[0]), '.geo_cache'])


@checkpoint(key=key_namer, work_dir='geo_cache/', refresh=False)
def get_geo_data_from_api(geo_data: str) -> location.Location:
    """Make a request to remote API for geo data. If the requested
    location was already received from API, use cached data instead.

    :param geo_data: location given by user (post creator)
    """

    # print('Making a call to remote API for:', geo_data)
    geolocator = Photon(user_agent='geopy/2.1.0', timeout=10)
    location = geolocator.geocode(geo_data)

    return location


def initiate_map(posts: django.db.models.QuerySet, location: tuple) -> str:
    """Initiate and return map with Posts locations marked on it, rendered as a HTML map.

    :param posts: Posts saved in database meant to be displayed on a map
    :param location: approximated location of user
    """

    latitude, longitude = location[2], location[3]

    m = folium.Map(width='100%', heigth='100%', location=(
        latitude, longitude), zoom_start=8)

    if not os.path.exists('geo_cache/'):
        os.mkdir('geo_cache/')

    for post in posts:
        geo_data = ' '.join([post.street_address, post.city, post.country])
        location = get_geo_data_from_api(geo_data)

        if post.type_of_post == 'HO':
            color = 'blue'
        else:
            color = 'red'

        url = reverse('post-detail', args=[post.slug])
        folium.Marker([location.latitude, location.longitude], popup=f'<a href="{url}">{post.title}</a>',
                      icon=folium.Icon(icon="info-sign", color=color)).add_to(m)


    m = m.get_root().render()
    return m

