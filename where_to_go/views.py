import json
import os

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.templatetags.static import static
from django.urls import reverse
from places.models import Place


def load_local_json():
    folder_path = os.path.join("static_src", "places\\")
    file_names = os.listdir(folder_path)
    features = []

    for file_name in file_names:
        file_path = f"{folder_path}{file_name}"
        with open(file_path, "r", encoding="utf-8") as file_content:
            file_content = json.load(file_content)
        file_id = f"{file_content['title']}.json"

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [file_content["coordinates"]["lng"], file_content["coordinates"]["lat"]]
            },
            "properties": {
                "title": file_content["title"],
                "placeId": file_content["title"],
                "detailsUrl": static(reverse("places", args=(file_id, )))
            }
        })

    return features


def load_data_base_json():
    places = Place.objects.all()
    features = []

    for place in places:
        features.append({
            "type": "Feature",
            "geometry": {
                    "type": "Point",
                    "coordinates": [place.longitude, place.latitude]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse("places", args=(place.id,))
            }
        })

    return features


def show_maps(request):
    geo_json = {
        "type": "FeatureCollection",
        "features": []
    }
    data_base_json = load_data_base_json()
    local_json = load_local_json()
    geo_json["features"].extend(data_base_json)
    geo_json["features"].extend(local_json)

    context = {"GeoJSON": geo_json}

    return render(request, "index.html", context=context)


def post_detail(request, id):
    place = get_object_or_404(Place, id=id)

    detiles = {
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
        detiles,
        safe=False,
        json_dumps_params={
            'ensure_ascii': False,
            'indent': 4
        }
    )

    return response
