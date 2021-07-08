from django.apps import AppConfig
import folium


class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
    def ready(self) -> None:

        # Update Bootstrap for Leaflet/Folium map
        
        folium.Map.default_css = [
            ('leaflet_css',
            'https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css'),
            ('bootstrap_css', 'https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'),
            ('bootstrap_theme_css', 'https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap-theme.min.css'),
            ('awesome_markers_font_css', 'https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css'),
            ('awesome_markers_css', 'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css'),
            ('awesome_rotate_css', 'https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css')
            ]

        folium.Map.default_js = [
            ('leaflet', 'https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.js'),
            ('jquery', 'https://code.jquery.com/jquery-1.12.4.min.js'),
            ('bootstrap', 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js'), 
            ('awesome_markers', 'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js')
            ]

        return super().ready()

