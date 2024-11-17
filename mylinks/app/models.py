from django.db import models
import uuid
class UserProfile(models.Model):
    id = models.CharField(max_length=100,default=uuid.uuid4(),primary_key=True)
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserLink(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="links")
    link_image = models.ImageField(upload_to="link_images/")
    link_url = models.URLField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Link for {self.user_profile.name}"
