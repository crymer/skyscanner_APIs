import requests
from authorization.models import FlightsData, OrdersData
from datetime import timedelta, datetime


base_skyscanner_url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/US" \
                      "/USD/en-US/ "


static_order_info = {
    "origin_city": "ATL",
    "destination_city": "MIA",
    "trip_type": "round_trip",
    "trip_price": 80,
    "trip_start_date": "2021-05-05",
    "trip_return_day_interval": 7
}


def create_order_data():
    order_obj = OrdersData.objects.create(**static_order_info)
    return order_obj


def insert_into_flights_db():
    order_var = create_order_data()

    headers = {
        'x-rapidapi-key': "193ace48b5msh63f93010b6db4a1p141edbjsn689f3f56a4d0",
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }

    return_day_interval = order_var.trip_return_day_interval
    date_obj = datetime.strptime(order_var.trip_start_date, "%Y-%m-%d").replace(tzinfo=None)

    trip_end_date = (date_obj + timedelta(days=return_day_interval)).replace(tzinfo=None)

    to_city = order_var.destination_city
    from_city = order_var.origin_city
    start_date = str(order_var.trip_start_date)
    end_date = str(trip_end_date.date())

    if order_var.trip_type == "round_trip":
        params = to_city + "/" + from_city + "/" + start_date + "/" + end_date
    else:
        params = to_city + "/" + from_city + "/" + start_date

    url = base_skyscanner_url + params
    url = url.replace(" ", "")

    response = requests.request("GET", url, headers=headers)
    try:
        if response.status_code == 200:
            response = response.json()
            places_dict = response.get('Places')
            origin_info = places_dict[0]
            destination_info = places_dict[1]
            carrier_dict = response.get('Carriers')[0]
            quote_dict = response.get('Quotes')[0]
            if int(quote_dict['MinPrice']) > order_var.trip_price:
                within_price_range = False
            else:
                within_price_range = True
            FlightsData.objects.create(carrier_id=carrier_dict['CarrierId'],
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
                                       return_date=quote_dict['InboundLeg']['DepartureDate'],
                                       minimum_price=quote_dict['MinPrice'],
                                       is_flight_direct=quote_dict['Direct'],
                                       within_price_range=within_price_range,
                                       trip_type=order_var.trip_type,
                                       country=origin_info['CountryName'])
        else:
            print(response.content)
            return response.content
    except Exception as e:
        print(e.args[0])
        return e.args[0]


def run():
    insert_into_flights_db()