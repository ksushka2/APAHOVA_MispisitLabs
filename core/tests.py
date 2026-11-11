from django.core.management import call_command
from django.db import connection
from django.test import Client, TestCase
from django.urls import reverse

from .models import Course, StudentRequest


class ItSchoolFlowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # Новая таблица этой лабы создаётся при запуске, вне миграций.
        with connection.constraint_checks_disabled():
            call_command("init_notifications", verbosity=0)
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.course = Course.objects.get(name="Scratch для начинающих")

    def data(self, **changes):
        return {
            "child_full_name": "Анна Смирнова", "child_age": "8",
            "parent_full_name": "Мария Смирнова", "parent_phone": "+7 (900) 123-45-67",
            "parent_email": "parent@example.com", "course": str(self.course.pk), **changes,
        }

    def test_empty_list_and_shared_navigation(self):
        for url in ("/", "/requests/", "/requests/new/", "/access-denied/"):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Версия 0.0.5")
            self.assertContains(response, 'href="/requests/new/"')
            self.assertNotContains(response, "Педагог ДО")
        self.assertContains(self.client.get("/requests/"), "Заявок пока нет")

    def test_create_card_list_and_second_client_read_from_database(self):
        response = self.client.post(reverse("request_create"), self.data(), follow=True)
        self.assertEqual(response.status_code, 200)
        item = StudentRequest.objects.get()
        self.assertContains(response, item.public_number)
        self.assertContains(response, "Анна Смирнова")
        self.assertContains(Client().get("/requests/"), item.public_number)
        self.assertEqual(item.course_id, self.course.pk)

    def test_age_outside_course_is_rejected_without_write(self):
        for age in ("6", "10", "12"):
            response = self.client.post(reverse("request_create"), self.data(child_age=age), follow=True)
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.redirect_chain[-1][0], "/access-denied/?reason=age_mismatch")
            self.assertContains(response, "Возраст не подходит", status_code=422)
        self.assertFalse(StudentRequest.objects.exists())

    def test_both_inclusive_age_bounds_are_accepted(self):
        for age in ("7", "9"):
            self.assertEqual(self.client.post(reverse("request_create"), self.data(child_age=age)).status_code, 302)
        self.assertEqual(StudentRequest.objects.count(), 2)
        self.assertEqual(StudentRequest.objects.values("public_number").distinct().count(), 2)

    def test_invalid_fields_remain_on_form_without_write(self):
        for changes in ({"parent_email": "broken"}, {"child_full_name": "   "}, {"child_age": "abc"}, {"course": "999999"}, {"parent_phone": "123"}):
            response = self.client.post(reverse("request_create"), self.data(**changes))
            self.assertEqual(response.status_code, 400)
            self.assertContains(response, "Проверьте заполнение формы", status_code=400)
            self.assertContains(response, "Мария Смирнова", status_code=400)
        self.assertFalse(StudentRequest.objects.exists())

    def test_foreign_phone_and_matching_formatted_phone(self):
        self.client.post(reverse("request_create"), self.data())
        item = StudentRequest.objects.get()
        url = reverse("request_detail", args=(item.pk,))
        denied = self.client.get(url, {"parent_phone": "+7 (911) 111-11-11"}, follow=True)
        self.assertContains(denied, "Чужая заявка", status_code=403)
        self.assertNotContains(denied, "Анна Смирнова", status_code=403)
        self.assertEqual(self.client.get(url, {"parent_phone": "79001234567"}).status_code, 200)
        self.assertEqual(StudentRequest.objects.count(), 1)

    def test_missing_record_and_untrusted_error_text(self):
        response = self.client.get("/requests/999999/", follow=True)
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/access-denied/", {"detail": "<script>alert(1)</script>"})
        self.assertNotContains(response, "<script>")

    def test_existing_lab3_record_is_shown_unchanged(self):
        item = StudentRequest.objects.create(
            public_number="REQ-0001", course=self.course,
            **{key: value for key, value in self.data().items() if key != "course"},
        )
        self.assertContains(self.client.get(reverse("request_detail", args=(item.pk,))), "REQ-0001")
        item.refresh_from_db()
        self.assertEqual(item.parent_phone, "+7 (900) 123-45-67")

    def test_csrf_protection_and_get_does_not_create_records(self):
        response = Client(enforce_csrf_checks=True).post(reverse("request_create"), self.data())
        self.assertEqual(response.status_code, 403)
        self.client.get(reverse("request_create"), self.data())
        self.assertFalse(StudentRequest.objects.exists())
