import os

import geocoder
import folium
import json
import datetime

from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.encoding import force_str

from ipware import get_client_ip
from .models import UserData


def index(request):
    user_agent = request.user_agent
    ip_address = get_client_ip(request)[0]
    ip_geocoder = geocoder.ip(ip_address)
    location = ip_geocoder.latlng

    # logging to stdout for docker
    print(f"User agent: {request.user_agent}")
    print(f"Client IP: {get_client_ip(request)}")
    print(f"IP Address: {ip_address}")
    print(f"location: {ip_geocoder.latlng}")
    print(f"Address: {ip_geocoder.city}, {ip_geocoder.state}, {ip_geocoder.country}")
    print(f"Timestamp: {datetime.datetime.now()}")

    try:
        map = folium.Map(location=location, zoom_start=10)
        folium.CircleMarker(location=location, radius=50, color="red").add_to(map)
        folium.Marker(location).add_to(map)
        user = UserData.objects.create(
            ip_address=ip_address,
            user_agent=force_str(user_agent),
            address=f"{ip_geocoder.city}, {ip_geocoder.state}, {ip_geocoder.country}",
            location=json.dumps(ip_geocoder.latlng),
        )
        map.save(os.path.join(settings.MAPS_LOCATION, f"user_{user.id}-{ip_address}.html"))

    # to broad exception, pass on
    except:
        print("Error has accrued in folium map generation")
    return redirect(settings.REDIRECTED_URL)


def display_map(request, id):
    user = UserData.objects.get(pk=id)
    user_id = user.id
    user_ip_address = user.ip_address
    map_file = f"user_{user_id}-{user_ip_address}.html"
    return render(request, map_file)
