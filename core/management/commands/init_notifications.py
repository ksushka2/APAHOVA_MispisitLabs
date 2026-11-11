from django.core.management.base import BaseCommand
from django.db import connection

from core.models import Notification


class Command(BaseCommand):
    help = "Создаёт таблицу уведомлений, если её ещё нет. Существующие данные не меняет."

    def handle(self, *args, **options):
        table_name = Notification._meta.db_table
        if table_name in connection.introspection.table_names():
            self.stdout.write("Таблица уведомлений уже существует.")
            return
        with connection.schema_editor() as editor:
            editor.create_model(Notification)
        self.stdout.write(self.style.SUCCESS("Таблица уведомлений создана."))
