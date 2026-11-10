from django import forms

from .models import Course, StudentRequest, TeacherRequest


class CourseChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, course):
        return f"{course.name} · {course.min_age}–{course.max_age} лет"


class StudentRequestForm(forms.ModelForm):
    parent_email = forms.EmailField(
        label="Электронная почта", max_length=254,
        widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email", "placeholder": "parent@example.com"}),
    )
    child_age = forms.IntegerField(
        label="Возраст ребёнка", min_value=0, max_value=120,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Полных лет"}),
    )
    course = CourseChoiceField(
        label="Курс", queryset=Course.objects.none(), empty_label="Выберите направление",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = StudentRequest
        fields = ("child_full_name", "child_age", "parent_full_name", "parent_phone", "parent_email", "course")
        labels = {
            "child_full_name": "ФИО ребёнка", "parent_full_name": "ФИО родителя",
            "parent_phone": "Телефон родителя", "parent_email": "Электронная почта",
        }
        widgets = {
            "child_full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Фамилия Имя Отчество"}),
            "parent_full_name": forms.TextInput(attrs={"class": "form-control", "autocomplete": "name", "placeholder": "Фамилия Имя Отчество"}),
            "parent_phone": forms.TextInput(attrs={"class": "form-control", "type": "tel", "autocomplete": "tel", "placeholder": "+7 (900) 123-45-67"}),
            "parent_email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email", "placeholder": "parent@example.com"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.order_by("min_age", "pk")
        for name, field in self.fields.items():
            field.widget.attrs["aria-describedby"] = f"id_{name}_errors"

    def clean_parent_phone(self):
        phone = self.cleaned_data["parent_phone"]
        if not 10 <= len("".join(c for c in phone if c.isdigit())) <= 15:
            raise forms.ValidationError("Укажите телефон, содержащий от 10 до 15 цифр.")
        return phone


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
