from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status ,generics ,status
from rest_framework.pagination import LimitOffsetPagination
from .serializers import UserSerializer , ProductSerializer ,CategorySerializer,SubscriptionSerializer , ReviewSerializer ,CartSerializer,CartItemSerializer ,CheckoutDetailsSerializer
from rest_framework.permissions import AllowAny
from store.models import Product, Category,Review ,CartItem ,Cart ,CheckoutDetails 
from django.shortcuts import get_object_or_404
from accounts import utils
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

class GetRoutes(APIView):

    def get(self,request):
        routes = [
            {
                "Method":"POST",
                "ENDPOINT":"http://127.0.0.1:8000/api/send_email/",
            },
            {
                "Method":"POST",
                "ENDPOINT":"http://127.0.0.1:8000/api/register/",
            },

            {
                "Method":"POST",
                "ENDPOINT":"http://127.0.0.1:8000/api/lgoin/",
            },

            {
                "Method":"POST",
                "ENDPOINT":"http://127.0.0.1:8000/api/refresh_token/",
            },
            
            {
                "Method":["GET","POST"],
                "ENDPOINT":"http://127.0.0.1:8000/api/categories/",
            },

            { 
               "Method":["GET","PUT","DELETE"],
                "ENDPOINT":"http://127.0.0.1:8000/api/categories/1",
            },
            { 
               "Method":["GET","POST"],
                "ENDPOINT":"http://127.0.0.1:8000/api/products/"
            },
             {
               "Method":["GET","PUT","DELETE"],
                 "ENDPOINT":"http://127.0.0.1:8000/api/products/1"
             },

             {
                 "Method":["GET","PUT","DELETE"],
                 "ENDPOINT":"http://127.0.0.1:8000/api/products/1/reviews"
            },   
             {
                 "Method":["POST"],
                 "ENDPOINT":"http://127.0.0.1:8000/api/checkout/"
            },   
             {
                 "Method":["GET"],
                 "ENDPOINT":"http://127.0.0.1:8000/api/cart/"
            },   
             {
                 "Method":["GET","PUT","DELETE"],
                 "ENDPOINT":"http://127.0.0.1:8000/api/cart/1/"
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

class GetCategoriesView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination

class GetCategoryView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class GetProductsView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination




class GetProductView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class GetCartView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class GetCartItemView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class GetCheckoutDetailsView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = CheckoutDetails.objects.all()
    serializer_class = CheckoutDetailsSerializer


class GetReviewsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self, **kwargs):
        product = get_object_or_404(Product,id=(self.kwargs['pk']))

        reviews = Review.objects.filter(product = product)

        return reviews
    serializer_class = ReviewSerializer

class SendEmailView(APIView):
    serializer_class = SubscriptionSerializer
    def post(self,request):
        email = request.data
        serializer = SubscriptionSerializer(data=email)
        serializer.is_valid(raise_exception=True)
        serializer.save()
 
        current_site = get_current_site(request).domain
        absurl = 'http://'+current_site
        email_body = 'Hi '+email["email"] + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': email["email"],
                'email_subject': 'Hi this is me'}

        utils.Util.send_email(data)
        return Response(email, status=status.HTTP_201_CREATED)

    pass

"""class GetReviewsView(APIView):
    permission_classes = [AllowAny]

    def get(self,request,pk):
        
        product = Product.objects.get(id=pk)
        reviews = Review.objects.filter(product = product)
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)
    def post(self,request,pk):
        
        review = ReviewSerializer(data = request.data)

        if review.is_valid():
            review.save()
            return Response(review.data, status=status.HTTP_201_CREATED)
        else:
            return Response(review.errors, status=status.HTTP_400_BAD_REQUEST)

 

"""