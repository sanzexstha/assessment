from django.conf.urls import url, include
from .views import *
from rest_framework import routers
from django.urls import path

router = routers.DefaultRouter()
router.register(r'user', UserViewSet , basename='user')
 
 
urlpatterns = [
   
    url(r'^', include(router.urls )),
    path('users/create', UserCreateViewSet.as_view()),
    path('users-csv-export', UsersExportAsCSV.as_view()),
    path('sample-csv-export/', csv_sample_write, name='sample'),

]

