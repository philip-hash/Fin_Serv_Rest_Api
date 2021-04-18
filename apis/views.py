
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import status


from apis import serializers
from apis import models

from django.contrib.auth.models import auth

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import token_generator

from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from django.core.mail import EmailMessage
from rest_framework.authentication import BasicAuthentication


import threading
# Create your views here.

class EmailThread(threading.Thread):
    
    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)



class login(CreateAPIView):
    authentication_classes=(BasicAuthentication,)
    serializer_class=serializers.login_serializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data.get('email')
            password=serializer.validated_data.get('password')
            user=auth.authenticate(username = email,password = password)
            if user is not None:
                auth.login(request,user)
                d_user=models.UserProfile.objects.get(email=email)
                
                return Response({'message':'Login Successful','email':user.email,'name':user.name})
            else:
                return Response({'message':'Login Failed','guide':'Invalid credentials'})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class logout(ListAPIView):
    def get(self,request):
        if request.user.is_authenticated: 
            auth.logout(request)
            return Response({'message':'Logout Successful','guide':'Hope to see you soon'})
        else:
            return Response({'message':'Not Logged in','guide':'Hope to see you on board'})


class Register(CreateAPIView):
    """Handle creating profiles"""
    serializer_class = serializers.UserProfileSerializer

    def post(self, request):
        """Create and return a new user"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            v_email=serializer.validated_data.get('email')
            v_name=serializer.validated_data.get('name')
            v_password=serializer.validated_data.get('password')
            if models.UserProfile.objects.filter(email=v_email).exists():
                    print('email taken')
                    return Response({'message': 'Email Already Exist', 'Guide': 'Register with new email Id or Reset Password'})
            else:                
                user = models.UserProfile.objects.create_user(
                    email=v_email,
                    name=v_name,
                    password=v_password
                )
                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                domain=get_current_site(request).domain

                link=reverse('activate', kwargs={
                    'uidb64':uidb64, 'token':token_generator.make_token(user)
                })
                activateurl='http://'+domain+link
                email_subject="Activation Link"

                email_body='hi '+v_name +\
                    'Please click through this link and get activate your account\n' +activateurl


                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@fin_serv.com',
                    [v_email],
                )
                EmailThread(email).start()
                print('saved successfully')
                return Response({'message': 'Registration Successful', 'Guide': 'Please verifiy your email for actiavtion link'})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

            
            

        

class VerificationView(ListAPIView):
    """Email verification for activation"""
    def get(self,request,uidb64,token): #uidb64 and token is derived from link
        id=force_text(urlsafe_base64_decode(uidb64))
        userobj=models.UserProfile.objects.get(pk=id)
        if not token_generator.check_token(userobj,token):
            return Response({'message':'Link is Invalid','guide':'User Already Activated'})
        if userobj.is_active:
            return Response({'message':'Aleady Activated','guide':'Just Try to Login'})
        userobj.is_active = True
        userobj.save()
        return Response({'message':'Successfully Activated','guide':'You can login Now'})

class password_reset(CreateAPIView):
    """password reset request"""
    serializer_class=serializers.Password_Reset_Serializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            v_email=serializer.validated_data.get('email')           
            user=models.UserProfile.objects.get(email=v_email)
            email_content={
                'user':user,
                'domain':get_current_site(request).domain,
                'uidb64':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':PasswordResetTokenGenerator().make_token(user),
            }
            link=reverse('reset-user-password', kwargs={
                'uidb64':email_content['uidb64'], 'token':email_content['token']
            })
            activateurl='http://'+email_content['domain']+link
            email_subject="Password Reset Link"

            email_body='hi there,Please click through this link to reset your account password\n' +activateurl


            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@fin_serv.com',
                [v_email],
            )
            EmailThread(email).start()

            return Response({'message':'Password Reset Mail Send','guide':'Verify your Mail id password reset link'})

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
    

class CompletePasswordReset(CreateAPIView):
    """confirming new password"""
    serializer_class=serializers.Confirm_Password_Serializer


    def post(self,request,uidb64,token):
        serializer = self.serializer_class(data=request.data)
        context={
            'uidb64':uidb64,
            'token':token,
        }
        if serializer.is_valid():
            password=serializer.validated_data.get('new_password')
            password1=serializer.validated_data.get('confirm_password')
            id=force_text(urlsafe_base64_decode(uidb64))
            userobj=models.UserProfile.objects.get(pk=id)
            if not PasswordResetTokenGenerator().check_token(userobj,token):
                return Response({'message':'Link is Invalid','guide':'User Already Activated'})
       
            if password!=password1:
                return Response({'message':'Password Does not match','guide':'Type both password again and make sure both are same'})
            
            if len(password)<5:
                return Response({'message':'Password is too short','guide':'Type Password with characters greater than 5'})

            try:
                user_id=force_text(urlsafe_base64_decode(uidb64))
                user=models.UserProfile.objects.get(pk=user_id)
                user.set_password(password)
                user.save()

                return Response({'message':'Password set successfully','guide':'Try to login with new password'})
            except Exception as identifier:
                return Response({'message':'Something went wrong','guide':'Try to reset password again'})

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )   

        