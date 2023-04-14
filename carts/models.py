from django.db import models
from products.models import ProductAttachment, Product
from django.conf import settings
# Create your models here.


User = settings.AUTH_USER_MODEL

class OrderManager(models.Manager):
    def new_or_get(self, request):
        order_id = request.session.get("order_id", None)
        qs = self.get_queryset().filter(id=order_id)
        if qs.count() == 1:
            new_obj = False
            order_obj = qs.first()
            if request.user.is_authenticated and order_obj.user is None:
                order_obj.user = request.user
                order_obj.save()
        else:
            order_obj = Order.objects.new(user=request.user)
            new_obj = True
            request.session['order_id'] = order_obj.id
        return order_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Order(models.Model) :
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = OrderManager()

    def __str__(self) :
        if self.user :
            return f"{str(self.user)} {self.pk}"
        return f"{self.pk}"
    

class Cart(models.Model) :
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    order           = models.ForeignKey(Order, on_delete=models.CASCADE)
    color           = models.ForeignKey(ProductAttachment, on_delete=models.SET_NULL, blank=True, null=True, related_name="product_color")
    size_number     = models.ForeignKey(ProductAttachment, on_delete=models.SET_NULL, blank=True, null=True, related_name="product_size_number")
    size            = models.ForeignKey(ProductAttachment, on_delete=models.SET_NULL, blank=True, null=True, related_name="product_size")
    quantity        = models.PositiveIntegerField(default=0)
    total_price     = models.DecimalField(max_digits=20,decimal_places=2, blank=True, null=True)
    transection_id  = models.CharField(blank=True, null=True, max_length=25)
    updated         = models.DateTimeField(auto_now_add=True)
    created         = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return self.product.name


