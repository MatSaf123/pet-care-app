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

    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)

    return country, city, lat, lon


def get_center_coordinates(lat_a, lon_a, lat_b=None, lon_b=None):
    """Compute coordinates of center location between point A and point B
    (If point B is not set yet, point A coordinates are returned).
    :param lat_a: latitude of point A
    :param lon_a: longitude of point A
    :param lat_b: latitude of point B
    :param lon_b: longitude of point B
    :return:
    """

    cord = (lat_a, lon_a)
    if lat_b and lon_b:
        cord = [(lat_a + lat_b) / 2, (lon_a + lon_b) / 2]
    return cord


def initiate_map(posts: django.db.models.QuerySet):
    geolocator = Photon(user_agent='measurements')
    m = folium.Map(width=800, height=500, zoom_start=8)

    for post in posts:
        geo_data = ' '.join([post.street_address, post.city, post.country])
        location = geolocator.geocode(geo_data)
        folium.Marker([location.latitude, location.longitude], tooltip='click here for more', popup=post.title,
                      icon=folium.Icon(color='red')).add_to(m)

    m = m._repr_html_()

    return m
