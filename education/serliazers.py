from rest_framework import serializers

from education.models import Chapter, Material, Test, TestResult


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class TestResultSerializer(serializers.ModelSerializer):
    is_correct = serializers.BooleanField()

    class Meta:
        model = TestResult
        fields = "__all__"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
