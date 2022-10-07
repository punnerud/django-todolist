from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import User


class TodoList(models.Model):
    title = models.CharField(max_length=128, default="untitled")
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        User, null=True, related_name="todolists", on_delete=models.CASCADE
    )
    saved_todo_user = models.ManyToManyField(
        User, related_name="my_saved_todo", blank=True
    )
    # SECRET OF THE TODOLIST
    secret_id_uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    secret_id_str = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.secret_id_str

    def count(self):
        return self.todos.count()

    def count_finished(self):
        return self.todos.filter(is_finished=True).count()

    def count_open(self):
        return self.todos.filter(is_finished=False).count()

    def save(self, *args, **kwargs):
        self.secret_id_str = self.secret_id_uuid.hex
        super().save(*args, **kwargs)


class Todo(models.Model):
    ranking = models.PositiveIntegerField(null=True, blank=True)
    description = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    is_finished = models.BooleanField(default=False)

    creator = models.ForeignKey(
        User, null=True, related_name="todos", on_delete=models.CASCADE
    )
    todolist = models.ForeignKey(
        TodoList, related_name="todos", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("ranking",)

    def __str__(self):
        return self.description

    def close(self):
        self.is_finished = True
        self.finished_at = timezone.now()
        self.ranking = None
        self.save()

    def reopen(self):
        self.is_finished = False
        self.finished_at = None
        self.save()

    def toggle_open_finshed(self):
        if self.is_finished:
            self.reopen()
        else:
            self.close()
