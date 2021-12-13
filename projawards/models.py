from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phone_field import PhoneField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField(max_length=400, blank=True)
    name = models.CharField(blank=True, max_length=120)
    profile_pic = models.ImageField(upload_to='images/',default='v1639327874/images/default_drurzc.jpg')
    phone_number = PhoneField(max_length=15, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=300)
    url = models.URLField(max_length=400)
    photo = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    upload_date = models.DateTimeField(auto_now_add=True, blank=True)
    technologies_used = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.title}'

    def delete_post(self):
        self.delete()

    @classmethod
    def search_project(cls, title):
        return cls.objects.filter(title__icontains=title).all()

    @classmethod
    def all_posts(cls):
        return cls.objects.all()

    def save_post(self):
        self.save()

class Rating(models.Model):
    rating = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    
    usability = models.IntegerField(choices=rating, blank=True, default='1')
    content = models.IntegerField(choices=rating, blank=True,default='1')
    design = models.IntegerField(choices=rating, default='1', blank=True,)
    score = models.FloatField(default=0, blank=True)
    design_average = models.FloatField(default=0, blank=True)
    usability_average = models.FloatField(default=0, blank=True)
    content_average = models.FloatField(default=0, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='rater')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings', null=True)

    def save_rating(self):
        self.save()

    @classmethod
    def get_ratings(cls, id):
        ratings = Rating.objects.filter(post_id=id).all()
        return ratings

    def __str__(self):
        return f'{self.post} Rating'