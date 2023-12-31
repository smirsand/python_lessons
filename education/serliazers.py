from rest_framework import serializers

from education.models import Chapter, Material, Test, TestResult


class ChapterSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели 'Chapter'.
    """

    class Meta:
        model = Chapter
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели 'Material'.
    """

    class Meta:
        model = Material
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели 'Test'.
    """

    class Meta:
        model = Test
        fields = '__all__'


class TestResultSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели 'TestResult'.
    """
    is_correct = serializers.BooleanField()

    class Meta:
        model = TestResult
        fields = "__all__"
