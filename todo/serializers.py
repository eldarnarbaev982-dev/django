from rest_framework import serializers
from .models import Task, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    progress = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_progress(self, obj):
        return obj.get_progress()

    def get_comments_count(self, obj):
        return obj.get_comments_count()

    def get_is_overdue(self, obj):
        return obj.is_overdue()