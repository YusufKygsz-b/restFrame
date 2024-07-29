# csv: CSV (Comma-Separated Values) dosyalarını okuma ve yazma işlevleri sağlar.
import csv
# types: Python'daki çeşitli türler ve tür kontrol işlevlerini sağlar.
import types

# Django'nun yerleşik hata yönetim modüllerini içerir.
# - FieldDoesNotExist: Model alanlarının var olup olmadığını kontrol ederken kullanılır.
# - ImproperlyConfigured: Django yapılandırma hataları için genel bir istisna sınıfıdır.
from django.core.exceptions import FieldDoesNotExist, ImproperlyConfigured

# Django'da HTTP yanıtları oluşturmak için kullanılan temel yanıt sınıflarını sağlar.
from django.http.response import HttpResponse
# Django' da karakter dizilerini doğru şekilde işlemek için kullanılan fonksiyonları içerir. 
from django.utils.encoding import force_str

# Django'nun genel görünüm sınıflarını içerir.

# - View: Tüm görünüm sınıflarının temelini oluşturan sınıftır.
from django.views.generic.base import View
# - MultipleObjectMixin: Birden fazla nesne ile çalışan görünüm sınıfları için karışım sınıfıdır.
from django.views.generic.list import MultipleObjectMixin


'''
1) _get_method_type:
------------------------------
Bu fonksiyon, Python'daki bir sınıf yöntemi (method) nesnesinin tipini belirlemek için kullanılır.
Bu, özel metodların sınıf içinde nasıl saklandığını anlamak için faydalıdır.

2) ExampleClass:
------------------------------
ExampleClass adında basit bir sınıf tanımlanır. Bu sınıf, bir örnek metod olan example_method içerir.
Bu metod, sınıfın içindeki bir metodun tipini belirlemek için kullanılır.

3) type(ExampleClass.example_method):
------------------------------
ExampleClass sınıfındaki example_method metodunun tipini döndürür.
Bu tip, sınıf içindeki diğer metodları tanımlamak ve kontrol etmek için kullanılabilir.

4) _method_type:
------------------------------
_method_type değişkeni, ExampleClass içindeki metodların tipini saklar. Bu bilgi,
sınıf içinde metodların nasıl tanımlandığını veya değiştirildiğini kontrol etmek için kullanılabilir.
'''

def _get_method_type():
    # Define a simple class with a method
    class ExampleClass:
        def example_method(self):
            pass

    # Get the type of the 'example_method' method from ExampleClass
    return type(ExampleClass.example_method)

# Store the method type in a variable for later use
_method_type = _get_method_type()


