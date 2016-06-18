from celery.result import AsyncResult
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks import task_get_data_from_spider


class TaskList(APIView):
    """
    List all snippets, or create a new task spider.
    """

    def get(self, request):
        """
        ---
        parameters:
            - name: task_id
              paramType: query
              defaultValue: ''
        response_serializer: ''
        responseMessages:
            - code: 400
              message: '{"message": "", "data": ""}'
            - code: 200
              message: '{"message": "", "data": ""}'
        """
        task_id = request.query_params.get('task_id')
        if task_id:
            result = AsyncResult(task_id)
            if result.ready():
                # res = repr(result.result).decode("unicode-escape")
                return Response(result.result, status=status.HTTP_200_OK)
            return Response({'message': 'Result is not ready yet!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Missing param task_id'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """
        ---
        parameters:
            - name: parameters
              type: json
              paramType: body
              description: "`parcel_id`"
              defaultValue: '{"parcel_id": "EL745355158VN"}'
        response_serializer: ''
        responseMessages:
            - code: 400
              message: '{"message": "", "data": ""}'
            - code: 200
              message: '{"message": "", "data": ""}'
        """
        parcel_id = request.data.get('parcel_id')
        if parcel_id:
            task = task_get_data_from_spider.delay(parcel_id)
            return Response({'task_id': task.task_id}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Parcel id must be not empty'}, status=status.HTTP_400_BAD_REQUEST)
