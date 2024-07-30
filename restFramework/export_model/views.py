# csv: CSV (Comma-Separated Values) dosyalarını okuma ve yazma işlevleri sağlar.
import csv
# types: Python'daki çeşitli türler ve tür kontrol işlevlerini sağlar.
import types
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured
from django.http import HttpResponse
from django.utils.encoding import force_str

# - View: Tüm görünüm sınıflarının temelini oluşturan sınıftır.
from django.views.generic.base import View
# - MultipleObjectMixin: Birden fazla nesne ile çalışan görünüm sınıfları için karışım sınıfıdır.
from django.views.generic.list import MultipleObjectMixin

# _get_method_type fonksiyonu, Python'daki bir sınıf yöntemi (method) nesnesinin tipini belirlemek için kullanılır.
from .partials.method_type import _get_method_type

_method_type = _get_method_type()

# CSV için yardımcı sınıf
class CSVHelper:
    @staticmethod
    def write_csv_header(writer, field_names, model, verbose_names=True):
        header = [CSVHelper.get_header_name(model, field_name, verbose_names) for field_name in field_names]
        writer.writerow(header)

    @staticmethod
    def get_header_name(model, field_name, verbose_names):
        if "__" in field_name:
            related_field_names = field_name.split("__")
            field = model._meta.get_field(related_field_names[0])
            if not field.is_relation:
                raise ImproperlyConfigured(f"{field} is not a relation")
            return CSVHelper.get_header_name(field.related_model, "__".join(related_field_names[1:]), verbose_names)
        
        field = model._meta.get_field(field_name)
        if not field:
            if hasattr(model, field_name):
                return field_name.replace("_", " ").title()
            raise FieldDoesNotExist(f"{field_name} does not exist in {model.__name__}")
        
        return force_str(field.verbose_name if verbose_names else field.name).title()

    @staticmethod
    def write_csv_rows(writer, queryset, field_names):
        for obj in queryset:
            row = [CSVExportView.get_field_value(obj, field) for field in field_names]
            writer.writerow(row)

class CSVExportView(MultipleObjectMixin, View):
    fields = None # CSV dosyası için dahil edilecek alanlar (field) listesi
    exclude = None # CSV dosyasından hariç tutulacak alanlar listesi
    header = True # CSV dosyasına başlık eklenip eklenmeyeceği
    verbose_names = True # Alan adlarının okunabilir isimlerle gösterilip gösterilmeyeceği
    specify_separator = True # Excel için faydalı olan ayracı belirtme özelliği
    filename = None # Oluşturulacak CSV dosyasının adı

    # CSVExportView tarafından desteklenmeyen bazı View varsayılanlarını geçersiz kılar
    paginate_by = None
    paginator_class = None
    page_kwarg = None
    allow_empty = True
    context_object_name = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._check_configuration()
    
    def _check_configuration(self):
        self._check_fields_override()
        self._check_disallowed_overrides()

    def _check_fields_override(self): # get_fields metodunun üzerine yazılıp yazılmadığını kontrol eder
        get_fields_overridden = False 
        for cls in self.__class__.__mro__:
            if cls == CSVExportView:
                break
            if hasattr(cls, "get_fields") and isinstance(getattr(cls, "get_fields"), _method_type):
                get_fields_overridden = True
                break
            
        # Eğer get_fields üzerine yazılmamışsa, fields veya exclude'un doğru yapılandırıldığını kontrol eder
        if not get_fields_overridden:
            if not self.fields and not self.exclude:
                raise ImproperlyConfigured("'fields' veya 'exclude' belirtilmelidir.")
            if self.fields and self.exclude:
                raise ImproperlyConfigured("'fields' ve 'exclude' aynı anda belirtilmemelidir.")

    def _check_disallowed_overrides(self):
        disallowed_overrides = ["get_context_data", "get_paginate_by", "get_allow_empty", "get_context_object_name"]
        for func in disallowed_overrides:
            if func in self.__class__.__dict__ and isinstance(self.__class__.__dict__[func], _method_type):
                raise ImproperlyConfigured(f"Overriding '{func}()' izin verilmez.")
        if self.paginate_by:
            raise ImproperlyConfigured(f"'{self.__class__.__name__}' pagination desteklemez.")
        if not self.allow_empty:
            raise ImproperlyConfigured(f"'{self.__class__.__name__}' allow_empty devre dışı bırakılmasını desteklemez.")
        if self.context_object_name:
            raise ImproperlyConfigured(f"'{self.__class__.__name__}' context_object_name ayarlanmasını desteklemez.")
    
    # Eğer dinamik alanlar gerekiyorsa bu metod üzerine yazılabilir
    # Eğer alanlar belirtilmemişse veya "__all__" ise modelin tüm alanlarını alır
    def get_fields(self, queryset):
        field_names = self.fields
        if not field_names or field_names == "__all__":
            opts = queryset.model._meta
            field_names = [field.name for field in opts.fields]

    # exclude içindeki alanlar field_names'den çıkarılır
        if self.exclude:
            exclude_set = set(self.exclude)
            field_names = [name for name in field_names if name not in exclude_set]
        return field_names

    # Eğer self.filename tanımlıysa, onu kullanır.
    # Eğer self.filename tanımlı değilse, modelin çoğul adını (verbose_name_plural) alır ve içindeki boşlukları tire ile değiştirir.
    def get_filename(self, queryset):
        filename = self.filename or queryset.model._meta.verbose_name_plural.replace(" ", "-")
        return f"{filename}.csv" if not filename.endswith(".csv") else filename

    @staticmethod
    def get_field_value(obj, field_name):
        if "__" not in field_name:
            if hasattr(obj, "all") and hasattr(obj, "iterator"):
                return ",".join([getattr(ro, field_name) for ro in obj.all()])
            try:
                field = obj._meta.get_field(field_name)
            except FieldDoesNotExist as e:
                if not hasattr(obj, field_name):
                    raise e
                return getattr(obj, field_name)
            value = field.value_from_object(obj)
            if field.many_to_many:
                return ",".join([force_str(ro) for ro in value])
            elif field.choices:
                if value is None or force_str(value).strip() == "":
                    return ""
                return dict(field.choices)[value]
            return value
        else:
            # İlişkili alanlar için özel davranış
            related_field_names = field_name.split("__")
            related_obj = getattr(obj, related_field_names[0])
            related_field_name = "__".join(related_field_names[1:])
            return CSVExportView.get_field_value(related_obj, related_field_name)

    def get_csv_writer_fmtparams(self):
        return {
            "dialect": "excel",
            "quoting": csv.QUOTE_ALL,
        }

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        field_names = self.get_fields(queryset)
        response = HttpResponse(content_type="text/csv")
        filename = self.get_filename(queryset)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'

        writer = csv.writer(response, **self.get_csv_writer_fmtparams())

        if self.specify_separator:
            response.write(f"sep={writer.dialect.delimiter}{writer.dialect.lineterminator}")

        if self.header:
            CSVHelper.write_csv_header(writer, field_names, queryset.model, self.verbose_names)

        CSVHelper.write_csv_rows(writer, queryset, field_names)

        return response
