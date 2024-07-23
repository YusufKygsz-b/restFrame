from django.urls import path
from news.api import views as api_views


# Function Based Views
# urlpatterns = [
#      path('makaleler/', api_views.makale_list_create_api_view, name='makale-listesi'),
#      path('makaleler/<int:pk>', api_views.makale_detail_api_view, name='makale-detay')
# ]


urlpatterns = [
     path('yazarlar/', api_views.GazeteciListCreateAPIView.as_view() , name='yazar-listesi'),
     path('yazarlar/<int:pk>', api_views.GazeteciDetailAPIView.as_view(), name='yazar-detay'),
     path('makaleler/', api_views.MakeListCreateAPIView.as_view(), name='makale-listesi'),
     path('makaleler/<int:pk>', api_views.MakaleDetailAPIView.as_view(), name='makale-detay')
]
