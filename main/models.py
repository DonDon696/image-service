from django.db import models

class UploadImage(models.Model):
    original_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image {self.id}, {self.original_name}'

