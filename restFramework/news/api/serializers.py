'''
from rest_framework import serializers
from news.models import Makale

from datetime import datetime
from django.utils.timesince import timesince


class MakaleSerializer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()
    user_ip = serializers.SerializerMethodField()

    class Meta:
        model = Makale
        fields = '__all__' # Bütün elemanların gösterilmesi sağlanır
        # fields = ['yazar', 'baslik', 'aciklama'] # Sadece istenilen field alanları gösterilir.
        # exclude = ['id'] # Burada yer alanlar hariç geriye kalan her şeyi gösterir
        read_only_fields = ['id', 'yayinlanma_tarihi', 'guncellenme_tarihi']

    def get_time_since_pub(self, object):
        now = datetime.now()
        pub_date = object.yayinlanma_tarihi
        time_delta = timesince(pub_date, now)
        return time_delta
    
    def get_user_ip(self, obj):
        request = self.context.get(request, None)
        if request:
            return request.META.get('REMOTE_ADDR')
        return None


class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayinlanma_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only=True)
    guncellenme_tarihi = serializers.DateTimeField(read_only=True)


# validated_data argumanı arka tarafta belirtilen kuralları işleyerek işleme alır.
# aslında veri doğrulaması yapar.

# validated_data arka planda bir dictionary nesnesinde (görevinde) - ** anlamı validated_datasını aç
# ve key valuelerine eriş ve eşle anlamına gelir
    def create(self, validated_data):
        print(validated_data)
        return Makale.objects.create(**validated_data)

# var olan bir nesnenin güncellenmesi istendiği için, instance nesnesi ile erişim yapılmalı
    def update(self, instance ,validated_data):
        # ilgili field alınır. Dönene validated dataya bak - bunun içerisinde yazar ile alakalı bir değer varsa onu al
        # Eğer yazar alanında bir değer yoksa instance'ın içerisinde bulunan yazar nesnesini kullanmaya devam etmesi sağla

        instance.yazar = validated_data.get('yazar', instance.yazar)
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.aciklama = validated_data.get('aciklama', instance.aciklama)
        instance.metin = validated_data.get('metin', instance.metin)
        instance.sehir = validated_data.get('sehir', instance.sehir)
        instance.yayinlanma_tarihi = validated_data.get ('yayinlanma_tarihi', instance.yayinlanma_tarihi)
        instance.aktif = validated_data.get ('aktif', instance.aktif)
        instance.save()
        return instance


    def validate(self, data): # object Level
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError('Header and Description field are not same. Plase change it.')
        return data
    
    def validate_baslik(self, value): # value = argument value
        length_of_value = len(value)
        if length_of_value < 15:
            raise serializers.ValidationError(f'baslik alanı minimum 20 karakter içermeli. Girilen karakter sayısı: {length_of_value}')
        return value
'''

from rest_framework import serializers
from news.models import Makale, Gazeteci
from datetime import datetime
from django.utils.timesince import timesince


class MakaleSerializer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()
    user_ip = serializers.SerializerMethodField()
    user_info = serializers.SerializerMethodField()
    # yazar = serializers.StringRelatedField()

    class Meta:
        model = Makale
        fields = '__all__'  # Bütün elemanların gösterilmesi sağlanır
        # fields = ['yazar', 'baslik', 'aciklama'] # Sadece istenilen field alanları gösterilir.
        # exclude = ['id'] # Burada yer alanlar hariç geriye kalan her şeyi gösterir
        read_only_fields = ['id', 'yayinlanma_tarihi', 'guncellenme_tarihi']

    def get_time_since_pub(self, obj):
        now = datetime.now()
        pub_date = obj.yayinlanma_tarihi
        time_delta = timesince(pub_date, now)
        return time_delta

    def get_user_ip(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.META.get('REMOTE_ADDR')
        return None

    def get_user_info(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return request.user.username
        return None


class GazeteciSerializer(serializers.ModelSerializer):
    # Makaleler = MakaleSerializer(many = True, read_only = True)
    Makaleler = serializers.HyperlinkedRelatedField(
        many= True,
        read_only = True,
        view_name= 'makale-detay'
    )

    class Meta:
        model = Gazeteci
        fields = '__all__'


class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayinlanma_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only=True)
    guncellenme_tarihi = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Makale.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.yazar = validated_data.get('yazar', instance.yazar)
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.aciklama = validated_data.get('aciklama', instance.aciklama)
        instance.metin = validated_data.get('metin', instance.metin)
        instance.sehir = validated_data.get('sehir', instance.sehir)
        instance.yayinlanma_tarihi = validated_data.get('yayinlanma_tarihi', instance.yayinlanma_tarihi)
        instance.aktif = validated_data.get('aktif', instance.aktif)
        instance.save()
        return instance

    def validate(self, data):  # object Level
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError('Header and Description field are not the same. Please change it.')
        return data

    def validate_baslik(self, value):  # value = argument value
        length_of_value = len(value)
        if length_of_value < 15:
            raise serializers.ValidationError(f'baslik alanı minimum 20 karakter içermeli. Girilen karakter sayısı: {length_of_value}')
        return value
