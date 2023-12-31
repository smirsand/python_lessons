from django import forms
from .models import TestResult, Test


class TestResultForm(forms.ModelForm):
    """
    Форма модели 'TestResult'.
    """

    class Meta:
        model = TestResult
        fields = ['choice']


class TestForm(forms.ModelForm):
    """
    Форма модели 'Test'.
    """

    class Meta:
        model = Test
        fields = '__all__'
