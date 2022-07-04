import os
import requests
from django.core.management.base import BaseCommand
from places.models import Place, Image
from django.conf import settings
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_url',
            help='Введите ссылку на Json файл'
        )

    def handle(self, *args, **options):
        response_json = requests.get(options['json_url']).json()
        image_urls = response_json['imgs']
        place = Place.objects.get_or_create(
            title=response_json['title'],
            description_short=response_json['description_short'],
            description_long=response_json['description_long'],
            latitude=response_json['coordinates']['lat'],
            longitude=response_json['coordinates']['lng'],
        )
        for count, image_url in enumerate(image_urls):
            response = requests.get(image_url)
            image_name = f'{place[0].title}_{count}.jpg'
            image = Image.objects.create(
                place=Place.objects.get(id=place[0].id),
            )
            file = ContentFile(response.content)
            image.image.save(image_name, file, save=True)
