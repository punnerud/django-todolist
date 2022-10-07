from django.urls import path

from lists import views

app_name = "lists"
urlpatterns = [
    path("", views.index, name="index"),
    path("todolist/<int:todolist_id>/", views.todolist_detail, name="todolist"),
    path(
        "save-other-user-todolist/<int:todolist_id>/",
        views.toogle_save_other_user_todolist,
        name="toogle_save_other_user_todolist",
    ),
    path(
        "open-finshed-todo/<int:pk>/", views.open_finshed_todo, name="open_finshed_todo"
    ),
    path(
        "finshed-open-todo/<int:pk>/", views.finshed_open_todo, name="finshed_open_todo"
    ),
    path(
        "toggle-todo-finshed-open/<int:todo_list_pk>/<int:todo_pk>/",
        views.toggle_todo_finshed_open,
        name="toggle_todo_finshed_open",
    ),
    path("todolist/new/", views.new_todolist, name="new_todolist"),
    path("todolist/add/", views.add_todolist, name="add_todolist"),
    path("add-todolist/<int:pk>/", views.add_todo, name="add_todo"),
    path(
        "change-ordering-todo/<int:pk>/",
        views.change_ordering_todo,
        name="change_ordering_todo",
    ),
    path("todolists/", views.overview, name="overview"),
]
