from django.db import models
from django.contrib.auth.models import User
from messaging.models import MessageGroup
# Create your models here.
class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    is_active = models.BooleanField(default=False)
    msg_group = models.ForeignKey( MessageGroup, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'friend']
        
    def __str__(self):
        return self.user.username + ' - ' + self.friend.username
