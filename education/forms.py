from django import forms
from .models import TestResult, Test


class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ['choice']


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
