from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, default="")
    role = models.CharField(max_length=50)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True, default="")
    level = models.IntegerField(default=0)
    coin = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    opening_hours = models.CharField(max_length=100)
    user = models.ForeignKey('User', on_delete=models.CASCADE,default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    img = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    rate = models.IntegerField()
    type = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    price = models.IntegerField()
    ship = models.IntegerField()
    discount = models.IntegerField(default= 0)
    total_amount = models.IntegerField()
    payment = models.CharField(max_length=50, default='Tiền mặt')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.name}"

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    item = models.ForeignKey('Dish', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    options = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Item {self.item.name} in Order #{self.order.id}"

class Review(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE,  default='')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, default='')
    rating = models.IntegerField()
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.item.name} by {self.user.name}"

class Cart(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item = models.ForeignKey('Dish', on_delete=models.CASCADE, default= "")
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, default='')
    quantity = models.PositiveIntegerField(default= 1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.name} with {self.quantity} {self.item.name}"
