from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMessage
from django.db import transaction
from django.urls import reverse

from .models import Notification


def send_next_notification():
    """Отправляет одно новое сообщение. Блокировка исключает параллельный захват."""
    with transaction.atomic():
        item = (
            Notification.objects.select_for_update(skip_locked=True)
            .filter(status=Notification.Status.NEW)
            .order_by("created_at", "pk")
            .first()
        )
        if item is None:
            return None

        record = item.request
        link = settings.PUBLIC_BASE_URL + reverse("request_detail", args=[record.pk])
        email = EmailMessage(
            subject=f"Новая заявка {record.public_number}",
            body=f"{item.message}\n\nКарточка заявки: {link}\n",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.NOTIFICATION_RECIPIENT],
            headers={"Message-ID": f"<it-school-notification-{item.pk}@it-school.test>"},
        )
        if email.send(fail_silently=False) != 1:
            raise SMTPException("Почтовый сервер не подтвердил отправку сообщения.")

        item.status = Notification.Status.SENT
        item.save(update_fields=["status"])
        return item.pk
