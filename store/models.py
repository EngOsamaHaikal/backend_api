from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel
from django.db import models
from django.urls import reverse
from accounts.models import CustomUser
choices=(
    ("draft", "draft"),
    ("publish", "publish")
)

sizes = (
    ("1Kg","1Kg"), 
    ("2Kg","2Kg"), 
    
)
class Base(models.Model):
    """
    Abstract class with 4 attributes:
            updated_on  DateTimeField
            created_on  DateTimeField
    """

    updated_on = models.DateTimeField(auto_now=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        abstract = True
        ordering = ('created_on',)

# Create your models here.
class Category(Base):
    name = models.CharField(max_length=200,null=True,blank=True,unique=True)
    slug = models.SlugField(max_length=200,null=True,unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name
class Variant(Base):
    name = models.CharField(max_length=200,null=True,blank=True,unique=True)
    slug = models.SlugField(max_length=200,null=True,unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'variant'
        verbose_name_plural = 'variants'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name



class Product(Base):
    category = models.ManyToManyField(Category,blank=True)
    variant = models.ManyToManyField(
        Variant, related_name='variants', blank=True)

    title = models.CharField(max_length=250,null=True)
    slug = models.SlugField(max_length=250,null=True,unique=True)
    description = models.TextField(max_length=500,null=True,blank=True)
    price = models.PositiveIntegerField(default=0,null=True)
    discount = models.IntegerField('Discount percentage', blank=True, default=0)
    stock = models.IntegerField(blank=True, default=0)
    available = models.BooleanField(default=True)
    sizes = models.CharField(max_length=120, choices=sizes, default="1Kg")
    status = models.CharField(max_length=120, choices=choices, default="draft")
    image = models.ImageField(upload_to='media/images/', null=True)

    def __str__(self):

        return self.title



class Cart(TimeStampedModel):
    user = models.OneToOneField(
        CustomUser, related_name="user_cart", on_delete=models.CASCADE
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True
    )


@receiver(post_save, sender=CustomUser)
def create_user_cart(sender, created, instance, *args, **kwargs):
    if created:
        Cart.objects.create(user=instance)


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(
        Cart, related_name="cart_item", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="cart_product", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)


class WishList(Base):
    user = models.OneToOneField(
        CustomUser, related_name="user_wishlist", on_delete=models.CASCADE
    )


class WishListItem(Base):
    
    wishlist = models.ForeignKey(WishList, related_name='wishlist_items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="wishlist_product", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.product.title




class CheckoutDetails(Base):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, related_name='checkout_details', null=True, on_delete=models.SET_NULL)
    name_of_receiver = models.CharField(max_length=100)
    main_address = models.CharField(max_length=200)
    secondary_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=12)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return  'products to ' + self.main_address + ' for ' + self.name_of_receiver
    
class ShippingDetails(Base):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    name_of_receiver = models.CharField(max_length=100)
    main_address = models.CharField(max_length=200)
    secondary_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100)
    delivery_address = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=12)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return  'products to ' + self.main_address + ' for ' + self.name_of_receiver
    


class Review(Base):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_reviews')
    content = models.CharField(max_length=500)
    
    def __str__(self):
        return self.content