class CSVExportView(MultipleObjectMixin, View):
    # CSV dosyası için dahil edilecek alanlar (field) listesi
    fields = None
    # CSV dosyasından hariç tutulacak alanlar listesi
    exclude = None
    # CSV dosyasına başlık eklenip eklenmeyeceği
    header = True
    # Alan adlarının okunabilir isimlerle gösterilip gösterilmeyeceği
    verbose_names = True
    # Excel için faydalı olan ayracı belirtme özelliği
    specify_separator = True
    # Oluşturulacak CSV dosyasının adı
    filename = None

    # CSVExportView tarafından desteklenmeyen bazı View varsayılanlarını geçersiz kılar.
    paginate_by = None
    paginator_class = None
    page_kwarg = None
    allow_empty = True
    context_object_name = None

    def __init__(self, **kwargs):
        # Üst sınıf başlatıcısını çağırır
        super().__init__(**kwargs)

        # get_fields metodunun üzerine yazılıp yazılmadığını kontrol eder
        get_fields_overridden = False
        for cls in self.__class__.__mro__:
            if cls == CSVExportView:
                # CSVExportView'e ulaşıldığında kontrolü durdurur
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


         # Ensure specific methods are not overridden.
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
    

    def get_fields(self, queryset):
        """Eğer dinamik alanlar gerekiyorsa bu metod üzerine yazılabilir."""
        field_names = self.fields
        # Eğer alanlar belirtilmemişse veya "__all__" ise modelin tüm alanlarını alır
        if not field_names or field_names == "__all__":
            opts = queryset.model._meta
            field_names = [field.name for field in opts.fields]

        if self.exclude:
            # exclude içindeki alanlar field_names'den çıkarılır
            exclude_set = set(self.exclude)
            field_names = [name for name in field_names if name not in exclude_set]
            # field_names = list(set(field_names) - exclude_set)

        return field_names

    # Eğer self.filename tanımlıysa, onu kullanır.
    # Eğer self.filename tanımlı değilse, modelin çoğul adını (verbose_name_plural) alır ve içindeki boşlukları tire ile değiştirir.
    
    def get_filename(self, queryset):
        return self.filename or queryset.model._meta.verbose_name_plural.replace(" ", "-")

    # def get_filename(self, queryset):
    #     """Dinamik bir dosya adı gerekiyorsa bu metod üzerine yazılabilir."""
    #     filename = self.filename
    #     if not filename:
    #         # Modelin verbose_name_plural özelliğini kullanarak dosya adı oluşturur
    #         filename = queryset.model._meta.verbose_name_plural.replace(" ", "-")
    #     return filename
    

    def get_field_value(self, obj, field_name):
        """Belirli alanlar için özel bir değer veya davranış gerekiyorsa bu metod üzerine yazılabilir."""
        if "__" not in field_name:
            if hasattr(obj, "all") and hasattr(obj, "iterator"):
                # İlişkili tüm nesnelerin field_name alanlarını birleştirir
                return ",".join([getattr(ro, field_name) for ro in obj.all()])

            try:
                field = obj._meta.get_field(field_name)
            except FieldDoesNotExist as e:
                if not hasattr(obj, field_name):
                    raise e
                # Eğer field_name bir özellikse onun değerini döndür
                return getattr(obj, field_name)

            if field.many_to_one:
                return str(getattr(obj, field_name))

            value = field.value_from_object(obj)
            if field.many_to_many:
                # Çoktan çoğa ilişkilerde değerleri birleştirir
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
            return self.get_field_value(related_obj, related_field_name)

    def get_header_name(self, model, field_name):
        """Belirli alanlar için özel bir başlık gerekiyorsa bu metod üzerine yazılabilir."""
        if "__" not in field_name:
            try:
                field = model._meta.get_field(field_name)
            except FieldDoesNotExist as e:
                if not hasattr(model, field_name):
                    raise e
                 # field_name bir özellik ise, onun adını döndür
                return field_name.replace("_", " ").title()

            if self.verbose_names:
                return force_str(field.verbose_name).title()
            else:
                return force_str(field.name)
        else:
            related_field_names = field_name.split("__")
            field = model._meta.get_field(related_field_names[0])
            if not field.is_relation:
                raise ImproperlyConfigured("{} is not a relation".format(field))
            return self.get_header_name(field.related_model, "__".join(related_field_names[1:]))

    def get_csv_writer_fmtparams(self):
        """CSV yazıcı için format parametrelerini döndürür."""
        return {
            "dialect": "excel",
            "quoting": csv.QUOTE_ALL,
        }

    def get(self, request, *args, **kwargs):
        # Queryset'i alır
        queryset = self.get_queryset()

        # Alan isimlerini alır
        field_names = self.get_fields(queryset)

        # CSV dosyası için bir HTTP yanıtı başlatır
        response = HttpResponse(content_type="text/csv")

        # Dosya adını belirler
        filename = self.get_filename(queryset)
        if not filename.endswith(".csv"):
            filename += ".csv"
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)

         # CSV yazıcıyı oluşturur
        writer = csv.writer(response, **self.get_csv_writer_fmtparams())

        # Ayracı belirtir (Excel için yararlı)
        if self.specify_separator:
            response.write("sep={}{}".format(writer.dialect.delimiter, writer.dialect.lineterminator))

        # Başlık satırını yazar (Opsiyonel)
        if self.header:
            writer.writerow([self.get_header_name(queryset.model, field_name) for field_name in list(field_names)])

        # Her nesne için alan değerlerini yazar
        for obj in queryset:
            writer.writerow([self.get_field_value(obj, field) for field in field_names])

        # HTTP yanıtını döndürür
        return response
        