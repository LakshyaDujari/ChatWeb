from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db.models.signals import post_save

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField(
    Group,
    verbose_name='groups',
    blank=True,
    help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    related_name="custom_user_set",
    related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",
        related_query_name="user",
    )


    def __str__(self):
        return self.username

class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    image = models.ImageField(default='default.jpg', upload_to='user_image', null=True, blank=True)
    verified = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.full_name

class Session(models.Model):
    sessionId = models.CharField(max_length=255, unique=True)
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField()
    
    def __str__(self):
        return self.sessionId

    def save(self, *args, **kwargs):
        if self.isActive:
            Session.objects.filter(user=self.user, isActive=True).update(isActive=False)
        super(Session, self).save(*args, **kwargs)

def create_user_profile(sender,instance,created,**kwargs):
    if created:
        UserDetail.objects.create(user=instance)
        
def save_user_profile(sender,instance,**kwargs):
    instance.userdetail.save()
    
class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.otp

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)