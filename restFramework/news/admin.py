from django.contrib import admin
from news.models import Makale, Gazeteci
from export_model.views import CSVExportView

admin.site.register(Gazeteci)

@admin.register(Makale)
class DataAdmin(admin.ModelAdmin):
    actions = ['export_data_csv']

    def export_data_csv(self, request, queryset):
        view = CSVExportView(queryset=queryset, fields="__all__")
        return view.get(request)

    export_data_csv.short_description = "CSV Formatonda çıktı al"
