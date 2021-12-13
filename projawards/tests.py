from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post,Rating

# Create your tests here.


class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='mary',email="mary@gmail.com")
        self.post = Post.objects.create(title='Django', photo='img.png', description='first project test',
                                        user=self.user, url="http://django.com")

    def test_instance(self):
        self.assertTrue(isinstance(self.post, Post))

    def test_save_post(self):
        self.post.save_post()
        post = Post.objects.all()
        self.assertTrue(len(post) > 0)        
        
    def test_search_post(self):
        self.post.save()
        post = Post.search_project('Django')
        self.assertTrue(len(post) > 0)

    def test_get_posts(self):
        self.post.save()
        posts = Post.all_posts()
        self.assertTrue(len(posts) > 0)

    def test_delete_post(self):
        self.post.delete_post()
        post = Post.search_project('Django')
        self.assertTrue(len(post) < 1)


class RatingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='mary',email="mary@gmail.com")
        self.post = Post.objects.create(title='Django', photo='img.png', description='first project test',
                                        user=self.user, url="http://django.com")
        self.rating = Rating.objects.create(design=9, usability=10, content=5, user=self.user, post=self.post)

    def test_instance(self):
        self.assertTrue(isinstance(self.rating, Rating))

    def test_save_rating(self):
        self.rating.save_rating()
        rating = Rating.objects.all()
        self.assertTrue(len(rating) > 0)

    def test_get_post_rating(self, id):
        self.rating.save()
        rating = Rating.get_ratings(post_id=id)
        self.assertTrue(len(rating) == 1)
        

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User(username='mary',email="mary@gmail.com", password='password')
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()
        