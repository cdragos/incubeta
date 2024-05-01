ROUTE_CSV_HEADERS = [
    "route",
    "org_country_code",
    "org_country_name",
    "org_station_code",
    "org_station_code2",
    "org_city_name",
    "dst_country_code",
    "dst_country_name",
    "dst_station_code",
    "dst_station_code2",
    "dst_city_name",
    "currency_code",
    "lowest_fare_economy_oneway",
    "lowest_fare_premium_oneway",
    "lowest_fare_economy_return",
    "lowest_fare_premium_return",
    "destination_url_economy_oneway",
    "destination_url_premium_oneway",
    "destination_url_economy_return",
    "destination_url_premium_return",
    "destination_city_image_url",
]

ROUTE_CSV_DATA_SAMPLES = [
    {
        "route": "ESB-IKA",
        "org_country_code": "TR",
        "org_country_name": "Turkey",
        "org_station_code": "ESB",
        "org_station_code2": "ESB",
        "org_city_name": "Ankara",
        "dst_country_code": "IR",
        "dst_country_name": "Iran",
        "dst_station_code": "IKA",
        "dst_station_code2": "IKA",
        "dst_city_name": "Tehran",
        "currency_code": "USD",
        "lowest_fare_economy_oneway": "250",
        "lowest_fare_premium_oneway": "",
        "lowest_fare_economy_return": "444",
        "lowest_fare_premium_return": "",
        "destination_url_economy_oneway": "https://booking.qatarairways.com/nsp/views/showBooking.action?selLang=en&tripType=O&fromStation=ESB&toStation=IKA&departing=2021-11-10&bookingClass=E&adults=1&children=0&infants=0",
        "destination_url_premium_oneway": "",
        "destination_url_economy_return": "https://booking.qatarairways.com/nsp/views/showBooking.action?selLang=en&tripType=R&fromStation=ESB&toStation=IKA&departing=2021-11-10&returning=2021-11-15&bookingClass=E&adults=1&children=0&infants=0",
        "destination_url_premium_return": "",
        "destination_city_image_url": "https://www.qatarairways.com/content/dam/images/custom/FacebookRM/IKA.jpg?ver=2",
    },
    {
        "route": "BLL-KWI",
        "org_country_code": "DK",
        "org_country_name": "Denmark",
        "org_station_code": "BLL",
        "org_station_code2": "BLL",
        "org_city_name": "Billund",
        "dst_country_code": "KW",
        "dst_country_name": "Kuwait",
        "dst_station_code": "KWI",
        "dst_station_code2": "KWI",
        "dst_city_name": "Kuwait",
        "currency_code": "DKK",
        "lowest_fare_economy_oneway": "3101",
        "lowest_fare_premium_oneway": "11674",
        "lowest_fare_economy_return": "4560",
        "lowest_fare_premium_return": "16430",
        "destination_url_economy_oneway": "https://booking.qatarairways.com/nsp/views/showBooking.action?selLang=en&tripType=O&fromStation=BLL&toStation=KWI&departing=2022-02-21&bookingClass=E&adults=1&children=0&infants=0",
        "destination_url_premium_oneway": "https://booking.qatarairways.com/nsp/views/showBooking.action?selLang=en&tripType=O&fromStation=BLL&toStation=KWI&departing=2021-11-11&bookingClass=B&adults=1&children=0&infants=0",
        "destination_url_economy_return": "https://booking.qatarairways.com/nsp/views/showBooking.action?selLang=en&tripType=R&fromStation=BLL&toStation=KWI&departing=2022-03-27&returning=2022-04-01&bookingClass=E&adults=1&children=0&infants=0",
        "destination_url_premium_return": "https://booking.qatarairways.com/nsp/views/showBooking.action?selLang=en&tripType=R&fromStation=BLL&toStation=KWI&departing=2022-03-08&returning=2022-03-14&bookingClass=B&adults=1&children=0&infants=0",
        "destination_city_image_url": "https://www.qatarairways.com/content/dam/images/custom/FacebookRM/KWI.jpg?ver=2",
    },
]
