from django.db import models
from django.utils import timezone

# Create your models here.

class Genere(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.title
    



class Author(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name
    


class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    description = models.TextField()
    nu_of_pages = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='authors')
    genere = models.ForeignKey(Genere, on_delete=models.CASCADE, related_name='category')
    cover_image = models.ImageField(upload_to='books/cover')
    edition = models.CharField(default='latest edition')
    isbn = models.CharField(max_length=200)

    def __str__(self):
        return self.title + " : " + self.author.name
    
    
class Address(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=200)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return self.name + " : " + self.user.username
    
    
    
class Coupopn(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.FloatField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_valid_now(self):
        return self.active
    
class Payment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='payments')
    amount = models.FloatField()
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.transaction_id
    
class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='orders')
    total_price = models.FloatField()
    order_date = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    coupon = models.ForeignKey(Coupopn, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def get_subtotal(self):
        subtotal = 0
        items = self.items.select_related('book').all()
        for item in items:
            unit_price = item.book.discount_price if item.book.discount_price is not None else item.book.price
            subtotal += unit_price * item.quantity
        return subtotal

    def get_delivery_charge(self):
        subtotal = self.get_subtotal()
        if subtotal > 0 and subtotal < 500:
            return 49
        return 0

    def get_coupon_discount(self):
        subtotal = self.get_subtotal()
        if self.coupon and self.coupon.active:
            return min(self.coupon.discount_amount, subtotal)
        return 0

    def get_tax_amount(self):
        subtotal = self.get_subtotal()
        coupon_discount = self.get_coupon_discount()
        delivery_charge = self.get_delivery_charge()
        taxable_amount = max(subtotal - coupon_discount, 0) + delivery_charge
        return taxable_amount * 0.18

    def get_final_total(self):
        subtotal = self.get_subtotal()
        coupon_discount = self.get_coupon_discount()
        delivery_charge = self.get_delivery_charge()
        tax_amount = self.get_tax_amount()
        return max(subtotal - coupon_discount, 0) + delivery_charge + tax_amount
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.book.title} in Order {self.order.id}"