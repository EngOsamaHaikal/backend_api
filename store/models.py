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
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True,unique=True)
    slug = models.SlugField(max_length=200,null=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ManyToManyField(Category,blank=True)
    title = models.CharField(max_length=250,null=True)
    slug = models.SlugField(max_length=250,null=True,unique=True)
    description = models.TextField(max_length=500,null=True,blank=True)
    price = models.PositiveIntegerField(default=0,null=True)
    discount = models.IntegerField('Discount percentage', blank=True, default=0)
    stock = models.IntegerField(blank=True, default=0)
    available = models.BooleanField(default=True)
    sizes = models.CharField(max_length=120, choices=sizes, default="1Kg")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=120, choices=choices, default="draft")
    image = models.ImageField(upload_to='media/images/',null=True)
    def __str__(self):

        return self.title


class Cart(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='user_reviews')
    content = models.CharField(max_length=500)

    def __str__(self):
        return self.content