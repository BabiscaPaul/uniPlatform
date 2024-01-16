from django import forms
from django.core.exceptions import ValidationError
from sharedmodels.models import Users

class StudentForm(forms.ModelForm):
    
    class Meta:
        model = Users
        fields = ['user_first_name', 'user_last_name', 'user_pic', 'user_address', 'user_email', 'user_phone_number', 'user_contract_number', 'user_iban']

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user