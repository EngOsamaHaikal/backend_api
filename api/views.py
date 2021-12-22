from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics

from .serializers import UserSerializer
from accounts.models import CustomUser
from rest_framework import status
from rest_framework.permissions import AllowAny ,IsAuthenticated , IsAdminUser
import jwt, datetime




class RegisterView(APIView):
    permission_classes = [AllowAny]

    
    def post(self,request):

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception = True )
        serializer.save()
        
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)
