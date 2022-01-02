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
        fields = ('id','username', 'password', 'password2', 'email', 'phone_number')
        extra_kwargs = {
            'phone_number': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
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
        fields = ['id','name','slug']


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id','product','user','content']



class WishListItemSerializer(serializers.ModelSerializer):


    class Meta:
        model = WishListItem
        fields = ( 'id', 'wishlist', 'product', 'updated_on', 'created_on' )


class WishListSerializer(serializers.ModelSerializer):


    class Meta:
        model = WishList
        fields = '__all__'

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "title",
            "seller",
            "quantity",
            "price",
            "image",
        )


class CartItemSerializer(serializers.ModelSerializer):
    # product = CartProductSerializer(required=False)
    class Meta:
        model = CartItem
        fields = ["cart", "product", "quantity"]


class CartItemMiniSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(required=False)

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

class CheckoutDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutDetails
        fields = ('id', 
        'cart', 'name_of_receiver', 
        'main_address', 'secondary_address', 
        'city', 'postal_code', 
        'phone_number',  'updated_on',
         'created_on', 
        )


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingDetails
        fields = ('id', 
         'name_of_receiver', 
        'main_address','delivery_address', 
        'city', 'postal_code', 
        'phone_number', 'updated_on',
         'created_on', 
        )


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsSubscription
        fields = ("email",)
        extra_kwargs = {
            'email': {'required': True},
        }
