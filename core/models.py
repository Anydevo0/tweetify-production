from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    img = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username 
    
# Commit msg of models creations

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, null=True)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers'
    )

    def follow(self, profile):
        if profile != self:
            self.following.add(profile)

    def unfollow(self, profile):
        if profile != self:
            self.following.remove(profile)

    def is_following(self, profile):
        return self.following.filter(id=profile.id).exists()

    def is_followed_by(self, profile):
        return self.followers.filter(id=profile.id).exists()

    def __str__(self):
        return self.user.username