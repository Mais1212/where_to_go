from pprint import pprint
import requests
from django.core.management.base import BaseCommand
from places.models import Place, Image
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_url',
            help='Введите ссылку на Json файл'
        )

    def handle(self, *args, **options):
        try:
            response = requests.get(options['json_url'])
            response.raise_for_status()
            response = response.json()
        except requests.exceptions.HTTPError as exception:
            print("Сервер не отвечает.")
            print(exception)
            exit()
        except requests.exceptions.InvalidSchema or requests.exceptions.MissingSchema as exception:
            print("Кажется, вы ошиблись ссылкой.")
            exit()

        image_urls = response['imgs']
        place, __ = Place.objects.get_or_create(
            latitude=response['coordinates']['lat'],
            longitude=response['coordinates']['lng'],
            defaults={
                'title': response['title'],
                'description_short': response['description_short'],
                'description_long': response['description_long']
            },
        )

        for count, image_url in enumerate(image_urls):
            try:
                response = requests.get("https://httpstat.us/404")
                response.raise_for_status()
            except requests.exceptions.HTTPError as exception:
                print('Ошибка в json файле.')
                print(exception)
                exit()
            image_name = f'{place.title}_{count}.jpg'
            image = Image.objects.create(
                place=Place.objects.get(id=place.id),
            )
            file = ContentFile(response.content)
            image.image.save(image_name, file, save=True)
