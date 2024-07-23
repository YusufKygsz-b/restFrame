from django.db import models

# one-To-Many relations

class Gazeteci(models.Model):
    isim = models.CharField(max_length=120)
    soy_isim = models.CharField(max_length=120)
    biyografi =  models.TextField(blank=True, null= True)

    def __str__(self):
        return f'{self.isim} {self.soy_isim}'
    

class Makale(models.Model):
    yazar = models.ForeignKey(Gazeteci, on_delete = models.CASCADE, related_name = 'Makaleler' )
    baslik = models.CharField(max_length=120)
    aciklama = models.CharField(max_length=200)
    metin = models.TextField()
    sehir = models.CharField(max_length=120)
    yayinlanma_tarihi = models.DateField()
    aktif = models.BooleanField(default=True)
    yaratilma_tarihi = models.DateTimeField(auto_now_add=True)
    guncellenme_tarihi = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.baslik
