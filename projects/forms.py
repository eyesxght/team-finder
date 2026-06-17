from django import forms

from .models import Project
from .validators import validate_github_url


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        validate_github_url(url)
        return url
