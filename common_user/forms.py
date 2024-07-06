from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'role')


class DatabaseBackupForm(forms.Form):
    backup_location = forms.CharField(
        label='Backup Location', 
        max_length=255, 
        initial='/home/mesele/erp/hotelerp/backup'
    )
