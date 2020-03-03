import io
import csv
from .models import *
from rest_framework import serializers
from .helpers import   DummyObject
from django.contrib.auth.models import User
from .utils.random_username import generate_random_username
from django.contrib.auth.hashers import make_password
from django.contrib.auth.validators import UnicodeUsernameValidator



class FileUploadSerializer(serializers.Serializer):
    csv_input = serializers.FileField()

    def create(self, validated_data):
        csv_input = validated_data.get("csv_input")
        decoded_file = csv_input.read().decode()
        io_string = io.StringIO(decoded_file)
        input_file = csv.DictReader(io_string)
        
        for row in input_file:

            user = User.objects.create_user(
                username=row.get('username'),
                first_name=row.get('first_name'),
                last_name=row.get('last_name')
            )
             
            user.set_password(User.objects.make_random_password(length=5))
            user.save()
            current_address,_ = Location.objects.get_or_create(
                street=row.get('c_a_street'),
                city=row.get('c_a_city'),
                province=row.get('c_a_province')
            )
            
            permanent_address,_ = Location.objects.get_or_create(
                street=row.get('p_a_street'),
                city=row.get('p_a_city'),
                province=row.get('p_a_province')
            )
           
            customuser= CustomUser.objects.create(
                user=user,
                gender=row.get('gender'),
                email=row.get('email'),
                current_address=current_address,
                permanent_address=permanent_address,
                dob=row.get('dob'),
                martial_status=row.get('martial_status')
                )
            customuser.save()
          
        return  DummyObject(**validated_data)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
   

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name', 'last_name','password',  )
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }  



class CustomUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
     
    current_address = AddressSerializer()
    permanent_address = AddressSerializer()
 
    class Meta:
        model = CustomUser
        fields = ( 'user','email','gender', 'martial_status', 'dob', 'current_address', 
                 'permanent_address','profile_picture')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')
        user = User.object.create_user(**user_data)
        user.set_password(password)
        user.save()
        current_address = validated_data.pop('current_address')
        current_address, _ = Location.objects.get_or_create(**current_address)
        permanent_address = validated_data.pop('permanent_address')
        permanent_address, _ = Location.objects.get_or_create(**permanent_address)

        customuser = CustomUser.objects.create(
            user=user,
            current_address=current_address,
            permanent_address=permanent_address,
            **validated_data
            )
        return customuser

    def update(self, instance, validated_data): 
        user_data = validated_data.pop('user')
        user = instance.user
        user.username = user_data.get('username', user.username)
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()

        ca_data = validated_data.pop('current_address')
        current_address = instance.current_address 
        if current_address:        
            current_address.street = ca_data.get('street',current_address.street)
            current_address.city = ca_data.get('city', current_address.city )
            current_address.province = ca_data.get('province', current_address.city)
            current_address.save()
        else:
            instance.current_address = Location.objects.create(
                **ca_data
            )
            instance.current_address.save()

        pa_data = validated_data.pop('permanent_address')
        permanent_address = instance.permanent_address
        if permanent_address:
            permanent_address.street = pa_data.get('street', permanent_address.street )
            permanent_address.city = pa_data.get('city', permanent_address.city)
            permanent_address.province = pa_data.get('province', permanent_address.province)
            permanent_address.save()
        else:
            instance.permanent_address = Location.objects.create(
                **pa_data
            )
            instance.permanent_address.save()
    
        instance.dob = validated_data.get('dob', instance.dob)
        instance.email = validated_data.get('email', instance.email)
        instance.martial_status = validated_data.get('martial_status',instance.martial_status)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()        
        return instance


           







        
        




    
