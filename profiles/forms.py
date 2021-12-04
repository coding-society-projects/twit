from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PostingForm(forms.Form):
    content = forms.CharField(label='Post something', max_length=140, min_length=5)


class SearchForm(forms.Form):
    term = forms.CharField(max_length=140, min_length=1,
                           widget=forms.TextInput(attrs={'class': 'form-control me-2', 'type': 'search',
                                                         'placeholder': "Search", 'aria-label': 'Search'}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self):
        user = super(RegisterForm, self).save()
        user.email = self.cleaned_data['email']
        user.save()
        return user




