from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("An email address must be provided")
        if not username:
            raise ValueError("A username address must be provided")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, username, password=None):
        if not email:
            raise ValueError("An email address must be provided")
        if not username:
            raise ValueError("A username address must be provided")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.password = make_password(password)
        user.save(using=self._db)
        return user


def get_profile_image_path(self, filename):
    return f'profile_images/{self.pk}/{"defa.png"}'

def get_default_profile_image():
    return 'default_image/default.png'
    
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_path, 
                                    null=True, blank=True, default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)
    capacity = models.PositiveIntegerField(default=0)
    workload = models.PositiveIntegerField(default=0)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'date_of_birth']
    
    def __str__(self):
        return self.username
        
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]
        
    def has_perm(self, perm, obj=None):
        return self.is_admin
        
    def has_module_perms(self, app_label):
        return True
        