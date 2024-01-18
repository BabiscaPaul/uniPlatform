from django import forms
from django.core.exceptions import ValidationError
from sharedmodels.models import Activities, Teachers, Users, Courses, Seminars, Laboratories

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
    
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['user_first_name', 'user_last_name', 'user_pic', 'user_address', 'user_email', 'user_phone_number', 'user_contract_number', 'user_iban']

    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    
class GradeForm(forms.Form):
    grade_value = forms.IntegerField()
    course = forms.ModelChoiceField(queryset=Courses.objects.none(), required=False)
    laboratory = forms.ModelChoiceField(queryset=Laboratories.objects.none(), required=False)
    seminar = forms.ModelChoiceField(queryset=Seminars.objects.none(), required=False)

    def __init__(self, *args, assigned_courses=None, assigned_laboratories=None, assigned_seminars=None, **kwargs):
        super().__init__(*args, **kwargs)
        if assigned_courses is not None:
            self.fields['course'].queryset = Courses.objects.filter(course_id__in=[course.course_id for course in assigned_courses])
            self.fields['course'].label_from_instance = lambda obj: f"{obj.course_name}"  # replace 'name' with the actual field that stores the course name
        if assigned_laboratories is not None:
            self.fields['laboratory'].queryset = Laboratories.objects.filter(laboratory_id__in=[laboratory.laboratory_id for laboratory in assigned_laboratories])
            self.fields['laboratory'].label_from_instance = lambda obj: f"{obj.laboratory_name}"  # replace 'name' with the actual field that stores the laboratory name
        if assigned_seminars is not None:
            self.fields['seminar'].queryset = Seminars.objects.filter(seminar_id__in=[seminar.seminar_id for seminar in assigned_seminars])
            self.fields['seminar'].label_from_instance = lambda obj: f"{obj.seminar_name}"  # replace 'name' with the actual field that stores the seminar name