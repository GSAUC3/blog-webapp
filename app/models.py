from django.db import models
from django.utils import timezone
from PIL import Image
from django.contrib.auth.models import User 
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
#     cascade means if user if deleted then delete the profile, but if the profile is deleted 
# then do not delete user 
    image = models.ImageField(default='default.png',upload_to='profile_pics')

    def __str__(self):
        return str(self.user.username) + ' Profile'
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.image.path)
        if img.height > 150 or img.width >150:
            output_size = (150,150)
            img.thumbnail(output_size)
            img.save(self.image.path)