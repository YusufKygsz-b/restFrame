from rest_framework import serializers
from news.models import Makale

class MakaleSerializer(serializers.Serializer):
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
    