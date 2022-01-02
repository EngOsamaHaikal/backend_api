from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status ,generics ,status
from rest_framework.pagination import LimitOffsetPagination
from .serializers import UserSerializer ,ShippingSerializer,WishListSerializer,WishListItemSerializer, ProductSerializer ,CategorySerializer,SubscriptionSerializer , ReviewSerializer ,CheckoutDetailsSerializer,CartItemSerializer,CartItemUpdateSerializer,CartItemMiniSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from store.models import Product, Category,Review ,CartItem ,Cart ,CheckoutDetails, ShippingDetails, WishList ,WishListItem
from django.shortcuts import get_object_or_404
from accounts import utils
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth import login,logout , authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from django.shortcuts import get_object_or_404
from .serializers import CartItemSerializer, CartItemUpdateSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable, ValidationError, PermissionDenied
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from django.utils.translation import ugettext_lazy as _
class GetRoutes(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        routes = [
            {
                "Method":"POST",
                "ENDPOINT":"http://127.0.0.1:8000/api/send_email/",
            },
            {
                "Method":"POST",
                "ENDPOINT":"http://127.0.0.1:8000/api/shipping/1",
            },
            {
                "Method":"POST",
                "ENDPOINT":"http://127.0.0.1:8000/api/register/",
            },

            {
                "Method":"POST",
                "ENDPOINT":"http://127.0.0.1:8000/api/login/",
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

    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

    @method_decorator(cache_page(60 * 60 * 24))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GetWishListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer

class GetWishListItemView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = WishListItem.objects.all()
    serializer_class = WishListItemSerializer


class GetCartView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        try:
            user = self.request.user
            queryset = CartItem.objects.filter(cart__user=user)
            return queryset
        except Exception as e:
            error = {"Error": "Login required"}
            raise NotAcceptable(
                error)


    def create(self, request, *args, **kwargs):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        product = get_object_or_404(Product, pk=request.data["product"])
        current_item = CartItem.objects.filter(cart=cart, product=product)

        if user == product.user:
            raise PermissionDenied("This Is Your Product")

        if current_item.count() > 0:
            raise NotAcceptable(
                "You already have this item in your shopping cart")

        try:
            quantity = int(request.data["quantity"])
        except Exception as e:
            raise ValidationError("Please Enter Your Quantity")

        if quantity > product.stock:
            raise NotAcceptable("You order quantity more than the seller have")

        cart_item = CartItem(cart=cart, product=product, quantity=quantity)
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        total = float(product.price) * float(quantity)
        cart.total = total
        cart.save()
  

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetCartItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    # method_serializer_classes = {
    #     ('PUT',): CartItemUpdateSerializer
    # }
    queryset = CartItem.objects.all()

    def retrieve(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        print(request.data)
        product = get_object_or_404(Product, pk=request.data["product"])

        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")

        try:
            quantity = int(request.data["quantity"])
        except Exception as e:
            raise ValidationError("Please, input vaild quantity")

        if quantity > product.quantity:
            raise NotAcceptable(
                "Your order quantity more than the seller have")

        serializer = CartItemUpdateSerializer(cart_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")
        cart_item.delete()
 
        return Response(
            {"detail": _("your item has been deleted.")},
            status=status.HTTP_204_NO_CONTENT,
        )
    permission_classes = [AllowAny]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class GetShippingDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = ShippingDetails.objects.all()
    serializer_class = ShippingSerializer


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
    permission_classes = [AllowAny]

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
