from rest_framework import serializers

class ListPostViewRequestSerializer(serializers.Serializer):
    page_number = serializers.IntegerField(default=1)

class PostResponseSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField(max_length=1000)
    created = serializers.DateTimeField()
    author = serializers.CharField(source='author.username')
    modified = serializers.DateTimeField()

class PostCreateViewRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField(max_length=1000)

class PostUpdateViewRequestSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    title = serializers.CharField(max_length=200, required=False)
    content = serializers.CharField(max_length=1000, required=False)

class PostDeleteViewRequestSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    
class PostLikeViewRequestSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()

class ListCommentViewRequestSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    
class CommentResponseSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)
    created = serializers.DateTimeField()

class CommentCreateViewRequestSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000)
    post_id = serializers.IntegerField()
