from django.db import models

# Create your models here.
class Friends(models.Model):
    user = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey('login.User', on_delete=models.CASCADE, related_name='friend')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'friend']
