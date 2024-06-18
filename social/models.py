from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    cover_picture = models.ImageField(upload_to='covers/', null=True, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField(User, related_name='tagged_photos', blank=True)
    location = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Photo {self.id} by {self.owner.username}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments', null=True)  # Allow null temporarily
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on Photo {self.photo.id}'

class Friendship(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_created')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_received')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user.username} -> {self.to_user.username}'

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    tags = models.ManyToManyField(User, related_name='tagged_posts', blank=True)
    location = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post {self.id} by {self.user.username}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} likes Post {self.post.id}'

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tagger')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='taggers')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} tagged in Post {self.post.id}'

class Feed(models.Model):
    CONTENT_TYPES = (
        ('post', 'Post'),
        ('photo', 'Photo'),
        ('comment', 'Comment'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feeds')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    object_id = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feed item {self.id} for {self.user.username}'

class Mention(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentions')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} mentioned at {self.timestamp}'
