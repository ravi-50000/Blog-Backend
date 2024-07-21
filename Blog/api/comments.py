from Blog.api.base import BaseView
from rest_framework.views import APIView
from Blog.serializers import ListCommentViewRequestSerializer, CommentCreateViewRequestSerializer
from Blog.flows.comments_flow import CommentViewFlow
from rest_framework.response import Response

class ListCommentView(APIView):
    """
    List comments for a specific post.

    POST /comments/
    Request Body:
    - post_id

    Response:
    - post_id
    - comments: List of comments
    """
    def post(self,request):
        request_seriliazer = ListCommentViewRequestSerializer(data=request.data)
        request_seriliazer.is_valid(raise_exception=True)
        validated_data = request_seriliazer.validated_data
        data, status_code = CommentViewFlow().get_post_comments(validated_data)
        return Response(data, status_code)
    
class CommentCreateView(BaseView):
    """
    Create a new comment on a post.

    POST /comments/create/
    Request Body:
    - post_id
    - text

    Response:
    - id
    - text
    - author
    - created
    - modified
    """
    request_serializer = CommentCreateViewRequestSerializer
    
    def execute_post(self, request, validated_data):
        data, status_code = CommentViewFlow(request_user=request.user).create_comment(validated_data)
        return data, status_code
