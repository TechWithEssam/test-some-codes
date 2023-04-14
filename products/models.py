from django.db import models
from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
# Create your models here.

def slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str

class Category(models.Model) :
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def __str__(self) :
        return self.name
    
    def save(self, *args, **kwargs) :
        if not self.slug :
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
class Brand(models.Model) :
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    
    def __str__(self) :
        return self.name
    def save(self, *args, **kwargs) :
        if not self.slug :
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    


class Product(models.Model) :
    salesman            = models.ForeignKey(User, on_delete=models.CASCADE)
    name                = models.CharField(max_length=100)
    slug                = models.SlugField(blank=True, null=True, unique=True)
    price               = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    category_sex        = models.CharField(max_length=10, blank=True)
    category            = models.ForeignKey(Category, blank=True,null=True, on_delete=models.SET_NULL)
    brand               = models.ForeignKey(Brand, blank=True,null=True, on_delete=models.SET_NULL)
    discound            = models.IntegerField(blank=True, null=True,
                                               validators=[MinValueValidator(0),
                                                            MaxValueValidator(100)])
    description         = models.TextField()
    timestamp           = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)


    @property
    def new_price_after_discound(self) :
        if self.discound  :
            new_price = self.price - self.price * self.discound / 100
        else :
            new_price = self.price
        return new_price

    def __str__(self) :
        return f"{str(self.name)} {self.new_price_after_discound}"
    
    def manager_url(self) :
        return reverse("products:manage", kwargs={"slug":self.slug})
    
    def upload_image_url(self) :
        return reverse("products:upload_image",kwargs={"pk":self.pk})
    
    def detail_product_url(self) :
        return reverse("products:detail_product", kwargs={"slug":self.slug})
    
    @property
    def all_image_related(self) :
        return self.images_set.all()
    @property
    def first_image(self) :
        try :
            image = self.all_image_related.first()
        except :
            image = None
        return image
        
    @property
    def get_productpttachment(self) :
        return self.productattachment_set.all()

def get_image_filename(instance, filename):
    title = instance.product.name
    slug = slugify(title)
    return "product_images/%s-%s" % (slug, filename)  

class Images(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')
    def __str__(self) :
        return f"iamge for product name {self.product.name} ID '{self.product.id}'"

    def delete_image_url(self) :
        return reverse("products:delete_image", kwargs={"pk": self.pk})
    
    


class ProductAttachment(models.Model):
    product             = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    size_number         = models.CharField(blank=True, null=True, max_length=100)
    size                = models.CharField(blank=True, null=True, max_length=100)
    color               = models.CharField(max_length=100, blank=True, null=True)
    inventory_quantity  = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_available        = models.BooleanField(default=False)
    active              = models.BooleanField(default=True)
    timestamp           = models.DateTimeField(auto_now_add=True)
    updated             = models.DateTimeField(auto_now=True)
    def __str__(self) :
        return f"iamge for product name {self.product.name} ID '{self.product.id}'"
    
    