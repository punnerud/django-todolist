from celery import Celery
from datetime import datetime
from time import sleep
from celery import shared_task
from .models import TodoList

app = Celery()


@shared_task
def delete_unauthcated_user_todolist(todolist_id):
    print("added the task to delete will be delete in 168 hours")
    # wait for 168 hours 168*60*60=604800s
    sleep(604800)
    todo_obj = TodoList.objects.get(id=todolist_id)
    todo_obj.delete()
    print("Deleted the TodoList ")
