from django.db import models
from uuid import uuid4
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


def user_directory_path(instance, filename):
    try:
        return f'user_{instance.user.username}/{filename}'
    except:
        return f'user_{instance.author.user.username}/{filename}'


class Book(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=50, blank=False, null=False)
    genre = models.CharField(max_length=50, blank=False, null=False)
    subtitle = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    file = models.FileField(upload_to=user_directory_path)
    cover = models.ImageField(upload_to=user_directory_path, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['-title']


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    degree = models.CharField(max_length=50, null=True, blank=True)
    organization = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, default='default.png')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile_detail', args=[str(self.id)])

    @receiver(post_save, sender=get_user_model())
    def create_profile(sender, instance, created, **kwargs):
        if created:
            new_profile = UserProfile.objects.create(user=instance)
            new_profile.save()


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.TextField()
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.comment
