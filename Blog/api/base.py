import traceback

from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseView(APIView):
    permission_classes = [IsAuthenticated]
    request_serializer = serializers.Serializer
    response_serializer = serializers.Serializer
    
    def execute_post(self, *args, **kwargs):
        pass

    def post(self, request):
        try:
            # validate request
            serializer = self.request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            # get response
            response, status_code = self.execute_post(request=request,validated_data=validated_data)
            if response is None:
                traceback.print_exc()
                raise APIException()
            return Response(response, status=status_code)

        except APIException as e:
            traceback.print_exc()
            raise e
        
        except Exception as e:
            traceback.print_exc()
            raise APIException(e)
