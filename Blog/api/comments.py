from Blog.api.base import BaseView
from rest_framework.views import APIView
from Blog.serializers import ListCommentViewRequestSerializer, CommentCreateViewRequestSerializer
from Blog.flows.comments_flow import CommentViewFlow
from rest_framework.response import Response

class ListCommentView(APIView):
    def post(self,request):
        request_seriliazer = ListCommentViewRequestSerializer(data=request.data)
        request_seriliazer.is_valid(raise_exception=True)
        validated_data = request_seriliazer.validated_data
        data, status_code = CommentViewFlow().get_post_comments(validated_data)
        return Response(data, status_code)
    
class CommentCreateView(BaseView):
    request_serializer = CommentCreateViewRequestSerializer
    
    def execute_post(self, request, validated_data):
        data, status_code = CommentViewFlow(request_user=request.user).create_comment(validated_data)
        return data, status_code
