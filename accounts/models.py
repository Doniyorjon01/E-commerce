from django.core.files.base import ContentFile
from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.contrib.auth.models import BaseUserManager

import base64

USER_TYPES = (
    ('user', 'User'),
    ('admin', 'Admin'),
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Phone Number field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class BaseData(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='%(class)s_creator',
                                   null=True)
    updated_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='%(class)s_renewer',
                                   null=True)

    state = models.SmallIntegerField(default=1)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class User(AbstractUser, BaseData):
    # boss = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name='boss_obj')
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    type = models.CharField(max_length=255, choices=USER_TYPES)

    image_file = models.ImageField(upload_to='media/', blank=True, null=True, default="")
    lang = models.CharField(max_length=10, choices=(
        ('uz', 'Uzbek'), ('ru', 'Rus'), ('en', 'Eng'),
    ), default='uz')
    fcm_token = models.TextField(null=True, blank=True)


    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.fullname if self.fullname else self.email

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if self.image_file and isinstance(self.image_file, str) and len(self.image_file) > 100:
            try:
                img_data = base64.b64decode(str(self.image_file))
                filename = f"{uuid4()}.png"
                self.image_file.save(filename, ContentFile(img_data), save=False)
                self.image_file = filename
            except Exception as e:
                raise ValueError(f"Invalid base64 image format: {e}")

        # ✅ Muhim: DB ga yozib qo‘yish
        super().save(*args, **kwargs)




