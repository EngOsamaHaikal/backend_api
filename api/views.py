from django.db.models.query import QuerySet
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status ,generics ,status
from rest_framework.pagination import PageNumberPagination , LimitOffsetPagination
from .serializers import UserSerializer , ProductSerializer ,CategorySerializer , ReviewSerializer
from accounts.models import CustomUser
from rest_framework.permissions import AllowAny ,IsAuthenticated , IsAdminUser
import jwt, datetime
from store.models import Product, Category,Review


class GetRoutes(APIView):

    def get(self,re):
        routes = [
            {
                "Method":"POST",
                "ENDPOINT":"/api/register/",
            },

            {
                "Method":"POST",
                "ENDPOINT":"/api/login/",
            },

            {
                "Method":"POST",
                "ENDPOINT":"/api/refresh_token/",
            },
            
            {
                "Method":"GET",
                "ENDPOINT":"/api/categories/",
            },

           { 
               "Method":"GET",
                "ENDPOINT":"/api/categories/<str:slug>"}
            ,
            { 
                "Method":"GET",
                "ENDPOINT":"/api/products/?limit= & offeset= "
            },
             {
                 "Method":"GET",
                 "ENDPOINT":"/api/products/<str:pk>"
             },

             {
                 "Method":"GET",
                 "ENDPOINT":"/api/products/<str:pk>/reviews"
            },     
        ]

        return Response(routes)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    
    def post(self,request):

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception = True )
        serializer.save()
        
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class GetCategoriesView(APIView):
    permission_classes = [AllowAny]

    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
class GetCategoryView(APIView):
    permission_classes = [AllowAny]

    def get(self,request,slug):
        categories = Category.objects.filter(slug=slug)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)



class GetProductsView(generics.ListAPIView):
    permission_classes = [AllowAny]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination




class GetProductView(APIView):
    permission_classes = [AllowAny]

    def get(self,request,pk):
        
        product = Product.objects.filter(id=pk)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)


class GetReviewsView(APIView):
    permission_classes = [AllowAny]

    def get(self,request,pk):
        
        product = Product.objects.get(id=pk)
        reviews = Review.objects.filter(product = product)
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)

 