import time

from django.core.management.base import BaseCommand, CommandError
from django.db import close_old_connections

from core.notifications import send_next_notification


class Command(BaseCommand):
    help = "Отправляет новые уведомления в Mailpit и отмечает их как отправленные."

    def add_arguments(self, parser):
        parser.add_argument("--interval", type=float, default=3, help="Пауза между проверками, секунд.")
        parser.add_argument("--once", action="store_true", help="Обработать одну порцию и завершить работу.")

    def handle(self, *args, **options):
        interval = options["interval"]
        if interval <= 0:
            raise CommandError("Интервал должен быть больше нуля.")
        self.stdout.write("Worker уведомлений запущен.")
        try:
            while True:
                close_old_connections()
                try:
                    for _ in range(20):
                        pk = send_next_notification()
                        if pk is None:
                            break
                        self.stdout.write(f"Уведомление {pk}: письмо принято Mailpit, статус «Отправлено».")
                except Exception as error:
                    # При сбое транзакция откатывается, сообщение остаётся новым.
                    if options["once"]:
                        raise CommandError(str(error)) from error
                    self.stderr.write(f"Отправка не выполнена, повтор через {interval:g} с: {error}")
                finally:
                    close_old_connections()
                if options["once"]:
                    return
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write("Worker остановлен.")
