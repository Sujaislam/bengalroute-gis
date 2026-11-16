from django.contrib import admin
from .models import Node, Edge

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'bn_name', 'division', 'region', 'latitude', 'longitude')
    list_filter = ('division', 'region')
    search_fields = ('code', 'name', 'bn_name', 'division', 'description')
    ordering = ('division', 'name')

@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination', 'distance_km', 'is_bidirectional')
    list_filter = ('is_bidirectional',)
    search_fields = ('source__name', 'source__code', 'destination__name', 'destination__code')
    autocomplete_fields = ('source', 'destination')
