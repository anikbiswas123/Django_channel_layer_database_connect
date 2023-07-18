from django.db import models

# Create your models here.
class chat(models.Model):
    content=models.CharField(max_length=1000)
    timestamp=models.DateTimeField(auto_now=True)
    group=models.ForeignKey('group',on_delete=models.CASCADE)
    
    
class group(models.Model):
    name=models.CharField(max_length=255)    