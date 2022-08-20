from django.db import models
from uuid import uuid4
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
# Create your models here.


class Book(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    author = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='book_files/')
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)

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
    last_name = models.CharField(max_length=50, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    degree = models.CharField(max_length=50, null=True, blank=True)
    organization = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='default.png')
    book = models.ManyToManyField(Book)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile_detail', args=[str(self.id)])

    @receiver(post_save, sender=get_user_model())
    def create_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.CharField(max_length=16)
    comment = models.TextField()

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('book_list')
