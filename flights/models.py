from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    # 'updated_at' is nullable and only set when an object is updated for the first time.
    # This helps distinguish between objects that have never been modified and those that have.
    # Potential issue: Setting 'updated_at' on new objects with a value different from 'created_at'
    # may give the impression that the object has been modified, even if it has not.
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]


class Currency(BaseModel):
    code = models.CharField(max_length=3, primary_key=True)

    def __str__(self):
        return self.code


class Country(BaseModel):
    iso_alpha2 = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(name="unq_country_iso_alpha2", fields=["iso_alpha2"]),
            models.Index(name="idx_country_name", fields=["name"]),
        ]

    def __str__(self):
        return self.name


class City(BaseModel):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(name="unq_city_name_country", fields=["name", "country"]),
        ]

    def __str__(self):
        return self.name


class Station(BaseModel):
    code = models.CharField(max_length=3)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(name="unq_station_code", fields=["code"]),
        ]

    def __str__(self):
        return self.code


class Route(BaseModel):

    # Currency for this route, ForeignKey to Currency model (e.g., "DKK")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    # Destination city of the route, linked to the City model
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="destination_city_routes")
    # Destination country of the route, linked to the Country model
    destination_country = models.ForeignKey(
        Country, on_delete=models.PROTECT, related_name="destination_country_routes"
    )
    # Destination station of the route, linked to the Station model
    destination_station = models.ForeignKey(
        Station, on_delete=models.PROTECT, related_name="destination_stating_routes"
    )
    # Origin city of the route, linked to the City model
    origin_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="origin_city_routes")
    # Origin country of the route, linked to the Country model
    origin_country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="origin_country_routes")
    # Origin station of the route, linked to the Station model
    origin_station = models.ForeignKey(Station, on_delete=models.PROTECT, related_name="origin_stating_routes")
    # Image URL of the destination city, optional (e.g., "https://example.com/image.jpg")
    destination_city_image_url = models.URLField(max_length=500, blank=True, default="")
    # Unique route identifier (e.g., "ESB-IKA")
    route_code = models.CharField(max_length=100)

    class Meta(BaseModel.Meta):
        constraints = [
            models.UniqueConstraint(name="unq_route_route_code", fields=["route_code"]),
        ]

    def __str__(self):
        return self.route_code
