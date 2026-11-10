from django.db import migrations, models
import django.db.models.deletion


def seed_programs(apps, schema_editor):
    programs = apps.get_model("core", "SupportProgram").objects.using(schema_editor.connection.alias)
    for name, min_experience in (
        ("Цифровые инструменты для занятий", 0),
        ("Проектное обучение в объединении", 1),
        ("Наставничество педагогов", 3),
    ):
        programs.get_or_create(name=name, defaults={"min_experience": min_experience})


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="SupportProgram",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160, unique=True)),
                ("min_experience", models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="TeacherRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=160)),
                ("organization", models.CharField(max_length=160)),
                ("email", models.EmailField(max_length=254)),
                ("experience", models.PositiveSmallIntegerField()),
                ("owner_session", models.CharField(editable=False, max_length=40)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("program", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="core.supportprogram")),
            ],
        ),
        migrations.RunPython(seed_programs, migrations.RunPython.noop),
    ]
