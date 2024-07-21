import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from Blog.models import Post, Comment

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def post(user):
    return Post.objects.create(title="Test Post", content="This is a test post.", author=user)

@pytest.fixture
def comment(user, post):
    return Comment.objects.create(content="Test Comment", post=post, author=user)

@pytest.mark.django_db
def test_list_posts(auth_client):
    url = reverse('post-list')
    response = auth_client.post(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_post(auth_client):
    url = reverse('post-create')
    data = {
        'title': 'New Post',
        'content': 'This is a new post',
    }
    response = auth_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Post.objects.count() == 1
    assert Post.objects.get().title == 'New Post'

@pytest.mark.django_db
def test_retrieve_post(auth_client, post):
    url = reverse('post-retrieve', kwargs={'post_id': post.id})
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == post.title

@pytest.mark.django_db
def test_update_post(auth_client, post):
    url = reverse('post-update')
    data = {
        'post_id': post.id,
        'title': 'Updated Post Title',
        'content': 'Updated content',
    }
    response = auth_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    post.refresh_from_db()
    assert post.title == 'Updated Post Title'

@pytest.mark.django_db
def test_delete_post(auth_client, post):
    url = reverse('post-delete')
    data = {'post_id': post.id}
    response = auth_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_like_post(auth_client, post):
    url = reverse('post-like', kwargs={'post_id': post.id})
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    post.refresh_from_db()
    assert post.likes.count() == 1

@pytest.mark.django_db
def test_list_comments(auth_client, post):
    url = reverse('comment-list')
    data = {'post_id': post.id}
    response = auth_client.post(url, data, format='json')
    print(response, response.json())
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_comment(auth_client, post):
    url = reverse('comment-create')
    data = {
        'text': 'New Comment',
        'post_id': post.id
    }
    response = auth_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Comment.objects.count() == 1
    assert Comment.objects.get().text == 'New Comment'
