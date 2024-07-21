import logging
from rest_framework import status
from Blog.models import Comment, Post
from Blog.serializers import CommentResponseSerializer
from django.shortcuts import get_object_or_404
from django.conf import settings
logger = logging.getLogger(settings.DEBUG_LOGGER_DJANGO)

class CommentViewFlow:
    def __init__(self, **kwargs):
        self.user = kwargs.get('request_user')
        
    def get_post_comments(self, validated_data):
        try:
            post_id = validated_data.get('post_id')
            logger.info(f'Fetching comments for post_id: {post_id}')
            post = get_object_or_404(Post, id=post_id, is_deleted=False)
            all_comments = post.comments.select_related('author').all()
            result_list = []
            for comment in all_comments:
                data = CommentResponseSerializer(comment).data
                data['id'] = str(comment.id)
                data['author'] = str(comment.author)
                result_list.append(data)
            result = {
                "result": {
                    "post_id": post_id,
                    "comments": result_list
                }
            }
            logger.info(f'Fetched {len(result_list)} comments for post_id: {post_id}')
            return result, status.HTTP_200_OK
        
        except Exception as e:
            logger.exception(f'Error fetching comments for post_id: {post_id} - {e}')
            return {'Error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
        
    def create_comment(self, validated_data):
        try:
            post_id = validated_data.get('post_id')
            logger.info(f'Creating comment for post_id: {post_id} by user: {self.user}')
            text = validated_data.get('text')
            post = get_object_or_404(Post, id=post_id, is_deleted=False)
            author = self.user
            comment = Comment.objects.create(
                post=post,
                text=text,
                author=author,
            )
            result = CommentResponseSerializer(comment).data
            result['id'] = str(comment.id)
            logger.info(f'Created comment with id: {comment.id} for post_id: {post_id}')
            return result, status.HTTP_201_CREATED
        
        except Exception as e:
            logger.exception(f'Error creating comment for post_id: {post_id} - {e}')
            return {'Error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
