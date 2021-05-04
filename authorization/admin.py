from django.contrib import admin
from .models import FlightsData, OrdersData

# Register your models here.
@admin.register(FlightsData)
class FlightDataAdmin(admin.ModelAdmin):
    list_display = ('carrier_id', 'carrier_name', 'origin_id', 'origin_airport_name', 'origin_city_name',
                    'origin_skyscanner_code', 'destination_id', 'destination_airport_name', 'destination_city_name',
                    'destination_skyscanner_code', 'departure_date', 'minimum_price', 'created_on', 'is_flight_direct',
                    'within_price_range')

    list_filter = ('origin_city_name', 'destination_city_name', 'departure_date', 'carrier_name', 'minimum_price',
                   'within_price_range')
    search_fields = ('origin_airport_name', 'origin_city_name', 'destination_city_name', 'destination_airport_name',
                     'carrier_name')


def order_dict(modeladmin, request, queryset):
    for x in queryset:
        print(x.__dict__)
order_dict.short_description = 'Ordaaaa Dict'

class OrdersDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'origin_city', 'destination_city', 'trip_start_date', 'trip_price')
    actions =[order_dict, ]

admin.site.register(OrdersData, OrdersDataAdmin)
