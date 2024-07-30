from django.shortcuts import render
from news.models import Makale
from export_model.views import CSVExportView

class DataExportView(CSVExportView):
    model = Makale
    fields = '__all__'
    filename = "Makaleler.csv"

# Create your views here.
