from django.contrib import admin
from .models import Protein

class ProteinAdmin(admin.ModelAdmin):
    list_display = ('gene_name', 'uniprot_id', 'protein_name', 'created_at')
    search_fields = ('gene_name', 'uniprot_id', 'protein_name', 'description')
    list_filter = ('created_at',)

admin.site.register(Protein, ProteinAdmin)
