from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import *
 
 


class UserViewSetTestCase(APITestCase):
              
    def setUp(self):
        self.admin = User.objects.create_user(username='sanjeev', password='sanjeev', is_staff=True)
        self.admin.save()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')
        self.user.save()

        self.customuser = CustomUser.objects.create(user=self.user)
        self.customuser.save()

        self.list_url = reverse('user-list')
     
        self.client = APIClient()
        self.client.login(username='sanjeev', password='sanjeev')
        
    def test_get_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         

    def test_get_detail(self):     
        response = self.client.get(reverse('user-detail', args=[self.customuser.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
           


    def test_post(self):

        with open('/home/sanjeev1/Documents/test.csv', 'rb') as image:
            response = self.client.post(reverse('user-list'), data= { 'csv_input': image}, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)         
  

    def test_put(self):
        data = {
                
                "user": {
                "id": self.user.id,
                "username": "vqz0-xjzb-ytiz-7k1a",
                "first_name": "ram",
                "last_name": "khatri",
                "password": "sanjeev",
                },
                "martial_status": "Single",
                "dob": "1990-01-02",
                "current_address":  {
                    "street": "sanchwok",
                    "city": "kathmandu",
                    "province": "2"
                },
                "permanent_address": {
                    "street": "bhanuchowk",
                    "city": "dharan",
                    "province": "6"
                },
                
                'gender': 'Male',
            }
            
        response = self.client.put(
                reverse('user-detail', args=[self.customuser.id]),
                data=data,
                format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#            

    def test_delete(self):
        response = self.client.delete(reverse('user-detail', args=[self.customuser.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        


