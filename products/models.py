from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import BaseData, User


class Category(BaseData):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, blank=True, null=True)  # emoji yoki icon
    color = models.CharField(max_length=7, default='#3B82F6')  # hex color

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(BaseData):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    attributes = models.JSONField(default=dict)
    colors = models.JSONField(default=list, blank=True)  # list sifatida saqlash
    sizes = models.JSONField(default=list, blank=True)   # o'lchamlar uchun
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    expire_time = models.DateTimeField(null=True, blank=True)  # dori-darmonlar uchun
    count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_products', blank=True)
    # is_featured = models.BooleanField(default=False)  # asosiy sahifada ko'rsatish uchun
    # discount_percentage = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

    def __str__(self):
        return self.name

    # @property
    # def discounted_price(self):
    #     if self.discount_percentage > 0:
    #         return self.price * (1 - self.discount_percentage / 100)
    #     return self.price



class Review(BaseData):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_reviews', blank=True)

    def __str__(self):
        return f"{self.user.fullname} - {self.product.name}"

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def dislike_count(self):
        return self.dislikes.count()

    class Meta:
        unique_together = ('product', 'user')

