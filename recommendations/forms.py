"""
Forms for the Recommendation Engine
"""
from django import forms
from .models import UserRating


class RatingForm(forms.ModelForm):
    class Meta:
        model = UserRating
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'review': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your review...'}),
        }
