from django.db import models
import random
# Create your models here.
class Cart(models.Model):
    noItem = models.IntegerField()
    user = models.CharField(max_length=20)
    
    @property
    def gender(self):
        return random.choice(['male','female'])