from django import forms

from .models import TeacherRequest


class TeacherRequestForm(forms.ModelForm):
    experience = forms.IntegerField(
        label="Педагогический стаж, лет",
        min_value=0,
        max_value=70,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Например, 4"}),
    )

    class Meta:
        model = TeacherRequest
        fields = ("full_name", "organization", "email", "experience", "program")
        labels = {
            "full_name": "ФИО педагога",
            "organization": "Организация дополнительного образования",
            "email": "Рабочая почта",
            "program": "Программа поддержки",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "autocomplete": "name"}),
            "organization": forms.TextInput(attrs={"class": "form-control", "autocomplete": "organization"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
            "program": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        program = self.fields["program"]
        program.queryset = program.queryset.order_by("min_experience", "name")
        program.empty_label = "Выберите программу"
