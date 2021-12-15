from django.test import TestCase
from .models import *
# Create your tests here.




class ImageTestCase(TestCase):
    def setUp(self):
  
        user = User.objects.create(
            username='test_user',
            first_name='dav',
            
        )
        Image.objects.create(
            image_name='test_image',
            image='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
            image_caption='test image',
            profile_id=user.id,
            user_id=user.id
        )

    def test_image_name(self):
        image = Image.objects.get(image_name='test_image')
        self.assertEqual(image.image_name, 'test_image')



class ProfileTestCase(TestCase):
    def setUp(self):
        # create a user
        user = User.objects.create(
            username='test_user',
            first_name='dav',
            
        )
        Profile.objects.create(
            bio='test bio',
            profile_photo='static/img/homepage.jpg',
            user_id=user.id
        )

    def test_bio(self):
        profile = Profile.objects.get(bio='test bio')
        self.assertEqual(profile.bio, 'test bio')



class LikesTestCase(TestCase):
    def setUp(self):
        # create a user
        user = User.objects.create(
            username='test_user',
            first_name='sdsa',
            
        )
     
        Profile.objects.create(
            bio='test bio',
            profile_photo='static/img/homepage.jpg',
            user_id=user.id
        )
   
        image = Image.objects.create(
            image_caption='test post',
            image='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
            profile_id=user.id,
            user_id=user.id
        )
       
       
    def test_image_id(self):
       
        user = User.objects.create(
            username='newuser',
            first_name='dddd',
            
        )
       
        image = Image.objects.create(
            image_caption='test post',
            image='https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
            profile_id=user.id,
            user_id=user.id
        )
        # likes = Likes.objects.get(image_id=image.id)
        # self.assertEqual(likes.image_id, 1)
