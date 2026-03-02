from django.contrib import admin
from .models import Protein, Interaction

class ProteinAdmin(admin.ModelAdmin):
    list_display = ('gene_name', 'uniprot_id', 'protein_name', 'created_at')
    search_fields = ('gene_name', 'uniprot_id', 'protein_name', 'description')
    list_filter = ('created_at',)

class InteractionAdmin(admin.ModelAdmin):
    list_display = ('protein_a', 'protein_b', 'score', 'interaction_type', 'dataset', 'created_at')
    search_fields = ('protein_a__gene_name', 'protein_b__gene_name', 'dataset')
    list_filter = ('interaction_type', 'dataset')

admin.site.register(Protein, ProteinAdmin)
admin.site.register(Interaction, InteractionAdmin)
