from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.utils.text import slugify
from django.template.defaultfilters import slugify
from django.urls import reverse
import re
# from projects.models import Status
# Create your models here.

role = (('US', 'User'),
        ('PR', 'Project Manager'),
        ('QA','Quality Analyst'),
        ('AD', 'Admin')
         )

class WorkPlace(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class MyAccountUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError("Users must have a username")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)

class AccountUser(AbstractBaseUser):
    workplace_id = models.ForeignKey(WorkPlace, blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=100, choices=role,
                            blank=True, null=True, default='US')
    slug = models.SlugField(null=False, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = MyAccountUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def full_name(self):
        return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        m = re.search(r'(.+)@', self.email)
        if not self.slug:
            self.slug = slugify(m.group()+"-"+self.username)
        return super().save(*args, **kwargs)
    # def name_path(self):
    #     m = re.search(r'(.+)@(.+)\.(.+)', self.email)
    #     # m.groups()
    #     name = m + "-" + self.username
    #     return name
