from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey("login.User", on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey("login.User", on_delete=models.CASCADE, related_name="receiver")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message