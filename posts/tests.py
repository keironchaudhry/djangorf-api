from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='test_user',
            password='test_password'
        )

    def test_can_list_posts(self):
        test_user = User.objects.get(
            username='test_user'
        )
        Post.objects.create(
            owner=test_user,
            title='test title'
        )
        response = self.client.get(
            '/posts/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(
            username='test_user',
            password='test_password'
        )
        response = self.client.post(
            '/posts/',
            {'title': 'test title'}
        )
        count = Post.objects.count()
        self.assertEqual(
            count, 1
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
