from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from news.models import Makale, Gazeteci
from news.api.serializers import MakaleSerializer, GazeteciSerializer
from rest_framework.views import APIView

from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from news.api.permissions import IsSuperUserOnly

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView


class GazeteciListCreateAPIView(ListCreateAPIView):
    queryset = Gazeteci.objects.all()
    serializer_class = GazeteciSerializer
    # Permission section feature field (Definitaion of exclusive permission)
    # Test User (Normal User)
    # ad523A6t.
    permission_classes = [IsSuperUserOnly]

class GazeteciDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Gazeteci.objects.all()
    serializer_class = GazeteciSerializer
    permission_classes = [permissions.IsAdminUser]


class MakeListCreateAPIView(ListCreateAPIView):
    queryset = Makale.objects.filter(aktif=True)
    serializer_class = MakaleSerializer
    permission_classes = [permissions.IsAdminUser]

"""
class MakaleDetailAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView ):
    
    queryset = Makale.objects.all()
    serializer_class = MakaleSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""

class MakaleDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Makale.objects.all()
    serializer_class = MakaleSerializer
    permission_classes = [permissions.IsAdminUser]

"""
# class MakeListCreateAPIView(APIView):
#     def get(self, request):
#         makaleler = Makale.objects.filter(aktif=True)
#         serializer = MakaleSerializer(makaleler, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = MakaleSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class GazeteciListCreateAPIView(APIView):
#     def get(self, request):
#         yazarlar = Gazeteci.objects.all()
#         serializer = GazeteciSerializer(yazarlar, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = GazeteciSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""    


# class MakaleDetailAPIView(APIView):
#     def get_object(self, pk):
#         makale_instance = get_object_or_404(Makale, pk=pk)
#         return makale_instance

#     def get(self, request, pk):
#         makale = self.get_object(pk=pk)
#         serializer = MakaleSerializer(makale, context={'request': request})
#         return Response(serializer.data)

#     def put(self, request, pk):
#         makale = self.get_object(pk=pk)
#         serializer = MakaleSerializer(makale, data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         makale = self.get_object(pk=pk)
#         makale.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

"""
#api_view decorator (function based view yaratabilmek için)
# APIView classes
# Browsable API

# Bu yapılar sayesinde, sunucumuza gelen istekleri, ya da gönderilen
# responsları kontrol etmek için gerekli tüm kodlar hazır gelecektir.

# api view içerisinde bir liste içerisinde kullanılacak olan metod
# yazılmalı

# @api_view(['GET', 'POST'])
# def makale_list_create_api_view(request):
    
#     if request.method == 'GET':
#         makaleler = Makale.objects.filter(aktif=True) # burada nesnelerden oluşan bir query set bulunmakta
#         serializer = MakaleSerializer(makaleler, many = True) # query set !!!
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = MakaleSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
#         Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def makale_detail_api_view(request, pk):
    # try:
    #     makale_instance = Makale.objects.get(pk = pk)

    # except Makale.DoesNotExist:
    #     return Response(
    #         {
    #             'Errors': {
    #                 'code': 404,
    #                 'message': f"This article ({pk}) not found."
    #             }
    #         },
    #         status= status.HTTP_404_NOT_FOUND
    #     )
    
    # if request.method == 'GET':
    #     if makale_instance.aktif:
    #         serializer = MakaleSerializer(makale_instance) # JSON'a çevirilir.
    #         return Response(serializer.data) # JSON formatlı yapıya geri döndürülür.
        
    #     return Response(status= status.HTTP_405_METHOD_NOT_ALLOWED)
    
    # # Güncelleme Fonksiyonu
    # elif request.method == 'PUT':
    #     serializer = MakaleSerializer(makale_instance, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
        
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # elif request.method == 'DELETE':
    #     makale_instance.delete()
    #     return Response(
    #         {
    #             'islem' : {
    #                 'code' : 204,
    #                 'message' : f"({pk}) .th article was deleted."
    #             }
    #         },
    #         status= status.HTTP_204_NO_CONTENT
    #     )
    """