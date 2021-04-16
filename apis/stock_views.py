from rest_framework.generics import ListAPIView
from apis import models
from django.contrib.auth.models import auth
from rest_framework.response import Response

class stock_list(ListAPIView):
    def get(self,request):
        lc=models.LargeCap.objects.values_list('name',flat=True) 
        return Response(lc)

#models.LargeCap.objects.filter(name='reliance').values('cp')

class stock_details(ListAPIView):
    def get(self,request,stock):
        try:
            lc=models.LargeCap.objects.filter(name=stock).values()
            if request.user.is_authenticated: 
                if not lc:        
                    return Response({'message':'Company is not available','guide':'Input the company name which are available'})
            else:
                return Response({'message':'Need Login Auth','guide':'Please login to get authorized datas'})    
            return Response(lc)
        except:
            return Response({'message':'Company is not available','guide':'Input the company name which are available'})


class matrix_list(ListAPIView):
    def get(self,request):
        lc=models.LargeCap.objects.all().values()
        col_name=lc[0].keys() 
        return Response(col_name)

class matrix_details(ListAPIView):
    def get(self,request,matrix):
        try:
            lc=models.LargeCap.objects.values('name', matrix)
            if request.user.is_authenticated: 
                if not lc:        
                    return Response({'message':'Matrix is not available','guide':'Fetch with listed matrix name which are available'})
            else:
                return Response({'message':'Need Login Auth','guide':'Please login to get authorized datas'})  
            return Response(lc)
        except:
            return Response({'message':'Matrix is not available','guide':'Fetch with listed matrix name which are available'})

                
        
