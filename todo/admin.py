from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    UserProfile, Category, Project, Tag, Task,
    Subtask, TaskFile, Comment, Favorite, FavoriteItem
)


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'age', 'phone_number', 'status', 'is_staff')
    list_filter = ('status', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone_number')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('age', 'phone_number', 'avatar', 'status')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)
    search_fields = ('tag_name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'category', 'owner', 'get_tasks_count', 'get_completed_percent')
    list_filter = ('category',)
    search_fields = ('project_name', 'owner__username')


class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1


class TaskFileInline(admin.TabularInline):
    model = TaskFile
    extra = 1


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'priority', 'completed', 'deadline', 'get_progress', 'get_comments_count')
    list_filter = ('priority', 'completed', 'project')
    search_fields = ('title', 'description')
    inlines = [SubtaskInline, TaskFileInline, CommentInline]


class FavoriteItemInline(admin.TabularInline):
    model = FavoriteItem
    extra = 1


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = [FavoriteItemInline]