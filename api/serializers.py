from django.db.models import fields
from rest_framework import serializers
from accounts.models import CustomUser , NewsSubscription
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from store.models import ShippingDetails,Category,Product,Review,CartItem,Cart,CheckoutDetails,WishListItem,WishList

class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=CustomUser.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('id','username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','title','slug']


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id','product','user','content']



class WishListItemSerializer(serializers.ModelSerializer):


    class Meta:
        model = WishListItem
        fields = ( 'id', 'wishlist', 'product', 'updated_by', 'updated_on', 'created_on', 'created_by' )


class WishListSerializer(serializers.ModelSerializer):


    class Meta:
        model = WishList
        fields = ('id', 'active', 'updated_by', 'updated_on', 'created_on', 'created_by')

class CartItemSerializer(serializers.ModelSerializer):


    class Meta:
        model = CartItem
        fields = ( 'id', 'cart', 'product', 'quantity', 'updated_by', 'updated_on', 'created_on', 'created_by' )


class CartSerializer(serializers.ModelSerializer):


    class Meta:
        model = Cart
        fields = ('id', 'active', 'updated_by', 'updated_on', 'created_on', 'created_by')


class CheckoutDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutDetails
        fields = ('id', 
        'cart', 'name_of_receiver', 
        'main_address', 'secondary_address', 
        'city', 'province', 'postal_code', 
        'phone_number', 'updated_by', 'updated_on',
         'created_on', 'created_by'
        )


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingDetails
        fields = ('id', 
         'name_of_receiver', 
        'main_address', 'delivery_address', 
        'city', 'postal_code', 
        'phone_number', 'updated_by', 'updated_on',
         'created_on', 'created_by'
        )


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsSubscription
        fields = ("email",)
        extra_kwargs = {
            'email': {'required': True},
        }
