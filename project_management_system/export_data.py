from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from project_management.models import ProjectSite

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Define the mapping between model fields and shapefile geometry types
        mapping = {
            'site_coordinates': 'POINT',
            'site_area': 'POLYGON',
            'way_to_home': 'LINESTRING',
        }

        # Create a LayerMapping instance, specifying the model, output shapefile path, and mapping
        lm = LayerMapping(ProjectSite, 'project_management/files/shapefile.shp', mapping)

        # Save the data to the shapefile, with strict and verbose options
        lm.save(verbose=True)
