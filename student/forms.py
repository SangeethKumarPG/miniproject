from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                }
            )
    class Meta:
        model = Registration
        exclude = [
            'selected_course',
            'date_of_admission',
            'roll_no',
            'fees'
        ]
