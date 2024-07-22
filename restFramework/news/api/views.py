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
@api_view(['GET', 'POST'])
def makale_list_create_api_view(request):
    
    if request.method == 'GET':
        makaleler = Makale.objects.filter(aktif=True) # burada nesnelerden oluşan bir query set bulunmakta
        serializer = MakaleSerializer(makaleler, many = True) # query set !!!
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MakaleSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def makale_detail_api_view(request, pk):
    try:
        makale_instance = Makale.objects.get(pk = pk)

    except Makale.DoesNotExist:
        return Response(
            {
                'Errors': {
                    'code': 404,
                    'message': f"This article ({pk}) not found."
                }
            },
            status= status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        if makale_instance.aktif:
            serializer = MakaleSerializer(makale_instance) # JSON'a çevirilir.
            return Response(serializer.data) # JSON formatlı yapıya geri döndürülür.
        
        return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
    
    # Güncelleme Fonksiyonu
    elif request.method == 'PUT':
        serializer = MakaleSerializer(makale_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        makale_instance.delete()
        return Response(
            {
                'islem' : {
                    'code' : 204,
                    'message' : f"({pk}) .th article was deleted."
                }
            },
            status= status.HTTP_204_NO_CONTENT
        )