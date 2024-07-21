import pytest
from django.contrib.auth import get_user_model
from Blog.models import Post, Comment

User = get_user_model()

@pytest.mark.django_db
def test_post_creation():
    user = User.objects.create_user(username="testuser", password="password")
    post = Post.objects.create(title="Test Post", content="This is a test post.", author=user)

    assert post.title == "Test Post"
    assert post.content == "This is a test post."
    assert post.author == user

@pytest.mark.django_db
def test_post_str_method():
    user = User.objects.create_user(username="testuser", password="password")
    post = Post.objects.create(title="Test Post", content="This is a test post.", author=user)

    assert str(post) == f'{user}-{post.title}'

@pytest.mark.django_db
def test_comment_creation():
    user = User.objects.create_user(username="testuser", password="password")
    post = Post.objects.create(title="Test Post", content="This is a test post.", author=user)
    comment = Comment.objects.create(post=post, author=user, text="This is a test comment.")

    assert comment.post == post
    assert comment.author == user
    assert comment.text == "This is a test comment."

@pytest.mark.django_db
def test_comment_str_method():
    user = User.objects.create_user(username="testuser", password="password")
    post = Post.objects.create(title="Test Post", content="This is a test post.", author=user)
    comment = Comment.objects.create(post=post, author=user, text="This is a test comment.")

    assert str(comment) == f'Comment by {user} on {post}'
