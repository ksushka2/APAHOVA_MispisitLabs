from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="Название курса")),
                ("min_age", models.IntegerField(verbose_name="Минимальный возраст")),
                ("max_age", models.IntegerField(verbose_name="Максимальный возраст")),
            ],
        ),
        migrations.CreateModel(
            name="StudentRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("public_number", models.CharField(max_length=20, unique=True, verbose_name="Номер заявки")),
                ("child_full_name", models.CharField(max_length=255, verbose_name="ФИО ребенка")),
                ("child_age", models.IntegerField(verbose_name="Возраст ребенка")),
                ("parent_full_name", models.CharField(max_length=255, verbose_name="ФИО родителя")),
                ("parent_phone", models.CharField(max_length=50, verbose_name="Телефон родителя")),
                ("parent_email", models.CharField(max_length=254, verbose_name="Email родителя")),
                ("course", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="core.course", verbose_name="Выбранный курс")),
            ],
        ),
    ]
