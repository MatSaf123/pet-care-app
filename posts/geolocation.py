import django.db.models
from django.contrib.gis.geoip2 import GeoIP2
from geopy import Photon
import folium
from ediblepickle import checkpoint
from django.template.defaultfilters import slugify
import os

def get_geo_from_ip(ip) -> tuple:
    """Get geometrical info from an IP address based on GeoLite2 databases.

    :param ip: user IP address
    :type ip: str
    :return: geometrical data
    """

    #########################
    # Practically just for testing purposes, because GeoLite2 doesn't contain 127.0.0.1 IP address
    # TODO: remove when done testing
    if ip == '127.0.0.1':
        ip = '89.74.26.21'  # Katowice
    #########################

    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)

    return country, city, lat, lon


def get_client_ip(request):
    """Get user IP address from user request

    :param request: user request
    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def key_namer(args, kwargs):
    """Create a key value for checkpoint by slugifying address query

    :param args: location address needed to create cache file name.
    :param kwargs: not used, but without it passed TypeError exception is thrown
    """

    return ''.join([slugify(args[0]), '.geo_cache'])


@checkpoint(key=key_namer, work_dir='geo_cache/', refresh=False)
def get_geo_data_from_api(geo_data: str):
    """Make a request to remote API for geo data

    :param geo_data: location given by user (post creator)
    """

    print('Making a call to remote API for:', geo_data)
    geolocator = Photon(user_agent='measurements')
    location = geolocator.geocode(geo_data)
    print('Returned: ',location)
    return location


def initiate_map(posts: django.db.models.QuerySet, location: tuple):
    """Initiate and return map with Posts locations marked on it, rendered as a HTML map

    :param posts: Posts saved in database meant to be displayed on a map
    :param location: approximated location of user
    """

    latitude = location[2]
    longitude = location[3]

    m = folium.Map(width=500, height=310, location=(
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

        url = f'<a href="/post/{post.slug}/">{post.title}</a>'

        folium.Marker([location.latitude, location.longitude], popup=url,
                      icon=folium.Icon(color=color)).add_to(m)


    m = m._repr_html_()
    #m = m.get_root().render()
    return m

