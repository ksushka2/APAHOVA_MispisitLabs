from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название курса")
    min_age = models.IntegerField(verbose_name="Минимальный возраст")
    max_age = models.IntegerField(verbose_name="Максимальный возраст")

    def __str__(self):
        return self.name

class StudentRequest(models.Model):
    public_number = models.CharField(max_length=20, unique=True, verbose_name="Номер заявки")
    child_full_name = models.CharField(max_length=255, verbose_name="ФИО ребенка")
    child_age = models.IntegerField(verbose_name="Возраст ребенка")
    parent_full_name = models.CharField(max_length=255, verbose_name="ФИО родителя")
    parent_phone = models.CharField(max_length=50, verbose_name="Телефон родителя")
    parent_email = models.CharField(max_length=254, verbose_name="Email родителя")
    course = models.ForeignKey(Course, on_delete=models.PROTECT, verbose_name="Выбранный курс")

    def __str__(self):
        return f"{self.public_number} - {self.child_full_name}"
