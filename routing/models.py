import math
from django.db import models

class Node(models.Model):
    """
    Represents a geographic district (Jela) or city intersection in Bangladesh.
    """
    code = models.CharField(max_length=25, unique=True, help_text="Short identifier e.g. BD_DHK, BD_CTG")
    name = models.CharField(max_length=120, help_text="District/Jela name in English")
    bn_name = models.CharField(max_length=120, blank=True, default="", help_text="District name in Bangla (বাংলা)")
    division = models.CharField(max_length=60, default="Dhaka", help_text="Division name (e.g. Dhaka, Chittagong, Sylhet, etc.)")
    region = models.CharField(max_length=40, default="bangladesh", help_text="e.g. 'bangladesh' (districts) or 'dhaka' (metro)")
    latitude = models.FloatField(help_text="Latitude in decimal degrees")
    longitude = models.FloatField(help_text="Longitude in decimal degrees")
    description = models.TextField(blank=True, default="", help_text="District details and transit notes")

    class Meta:
        ordering = ['division', 'name']

    def __str__(self):
        bn_part = f" ({self.bn_name})" if self.bn_name else ""
        return f"[{self.division}] {self.name}{bn_part} - {self.code}"

    def distance_to(self, other_node):
        """
        Calculates great-circle (Haversine) distance in kilometers to another node.
        """
        R = 6371.0  # Earth radius in kilometers
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other_node.latitude), math.radians(other_node.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = (math.sin(dlat / 2.0) ** 2 +
             math.cos(lat1) * math.cos(lat2) *
             math.sin(dlon / 2.0) ** 2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return round(R * c, 3)


class Edge(models.Model):
    """
    Represents a navigable road or national highway segment between two districts/jelas.
    """
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='outgoing_edges')
    destination = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_edges')
    distance_km = models.FloatField(null=True, blank=True, help_text="Segment length in km (auto-computed if blank)")
    is_bidirectional = models.BooleanField(default=True, help_text="True if travel is allowed in both directions")

    class Meta:
        unique_together = ('source', 'destination')
        ordering = ['source__code', 'destination__code']

    def __str__(self):
        direction = "<->" if self.is_bidirectional else "->"
        return f"{self.source.name} {direction} {self.destination.name} ({self.distance_km} km)"

    def save(self, *args, **kwargs):
        if self.distance_km is None:
            self.distance_km = self.source.distance_to(self.destination)
        super().save(*args, **kwargs)
