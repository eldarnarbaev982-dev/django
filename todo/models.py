from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# 1. Профиль пользователя
class UserProfile(AbstractUser):
    STATUS_CHOICES = (
        ('beginner', 'Beginner'),
        ('active', 'Active'),
        ('pro', 'Pro'),
    )

    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(14), MaxValueValidator(70)],
        null=True,
        blank=True,
        verbose_name="Возраст"
    )
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватар")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='beginner', verbose_name="Статус")
    date_register = models.DateField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self):
        return self.username


# 2. Категория
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True, verbose_name="Название категории")
    category_img = models.ImageField(upload_to="categories/", blank=True, null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.category_name


# 3. Проект
class Project(models.Model):
    project_name = models.CharField(max_length=100, verbose_name="Название проекта")
    description = models.TextField(blank=True, verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="projects", verbose_name="Категория")
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="projects", verbose_name="Владелец")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.project_name

    def get_tasks_count(self):
        return self.tasks.count()

    def get_completed_percent(self):
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.tasks.filter(completed=True).count()
        return round((completed_tasks / total_tasks) * 100, 2)


# 4. Тег
class Tag(models.Model):
    tag_name = models.CharField(max_length=30, unique=True, verbose_name="Тег")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.tag_name


# 5. Задача
class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    completed = models.BooleanField(default=False, verbose_name="Выполнено")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Приоритет")
    deadline = models.DateTimeField(null=True, blank=True, verbose_name="Срок выполнения")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks", verbose_name="Проект")
    assignee = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks", verbose_name="Исполнитель")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title

    def get_progress(self):
        total_subtasks = self.subtasks.count()
        if total_subtasks == 0:
            return 0
        completed_subtasks = self.subtasks.filter(completed=True).count()
        return round((completed_subtasks / total_subtasks) * 100, 2)

    def get_comments_count(self):
        return self.comments.count()

    def is_overdue(self):
        if self.deadline and not self.completed:
            return timezone.now() > self.deadline
        return False


# 6. Подзадача
class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks", verbose_name="Задача")
    title = models.CharField(max_length=100, verbose_name="Название подзадачи")
    completed = models.BooleanField(default=False, verbose_name="Выполнено")

    class Meta:
        verbose_name = "Подзадача"
        verbose_name_plural = "Подзадачи"

    def __str__(self):
        return self.title


# 7. Файл задачи
class TaskFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="files", verbose_name="Задача")
    file = models.FileField(upload_to="task_files/", verbose_name="Файл")

    class Meta:
        verbose_name = "Файл задачи"
        verbose_name_plural = "Файлы задач"


# 8. Комментарий
class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments", verbose_name="Задача")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="Автор")
    text = models.TextField(verbose_name="Текст комментария")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.task.title}"


# 9. Избранное
class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="favorite", verbose_name="Пользователь")

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"Избранное пользователя {self.user.username}"


# 10. Элемент избранного
class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name="items", verbose_name="Список избранного")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="Задача")

    class Meta:
        verbose_name = "Элемент избранного"
        verbose_name_plural = "Элементы избранного"
        unique_together = ('favorite', 'task')

    def __str__(self):
        return f"{self.task.title} в {self.favorite}"