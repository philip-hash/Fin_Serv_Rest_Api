from rest_framework import serializers

from apis import models

from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .utils import token_generator


class login_serializer(serializers.Serializer):
    """login Serializer"""
    email = serializers.EmailField(max_length=255)  
    password=serializers.CharField(max_length=255,write_only=True,style={'input_type': 'password', 'placeholder': 'Password'})


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """Create and return a new user"""
        if models.UserProfile.objects.filter(email=validated_data['email']).exists():
                print('email taken')
                return Response({'message': 'Email Already Exist', 'Guide': 'Register with new email Id or Reset Password'})
        else:
            
            request = self.context.get("request")
            user = models.UserProfile.objects.create_user(
                email=validated_data['email'],
                name=validated_data['name'],
                password=validated_data['password']
            )
            uidb64=urlsafe_base64_encode(force_bytes(user.pk))
            domain=get_current_site(request).domain

            link=reverse('activate', kwargs={
                'uidb64':uidb64, 'token':token_generator.make_token(user)
            })
            activateurl='http://'+domain+link
            email_subject="Activation Link"

            email_body='hi '+validated_data['name'] +\
                'Please click through this link and get activate your account\n' +activateurl


            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@fin_serv.com',
                [validated_data['email']],
            )
            email.send(fail_silently=False)
            print('saved successfully')
            

        return user


class Password_Reset_Serializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)    


class Confirm_Password_Serializer(serializers.Serializer):
    new_password=serializers.CharField(max_length=255,write_only=True,style={'input_type': 'password', 'placeholder': 'Password'})
    confirm_password=serializers.CharField(max_length=255,write_only=True,style={'input_type': 'password', 'placeholder': 'Password'})

