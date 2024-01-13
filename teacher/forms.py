from django import forms
from django.core.exceptions import ValidationError
from sharedmodels.models import Activities

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activities
        fields = ['activity_type', 'activity_start_date', 'activity_end_date', 'activity_max_students']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('activity_start_date')
        end_date = cleaned_data.get('activity_end_date')

        if start_date and end_date:
            # Check if end date is before start date
            if end_date < start_date:
                raise ValidationError("End date should be after start date.")

        return cleaned_data