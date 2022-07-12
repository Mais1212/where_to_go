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
        except requests.exceptions.InvalidSchema or requests.exceptions.MissingSchema:
            print("Кажется, вы ошиблись ссылкой.")
            exit()
        except requests.exceptions.HTTPError:
            print("Сервер не отвечает.")
            exit()

        image_urls = response['imgs']
        place = Place.objects.get_or_create(
            title=response['title'],
            description_short=response['description_short'],
            description_long=response['description_long'],
            latitude=response['coordinates']['lat'],
            longitude=response['coordinates']['lng'],
        )
        for count, image_url in enumerate(image_urls):
            response = requests.get(image_url)
            image_name = f'{place[0].title}_{count}.jpg'
            image = Image.objects.create(
                place=Place.objects.get(id=place[0].id),
            )
            file = ContentFile(response.content)
            image.image.save(image_name, file, save=True)
