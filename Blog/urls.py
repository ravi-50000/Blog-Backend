from django.urls import path
from Blog.api.posts import ListPostView, PostCreateView, RetrievePostView, PostUpdateView, PostDeleteView, PostLikeView
from Blog.api.comments import CommentCreateView, ListCommentView
from Blog.views import health

urlpatterns = [
    path('health/', health, name='health'),
    path('posts/', ListPostView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/retrieve/<int:post_id>/', RetrievePostView.as_view(), name='post-retrieve'),
    path('posts/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/like/<int:post_id>/', PostLikeView.as_view(), name='post-like'),
    path('comments/', ListCommentView.as_view(), name='comment-list'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
]
