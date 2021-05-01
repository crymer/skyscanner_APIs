from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(FlightsData)
class FlightDataAdmin(admin.ModelAdmin):
    list_display = ('carrier_id', 'carrier_name', 'origin_id', 'origin_airport_name', 'origin_city_name',
                    'origin_skyscanner_code', 'destination_id', 'destination_airport_name', 'destination_city_name',
                    'destination_skyscanner_code', 'departure_date', 'minimum_price', 'created_on', 'is_flight_direct')

    list_filter = ('origin_city_name', 'destination_city_name', 'departure_date', 'carrier_name', 'minimum_price')
    search_fields = ('origin_airport_name', 'origin_city_name', 'destination_city_name', 'destination_airport_name',
                     'carrier_name')
