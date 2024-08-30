# card_recommendation/models.py

from django.db import models

class Card(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(default='')
    link = models.URLField()
    benefits = models.JSONField(default=list)
    details = models.JSONField(default=list)  # Ensure this field is defined

    def __str__(self):
        return self.name
