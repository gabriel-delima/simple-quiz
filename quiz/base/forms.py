from django.forms import ModelForm
from quiz.base.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']