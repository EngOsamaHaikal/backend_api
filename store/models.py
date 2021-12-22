from django.db import models

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
    title = models.CharField(max_length=200,null=True,blank=True)
    slug = models.SlugField(max_length=200,null=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title

class Product(models.Model):
    category = models.ManyToManyField(Category,blank=True)
    title = models.CharField(max_length=250,null=True)
    slug = models.SlugField(max_length=250,null=True,unique=True)
    description = models.TextField(max_length=500,null=True,blank=True)
    price = models.PositiveIntegerField(default=0,null=True)
    discount = models.IntegerField('Discount percentage', blank=True, default=0)
 
    sizes = models.CharField(max_length=120, choices=sizes, default="1Kg")
    quantity = models.PositiveIntegerField(default=0,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=120, choices=choices, default="draft")

    def __str__(self):

        return self.title

class Image(models.Model):
    model = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/images/',null=True)

