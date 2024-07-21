from Blog.api.base import BaseView
from rest_framework.views import APIView
from Blog.serializers import ListPostViewRequestSerializer, PostCreateViewRequestSerializer, PostUpdateViewRequestSerializer, PostDeleteViewRequestSerializer
from Blog.flows.posts_flow import PostViewFlow
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ListPostView(APIView):
    """
    List all posts with pagination.

    POST /posts/
    Request Body:
    - page_number (optional)

    Response:
    - page_context
    - result: List of posts
    """
    def post(self,request):
        request_seriliazer = ListPostViewRequestSerializer(data=request.data)
        request_seriliazer.is_valid(raise_exception=True)
        validated_data = request_seriliazer.validated_data
        data, status_code = PostViewFlow().get_all_posts(validated_data)
        return Response(data, status_code)

class PostCreateView(BaseView):
    """
    Create a new post.

    POST /posts/create/
    Request Body:
    - title
    - content

    Response:
    - id
    - title
    - content
    - author
    - created(published_date)
    - modified
    """
    request_serializer = PostCreateViewRequestSerializer
    
    def execute_post(self, request, validated_data):
        data, status_code = PostViewFlow(request_user=request.user).create_post(validated_data)
        return data, status_code

class RetrievePostView(APIView):
    """
    Retrieve a specific post by ID.

    GET /posts/retrieve/{post_id}/
    Request Parameters:
    - post_id

    Response:
    - id
    - title
    - content
    - author
    - created(published_date)
    - modified
    """
    def get(self, request, post_id):
        data, status_code = PostViewFlow().retrieve_post(post_id)
        return Response(data, status_code)

class PostUpdateView(BaseView):
    """
    Update an existing post.

    PUT /posts/update/{post_id}/
    Request Body:
    - title (optional)
    - content (optional)

    Response:
    - id
    - title
    - content
    - author
    - created(published_date)
    - modified
    """
    request_serializer = PostUpdateViewRequestSerializer
    
    def execute_post(self, request, validated_data):
        data, status_code = PostViewFlow(request_user=request.user).update_post(validated_data)
        return data, status_code
    
class PostDeleteView(BaseView):
    """
    Delete a specific post by ID.

    DELETE /posts/delete/{post_id}/
    Request Body:
    - post_id

    Response:
    - Message: 'Post Deleted Successfully'
    """
    request_serializer = PostDeleteViewRequestSerializer
    
    def execute_post(self, request, validated_data):
        data, status_code = PostViewFlow(request_user=request.user).delete_post(validated_data)
        return data, status_code

class PostLikeView(APIView):
    """
    Like a post and get the like count.

    GET /posts/like/{post_id}/
    Request Parameters:
    - post_id

    Response:
    - Message: 'Post Liked Successfully'
    - LikeCount: constant(1,2,..)
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, post_id):
        data, status_code = PostViewFlow(request_user=request.user).like_post_and_get_count(post_id)
        return Response(data, status_code)
