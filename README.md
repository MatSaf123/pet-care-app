# PetCare: web platform to help animals in need

<p float="left">
<img alt="GitHub contributors" src="https://img.shields.io/github/contributors/MatSaf123/pet-care-app?style=plastic"/>
<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/MatSaf123/pet-care-app?style=plastic"/>
</p>

Python-Django powered web platform meant to help organizing volunteer activities towards animals in need, allowing both people in need of help and people willing to help then to communicate and commit to bettering animal lives.

<div style="text-align:center">    <img src="media/readme_pictures/petcare.gif" width="60%" height="60%">
</div>

#

## Run

Get PetCare from Github.
```
git clone https://github.com/MatSaf123/pet-care-app.git

```
Create new virtual environment, activate it and instal requirements.

```
python3 -m venv /path/to/new/virtual/environment

source /path/to/new/virtual/environment/bin/activate

pip install -r requirements.txt
```
Run migrations.

```
python manage.py migrate
```

Get MaxMind GeoLite2 databases from https://dev.maxmind.com/geoip/geolite2-free-geolocation-data and put them into /geoip directory. Required databases:

- GeoLite2-City.mmdb
- GeoLite2-Country.mmdb

Finally, run server.

```
python manage.py runserver
```

Optionally, Create superuser to access admin panel.

```
python manage.py createsuperuser
```

#


## Used technologies: 
- Python 3.8.5
- Django 3.2
- HTML5, CSS, JavaScript
- Bootstrap 4
- GeoLite2 databases
- Leaflet, OSM data

#

## Functionality so far:

- for not logged-in user:
    - browsing posts
    - sorting posts by tags
    - seeing post details
    - displaying user profiles (but no access to contact data)
    - registering, logging in
    - access to 'about' page
    - access to post map
    - map initialization on approximated user location (IP geolocation with GeoLite2)
    - browsing comments on user's profiles
    

- for logged-in user:
    - all of above
    - access to contact data on user profiles
    - creating new posts
    - editing created posts
    - deleting created posts
    - customizing user profile (adding more info, profile photo...)
    - adding and removing own comments on users profiles

#

## Some potential features to be implemented:

- internationalization (adding more languages)
- option to edit comments
- password reset module
- deleting account on user request

## Screens:

<div style="text-align:center">

#### Home screen
<img src="media/readme_pictures/1.png" width="70%" height="70%">

### Post detail screen
<img src="media/readme_pictures/2.png" width="70%" height="70%">

### Users list
<img src="media/readme_pictures/3.png" width="70%" height="70%">

### Users list before and after filtering results
<img src="media/readme_pictures/4.png" width="70%" height="70%">

### User profile detail screen
<img src="media/readme_pictures/5.png" width="70%" height="70%">

### Post creation form
<img src="media/readme_pictures/6.png" width="70%" height="70%">

</div>

## Issues:

- map is embedded in the site, meaning everytime user tries to open link in the popum, internet browser may warn him about potential danger.
This is because of a conflict between Bootstrap and Folium libraries (https://github.com/python-visualization/folium/issues/192). May fix in future.

#

## Legal notes:

This product includes GeoLite2 data created by MaxMind, available from <a href="https://www.maxmind.com">https://www.maxmind.com</a>.

Map technology powered by <a href="https://leafletjs.com/">Leaflet</a> and <a href="https://www.openstreetmap.org">OpenStreetMaps</a>.

#

<div style="text-align:center">
<img src="media/readme_pictures/kapoo.gif" width="30%" height="30%">
</div>

Mateusz Safaryjski / MatSaf123 

2021
