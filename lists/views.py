from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from pkg_resources import require

from lists.forms import TodoForm, TodoListForm
from lists.models import Todo, TodoList
from django.views.decorators.http import require_POST
import json
from django.db.models import Q
import uuid
from .tasks import delete_unauthcated_user_todolist
from datetime import datetime


def index(request):

    # apply_async(eta=datetime(2019, 7, 31, 6, 28))
    return render(request, "lists/index.html", {"form": TodoForm()})


def todolist_detail(request, todolist_id):

    if request.method == "POST":
        redirect("lists:add_todo", todolist_id=todolist_id)
    elif request.method == "GET":
        todolist = get_object_or_404(TodoList, pk=todolist_id)

        if todolist.creator == None:
            return render(
                request,
                "lists/todolist.html",
                {"todolist": todolist, "form": TodoForm()},
            )
        elif todolist.creator == request.user:
            return render(
                request,
                "lists/todolist.html",
                {"todolist": todolist, "form": TodoForm()},
            )
        else:

            # uuid.UUID(o['uuid']).hex
            auth_todo_token = request.GET.get("authID", "invalid_id")
            auth_todo_token = (
                auth_todo_token[0:-1] if auth_todo_token[-1] == "/" else auth_todo_token
            )
            print(
                "auth_todo_token",
            )
            todolisttoken = get_object_or_404(TodoList, secret_id_str=auth_todo_token)
            if not todolisttoken == todolist:
                # validating the todolist
                return HttpResponse("4040n not founr bro")
            else:
                return render(
                    request,
                    "lists/todolist.html",
                    {"todolist": todolist, "form": TodoForm()},
                )


def add_todo(request, pk):
    todolist = get_object_or_404(TodoList, pk=pk)
    post_data = json.loads(request.body.decode("utf-8"))
    user = request.user if request.user.is_authenticated else None
    # checking how many element in qs
    qs = Todo.objects.filter(todolist=todolist)
    # addding ranking to new todo
    new_todo_rank = qs.count() + 1

    todo_obj = Todo.objects.create(
        ranking=new_todo_rank,
        description=post_data.get("description"),
        creator=user,
        todolist=todolist,
    )
    todo_obj.save()
    print("reciive th dta", post_data, todolist)
    return JsonResponse({"added": True})


@login_required
def overview(request):
    if request.method == "POST":
        return redirect("lists:add_todolist")
    return render(request, "lists/overview.html", {"form": TodoListForm()})


def new_todolist(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            # create default todolist
            user = request.user if request.user.is_authenticated else None
            todolist = TodoList(creator=user, title=request.POST["description"])
            todolist.save()
            # delete todo of unauthcated_user in 168 hours
            if user == None:
                delete_unauthcated_user_todolist.delay(todolist.id)

            return redirect("lists:todolist", todolist_id=todolist.id)
        else:
            return render(request, "lists/index.html", {"form": form})

    return redirect("lists:index")


def add_todolist(request):
    if request.method == "POST":
        form = TodoListForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            todolist = TodoList(title=request.POST["title"], creator=user)
            todolist.save()
            return redirect("lists:todolist", todolist_id=todolist.id)
        else:
            return render(request, "lists/overview.html", {"form": form})

    return redirect("lists:index")


def open_finshed_todo(request, pk):
    todolist = get_object_or_404(TodoList, pk=pk)
    return render(request, "lists/open_finshed.html", {"todolist": todolist})


def finshed_open_todo(request, pk):
    todolist = get_object_or_404(TodoList, pk=pk)
    return render(request, "lists/finished_open.html", {"todolist": todolist})


@require_POST
def toggle_todo_finshed_open(request, todo_list_pk, todo_pk):
    todolist = get_object_or_404(TodoList, pk=todo_list_pk)
    todo_obj = get_object_or_404(Todo, pk=todo_pk, todolist=todolist)
    # toggle the todo
    todo_obj.toggle_open_finshed()
    return JsonResponse({"toggle_todo": True})


@require_POST
def change_ordering_todo(request, pk):
    todolist = get_object_or_404(TodoList, pk=pk)
    updated_dict = json.loads(request.POST.get("dict"))
    for key in updated_dict:
        todo_obj = Todo.objects.get(todolist=todolist, id=int(key))
        todo_obj.ranking = int(updated_dict[key])
        todo_obj.save()
    return JsonResponse({"changing ": True})


# toogle save  and unsave todolist  for the users
@login_required
def toogle_save_other_user_todolist(request, todolist_id):
    todolist = get_object_or_404(TodoList, pk=todolist_id)
    if todolist.creator != request.user:
        if request.user in todolist.saved_todo_user.all():
            todolist.saved_todo_user.remove(request.user)
        else:
            todolist.saved_todo_user.add(request.user)

        return redirect("lists:overview")
