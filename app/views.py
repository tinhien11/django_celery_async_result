from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from tasks import task_get_data_from_spider
from celery.result import AsyncResult


def create_task(request):
    if request.method == 'POST':
        task = task_get_data_from_spider.delay(request.POST.get('parcel_id'))
        return redirect('task_result', task_id=task.task_id)
    return render(request, 'create_task.html', {})


def task_result(request, task_id):
    result = AsyncResult(task_id)
    if result.ready():
        return HttpResponse('Result is: %s' % (result.result,))
    else:
        return HttpResponse('Result is not ready yet!')
