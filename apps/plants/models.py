from django.db import models
from apps.core.models import TimeStampedModel   
from PIL import Image

class Plant(TimeStampedModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='plants')
    scientific_name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='plant_images/', blank=True, null=True)
    care_data = models.JSONField(blank=True, null=True)    

    class Meta:
        db_table = 'plants'

    def __str__(self):
        return self.common_name or self.scientific_name 
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the model first to get the image path
        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((800, 800))  
            img.save(self.image.path)  
            