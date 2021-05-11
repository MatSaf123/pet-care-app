import django.db.models
from django.contrib.gis.geoip2 import GeoIP2
from geopy import Photon
import folium


def get_geo(ip) -> tuple:
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
    """Get and return user IP address"""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def initiate_map(posts: django.db.models.QuerySet, location: tuple):
    """Initiate and return map with Posts locations marked on it, rendered as a HTML map"""

    geolocator = Photon(user_agent='measurements')
    m = folium.Map(width=500, height=310, location=(location[2], location[3]), zoom_start=8)

    for post in posts:
        geo_data = ' '.join([post.street_address, post.city, post.country])
        location = geolocator.geocode(geo_data)
        folium.Marker([location.latitude, location.longitude], popup=post.title,
                      icon=folium.Icon(color='red')).add_to(m)

    m = m._repr_html_()

    return m
