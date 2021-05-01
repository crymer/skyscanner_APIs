import itertools
import requests
from authorization.models import FlightsData
from django.utils import timezone
from datetime import timedelta


"""
Add or remove cities according to your need
"""

cities = ['ATL', 'MIA', 'SFO', 'JFK', 'ORD']

base_skyscanner_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US" \
                      "/USD/en-US/ "

final_list = []
bulk_objs = []
date_range = timezone.now().date() + timedelta(days=7)  # 7 days from now


def mirror(data):
    if not isinstance(data, list):
        return data
    return list(map(mirror, reversed(data)))


def insert_into_flights_db(flights_combination):

    headers = {
        'x-rapidapi-key': "193ace48b5msh63f93010b6db4a1p141edbjsn689f3f56a4d0",
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }

    for obj in flights_combination:

        to_city = f"{obj[0]}-sky"
        from_city = f"{obj[1]}-sky"
        date = str(date_range)

        params = to_city + "/" + from_city + "/" + date

        url = base_skyscanner_url + params
        url = url.replace(" ", "")

        response = requests.request("GET", url, headers=headers).json()
        places_dict = response.get('Places')
        origin_info = places_dict[0]
        destination_info = places_dict[1]
        carrier_dict = response.get('Carriers')[0]
        quote_dict = response.get('Quotes')[0]
        bulk_objs.append(FlightsData(carrier_id=carrier_dict['CarrierId'],
                                     carrier_name=carrier_dict['Name'],
                                     origin_id=origin_info['PlaceId'],
                                     origin_airport_name=origin_info['Name'],
                                     origin_city_name=origin_info['CityName'],
                                     origin_skyscanner_code=origin_info['SkyscannerCode'],
                                     destination_id=destination_info['PlaceId'],
                                     destination_airport_name=destination_info['Name'],
                                     destination_city_name=destination_info['CityName'],
                                     destination_skyscanner_code=destination_info['SkyscannerCode'],
                                     departure_date=quote_dict['OutboundLeg']['DepartureDate'],
                                     minimum_price=quote_dict['MinPrice'],
                                     is_flight_direct=quote_dict['Direct'],
                                     country=origin_info['CountryName']))
    FlightsData.objects.bulk_create(bulk_objs)


def run():
    for L in range(0, len(cities)):
        for subset in itertools.combinations(cities, L):
            if len(subset) == 2:
                final_list.append(subset)

    final_list.extend(mirror(data=final_list))
    insert_into_flights_db(flights_combination=final_list)