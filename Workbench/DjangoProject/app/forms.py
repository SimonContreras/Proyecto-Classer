from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import TrainingDocument


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=254)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class ClassifyForm(forms.Form):
    sentence = forms.CharField()


class DocumentForm(forms.ModelForm):

    class Meta:
        model = TrainingDocument
        fields = ('description', 'document')

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['document'].widget.attrs \
            .update({
            'class': 'upload',
            'id': 'photosubmit',
            'name': 'photosubmit'
        })
        self.fields['description'].widget.attrs \
            .update({
            'class': 'form-control'
        })
        self.fields['document'].label = ''
        self.fields['description'].label = 'Descripción'