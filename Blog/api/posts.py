from Blog.api.base import BaseView
from rest_framework.views import APIView
from Blog.serializers import ListPostViewRequestSerializer, PostCreateViewRequestSerializer, PostUpdateViewRequestSerializer, PostDeleteViewRequestSerializer
from Blog.flows.posts_flow import PostViewFlow
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ListPostView(APIView):
    def post(self,request):
        request_seriliazer = ListPostViewRequestSerializer(data=request.data)
        request_seriliazer.is_valid(raise_exception=True)
        validated_data = request_seriliazer.validated_data
        data, status_code = PostViewFlow().get_all_posts(validated_data)
        return Response(data, status_code)

class PostCreateView(BaseView):
    request_serializer = PostCreateViewRequestSerializer
    
    def execute_post(self, request, validated_data):
        data, status_code = PostViewFlow(request_user=request.user).create_post(validated_data)
        return data, status_code

class RetrievePostView(APIView):
    
    def get(self, request, post_id):
        data, status_code = PostViewFlow().retrieve_post(post_id)
        return Response(data, status_code)

class PostUpdateView(BaseView):
    request_serializer = PostUpdateViewRequestSerializer
    
    def execute_post(self, request, validated_data):
        data, status_code = PostViewFlow(request_user=request.user).update_post(validated_data)
        return data, status_code
    
class PostDeleteView(BaseView):
    request_serializer = PostDeleteViewRequestSerializer
    
    def execute_post(self, request, validated_data):
        data, status_code = PostViewFlow(request_user=request.user).delete_post(validated_data)
        return data, status_code

class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, post_id):
        data, status_code = PostViewFlow(request_user=request.user).like_post_and_get_count(post_id)
        return Response(data, status_code)
