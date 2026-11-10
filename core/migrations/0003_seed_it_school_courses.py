from django.db import migrations


def seed_courses(apps, schema_editor):
    courses = apps.get_model("core", "Course").objects.using(schema_editor.connection.alias)
    # Existing courses and applications from lab 3 are left as they are.
    if not courses.exists():
        for name, min_age, max_age in (
            ("Scratch для начинающих", 7, 9),
            ("Python Junior (Робототехника)", 10, 13),
            ("Web-разработка (HTML/CSS)", 14, 17),
        ):
            courses.create(name=name, min_age=min_age, max_age=max_age)


class Migration(migrations.Migration):
    dependencies = [("core", "0002_teacher_cabinet")]
    operations = [migrations.RunPython(seed_courses, migrations.RunPython.noop)]
