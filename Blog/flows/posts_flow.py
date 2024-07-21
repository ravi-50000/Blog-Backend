import logging
from rest_framework import status
from Blog.models import Post
from Blog.utils import get_paginated_results
from Blog_Project.settings import PAGE_LIMIT
from Blog.serializers import PostResponseSerializer
from django.shortcuts import get_object_or_404
from django.conf import settings
logger = logging.getLogger(settings.DEBUG_LOGGER_DJANGO)

class PostViewFlow:
    def __init__(self, **kwargs):
        self.user = kwargs.get('request_user')
        
    def get_all_posts(self, validated_data):
        try:
            page_number = validated_data.get('page_number', 1)
            logger.info(f'Fetching posts for page_number: {page_number}')
            all_posts = Post.objects.select_related('author').filter(is_deleted=False)
            page_obj, page_context = get_paginated_results(all_posts, page_number, PAGE_LIMIT)
            result_list = []
            for post in page_obj.object_list:
                data = PostResponseSerializer(post).data
                data['id'] = str(post.id)
                result_list.append(data)
            result = {
                "page_context": page_context,
                "result": result_list
            }
            logger.info(f'Fetched {len(result_list)} posts for page_number: {page_number}')
            return result, status.HTTP_200_OK
        
        except Exception as e:
            logger.exception(f'Error fetching posts for page_number: {page_number} - {e}')
            return {'Error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
        
    def create_post(self, validated_data):
        try:
            title = validated_data.get('title')
            content = validated_data.get('content')
            author = self.user
            post = Post.objects.create(
                title=title,
                content=content,
                author=author,
            )
            result = PostResponseSerializer(post).data
            result['id'] = str(post.id)
            logger.info(f'Created post with id: {post.id}')
            return result, status.HTTP_201_CREATED
        
        except Exception as e:
            logger.exception(f'Error creating post with title: "{title}" - {e}')
            return {'Error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
        
    def retrieve_post(self, post_id):
        try:
            logger.info(f'Retrieving post with id: {post_id}')
            post = get_object_or_404(Post, id=post_id, is_deleted=False)
            post_serializer = PostResponseSerializer(post)
            logger.info(f'Retrieved post with id: {post_id}')
            return post_serializer.data, status.HTTP_200_OK
        
        except Exception as e:
            logger.exception(f'Error retrieving post with id: {post_id} - {e}')
            return {'Error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def update_post(self, validated_data):
        try:
            post_id = validated_data.get('post_id')
            logger.info(f'Updating post with id: {post_id}')
            post = get_object_or_404(Post, id=post_id, is_deleted=False)
            if self.user != post.author:
                logger.warning(f'User: {self.user} is not authorized to update post with id: {post_id}')
                return {'Error': 'You are not authorized to update this post'}, status.HTTP_403_FORBIDDEN
        
            title = validated_data.get('title')
            content = validated_data.get('content')
            update_fields = []
            if title:
                post.title = title
                update_fields.append('title')
            if content:
                post.content = content
                update_fields.append('content')
            
            if update_fields:
                update_fields.append('modified')
                post.save(update_fields=update_fields)
            
            result = PostResponseSerializer(post).data
            result['id'] = str(post.id)
            logger.info(f'Updated post with id: {post.id}')
            return result, status.HTTP_200_OK
        
        except Exception as e:
            logger.exception(f'Error updating post with id: {post_id} - {e}')
            return {'Error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def delete_post(self, validated_data):
        try:
            post_id = validated_data.get('post_id')
            logger.info(f'Deleting post with id: {post_id}')
            post = get_object_or_404(Post, id=post_id, is_deleted=False)
            if self.user != post.author:
                logger.warning(f'User: {self.user} is not authorized to delete post with id: {post_id}')
                return {'Error': 'You are not authorized to delete this post'}, status.HTTP_403_FORBIDDEN

            post.is_deleted = True
            post.save(update_fields=['is_deleted', 'modified'])
            logger.info(f'Deleted post with id: {post.id}')
            return {'Message': 'Post Deleted Successfully'}, status.HTTP_200_OK
        
        except Exception as e:
            logger.exception(f'Error deleting post with id: {post_id} - {e}')
            return {'Error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def like_post_and_get_count(self, post_id):
        try:
            logger.info(f'Like request for post with id: {post_id} by user: {self.user}')
            post = get_object_or_404(Post, id=post_id, is_deleted=False)
            if post.likes.filter(id=self.user.id).exists():
                logger.info(f'Post with id: {post_id} already liked by user: {self.user}')
                like_count = post.likes.count()
                return {'Message': 'Post already liked', 'LikeCount': like_count}, status.HTTP_200_OK
           
            post.likes.add(self.user)
            like_count = post.likes.count()
            logger.info(f'Post with id: {post_id} liked successfully. Total likes: {like_count}')
            return {'Message': 'Post Liked Successfully', 'LikeCount': like_count}, status.HTTP_200_OK
        
        except Exception as e:
            logger.exception(f'Error liking post with id: {post_id} - {e}')
            return {'Error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR
