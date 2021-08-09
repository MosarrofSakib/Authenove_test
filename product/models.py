from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    
    Available = [
        ( 'In Stock', 'In Stock' ),
        ( 'Out Of Stock', 'Out Of Stock' ),
    ]
    
    CATAGORY = [
        ('Home Decor', 'Home Decor'),
        ('Mathir sets','Mathir sets'),
        ("Men's Collection","Men's Collection"),
    ]
    Sub_CATAGORY = [
        ('Table Mat', 'Table Mat'),
        ('Floor Mat', 'Floor Mat'),
        ('Door Mat', 'Door Mat'),
        ('Basin Set', 'Basin Set'),
        ('Flower Set', 'Flower Set'),
        ('Tea Set', 'Tea Set'),
        ('Diner Set', 'Diner Set'),
        ('Plate set', 'Plate set'),
        ('T-shirts', 'T-shirts'),
        ('Shirts', 'Shirts'),
        ('Pants', 'Pants')
    ]

    catagory = models.CharField( max_length=200, null=True, choices= CATAGORY)
    sub_catagory = models.CharField( max_length=200, null=True, choices= Sub_CATAGORY)
    name = models.CharField( max_length=200, null=True )
    code = models.CharField( max_length=100,null=True, blank=False)
    description = models.TextField( null=True, blank=True )
    price = models.FloatField( null=True, blank=True )
    available = models.CharField( max_length=100, null=True, blank=True, choices=Available )
    product_img = models.ImageField( null=True, blank=True)
    product_img_more = models.ImageField( null=True, blank=True)
    review_total = models.IntegerField( default=0 )
    review_ratio = models.IntegerField( default=0 )
    date_created = models.DateTimeField( auto_now_add=True, null=True, blank=True )
    #id = UUIDField(default=uuid.uuid3, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            img = self.product_img.url
        except:
            img = ''
        return img
    

class Customer(models.Model):

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField( null=True, blank=True )
    date_created = models.DateTimeField( auto_now_add=True, null=True, blank=True )

    def __str__(self):
        return self.name
    
    @property
    def orders(self):
        order_count = self.order_set.all().count()
        return str(order_count)


class Order(models.Model):
    STATUS = [
        ( 'Pending', 'Pending' ),
        ( 'Shipping', 'Shipping' ),
        ( 'Delivered', 'Delivered' ),
    ]

    customer = models.ForeignKey( Customer, null=True, on_delete = models.SET_NULL )
    #product = models.ForeignKey( Product, null=True, on_delete = models.SET_NULL )
    status = models.CharField( max_length=100, null=True, blank=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.customer.name

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    phone_no = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address