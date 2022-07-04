import json
import os

from django.conf import settings
from django.http import Http404, JsonResponse
from django.shortcuts import render
from places.models import Place


def append_json_local(geo_json):
    folder_path = f"{settings.STATICFILES_DIRS[0]}/places/"
    fiels = os.listdir(folder_path)

    for file in fiels:
        file_path = f"{folder_path}{file}"
        with open(file_path, "r", encoding="utf-8") as file:
            file = json.load(file)

            geo_json["features"].append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [file["coordinates"]["lng"], file["coordinates"]["lat"]]
                },
                "properties": {
                    "title": file["title"],
                    "placeId": file["title"],
                    "detailsUrl": f"{settings.STATIC_URL}places/{file['title']}.json"
                }
            })

    return geo_json


def append_json_db(geo_json):
    places = Place.objects.all()

    for place in places:
        geo_json["features"].append({
            "type": "Feature",
            "geometry": {
                    "type": "Point",
                    "coordinates": [place.longitude, place.latitude]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": f"places/{place.id}"
            }
        })

    return geo_json


def show_maps(request):
    geo_json = {
        "type": "FeatureCollection",
        "features": []
    }
    append_json_db(geo_json)
    append_json_local(geo_json)

    data = {"GeoJSON": geo_json}

    return render(request, "index.html", context=data)


def post_detail(request, id):
    try:
        place = Place.objects.get(id=id)
    except Place.DoesNotExist:
        raise Http404("No MyModel matches the given query.")

    response = {
        "title": place.title,
        "imgs": [image.image.url for image in place.images.all()],
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lat": place.latitude,
            "lng": place.longitude
        }
    }

    response = JsonResponse(
        response,
        safe=False,
        json_dumps_params={
            'ensure_ascii': False,
            'indent': 4
        }
    )

    return response
