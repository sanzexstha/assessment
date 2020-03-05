from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.parsers import FileUploadParser
from rest_framework import generics
from myapp.permissions import IsLoggedInUserOrAdmin, IsAdminUser 
from rest_framework.views import APIView
# from .utils.exportcsv import export_to_csv
import csv
from django.http import HttpResponse


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FileUploadSerializer
        return super().get_serializer_class()

  
    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
       
        
        serializer.save()
      

class UserCreateViewSet(generics.CreateAPIView):
     
    serializer_class = CustomUserSerializer
    


from django.http import HttpResponse
import csv
from rest_framework.decorators import api_view, permission_classes



@api_view(['GET'])
@permission_classes([IsAdminUser])
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['first_name', 'last_name', 'username' ])

    users = User.objects.all().values_list('first_name', 'last_name', 'username' )
    for user in users:
        writer.writerow(user)

    return response

# Simple CSV Write Operation
def csv_sample_write(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_simple_write.csv"'

    writer = csv.writer(response)
    writer.writerow(['first_name', 'last_name', 'gender', 'dob', 'email', 'martial_status','c_a_street','c_a_city'
                    ,'c_a_province','p_a_street','p_a_city','p_a_province', 'username'])


    return response


# def get_users_data():
#     queryset = User.objects.only('first_name', 'last_name', 'username', 'email' )
     

#     fields = ['first_name', 'last_name', 'username', 'email']
#     titles = ['first_name', 'first_name' , 'username','email' ]
#     file_name = 'users'
#     return queryset, fields, titles, file_name


# class UsersExportAsCSV(APIView):
#     def get(self, request):
#         users = get_users_data()
#         data = export_to_csv(queryset=users[0], fields=users[1], titles=users[2], file_name=users[3])
#         return data
 

# def get_sample_data():
#         titles = ['first_name', 'first_name' , 'username','email' ]
#         file_name = 'sample'
#         return titles , file_name
