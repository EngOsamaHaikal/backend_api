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
            updated_by  CHARFIELD(100)
            updated_on  DateField
            created_on  DateField
            created_by  CHARFIELD(100)
    """

    updated_by = models.CharField(max_length=100,null=True)
    updated_on = models.DateTimeField(auto_now=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.CharField(max_length=100,null=True)
    class Meta:
        abstract = True
        ordering = ('created_on',)

# Create your models here.
class Category(Base):
    title = models.CharField(max_length=200,null=True,blank=True,unique=True)
    slug = models.SlugField(max_length=200,null=True,unique=True)
    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.title

class Product(Base):
    category = models.ManyToManyField(Category,blank=True)
    title = models.CharField(max_length=250,null=True)
    slug = models.SlugField(max_length=250,null=True,unique=True)
    description = models.TextField(max_length=500,null=True,blank=True)
    price = models.PositiveIntegerField(default=0,null=True)
    discount = models.IntegerField('Discount percentage', blank=True, default=0)
    stock = models.IntegerField(blank=True, default=0)
    available = models.BooleanField(default=True)
    sizes = models.CharField(max_length=120, choices=sizes, default="1Kg")
    status = models.CharField(max_length=120, choices=choices, default="draft")
    image = models.ImageField(upload_to='media/images/',null=True)
    def __str__(self):

        return self.title

class Cart(Base):
    user = models.ForeignKey(CustomUser,null=True,blank=True, default=None, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)


    def get_items(self):
        return self.cart_items.prefetch_related('product').all()

    @classmethod
    def delete_unactive_carts(cls):
    # deletes all non-active cart instances
        cls.objects.filter(active=False).delete()

    @classmethod
    def delete_all_carts(cls):
        cls.objects.all().delete()



class CartItem(Base):
    
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.title + ' cart item from cart object ' + str(self.cart.id)

    def find_total_cost(self):
        tax = 5
        self.total_cost = self.quantity * self.product.current_price * tax
        return self.total_cost

    def update_quantity(self, quantity):
        self.update(quantity=quantity)



class CheckoutDetails(Base):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, related_name='checkout_details', null=True, on_delete=models.SET_NULL)
    name_of_receiver = models.CharField(max_length=100)
    main_address = models.CharField(max_length=200)
    secondary_address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=20)
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

