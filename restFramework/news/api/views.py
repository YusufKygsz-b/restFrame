from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from news.models import Makale
from news.api.serializers import MakaleSerializer

#api_view decorator (function based view yaratabilmek için)
# APIView classes
# Browsable API

# Bu yapılar sayesinde, sunucumuza gelen istekleri, ya da gönderilen
# responsları kontrol etmek için gerekli tüm kodlar hazır gelecektir.


# api view içerisinde bir liste içerisinde kullanılacak olan metod
# yazılmalı
@api_view(['GET'])
def makale_list_create_api_view(request):
    
    if request.method == 'GET':
        makaleler = Makale.objects.filter(aktif=True) # burada nesnelerden oluşan bir query set bulunmakta
        serializer = MakaleSerializer(makaleler) # query set !!!
        return Response(serializer.data)