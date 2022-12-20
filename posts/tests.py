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

    def test_logged_out_user_cant_create_post(self):
        response = self.client.post(
            '/posts/',
            {'title': 'test title'}
        )
        count = Post.objects.count()
        self.assertEqual(
            count, 0
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )


class PostDetailViewTests(APITestCase):
    def setUp(self):
        test_droid_1 = User.objects.create_user(
            username='test_droid_1',
            password='test_password'
        )
        test_droid_2 = User.objects.create_user(
            username='test_droid_2',
            password='test_password'
        )
        Post.objects.create(
            owner=test_droid_1,
            title='test title',
            content='test droid 1 content'
        )
        Post.objects.create(
            owner=test_droid_2,
            title='another test title',
            content='test droid 2 content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get(
            '/posts/1/'
        )
        self.assertEqual(
            response.data['title'],
            'test title'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get(
            '/posts/10/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_user_can_update_own_post(self):
        self.client.login(
            username='test_droid_1',
            password='test_password'
        )
        response = self.client.put(
            '/posts/1/',
            {'title': 'a new title'}
        )
        # Locates newly created test object
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(
            post.title,
            'a new title'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
