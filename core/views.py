from urllib.parse import urlencode

from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import TeacherRequestForm
from .models import TeacherRequest


PRODUCT_NAME = "Платформа поддержки обучения для педагогов дополнительного образования"
VERSION = "0.0.4"
DENIALS = {
    "invalid_data": ("Проверьте данные заявки", "Заполните обязательные поля, укажите рабочую почту и выберите программу."),
    "experience_mismatch": ("Недостаточно педагогического стажа", "Указанный стаж меньше минимального для этой программы. Выберите программу с подходящими условиями."),
    "foreign_request": ("Карточка заявки закрыта", "Подробности заявки доступны в том же браузере, в котором она была подана."),
    "not_found": ("Заявка не найдена", "Вернитесь в реестр и выберите существующую заявку."),
}
DENIAL_DEMO = (
    "Проверка отказа",
    "Чтобы получить отказ, выберите программу «Наставничество педагогов» и укажите стаж 1 год. Для просмотра чужой заявки откройте её карточку в приватном окне.",
)


def _page(request, template, active_nav, *, status=200, **context):
    return render(
        request,
        f"core/{template}.html",
        {"product_name": PRODUCT_NAME, "version": VERSION, "active_nav": active_nav, **context},
        status=status,
    )


def _deny(reason):
    query = urlencode({"reason": reason})
    return redirect(f"{reverse('access_denied')}?{query}")


def home(request):
    return _page(request, "home", "home")


def request_list(request):
    items = TeacherRequest.objects.select_related("program").order_by("-pk")
    return _page(request, "request_list", "list", requests=items)


def request_create(request):
    form = TeacherRequestForm(request.POST if request.method == "POST" else None)
    if request.method == "POST":
        if not form.is_valid():
            return _deny("invalid_data")

        record = form.save(commit=False)
        if record.experience < record.program.min_experience:
            return _deny("experience_mismatch")

        request.session.setdefault("teacher_cabinet", True)
        if request.session.session_key is None:
            request.session.save()
        record.owner_session = request.session.session_key
        record.save()
        return redirect("request_detail", pk=record.pk)

    return _page(request, "request_form", "new", form=form)


def request_detail(request, pk):
    record = TeacherRequest.objects.select_related("program").filter(pk=pk).first()
    if record is None:
        return _deny("not_found")
    if request.session.session_key != record.owner_session:
        return _deny("foreign_request")
    return _page(request, "request_detail", "list", item=record)


def access_denied(request):
    reason = request.GET.get("reason", "")
    denial = DENIALS.get(reason)
    title, detail = denial or DENIAL_DEMO
    status = {"not_found": 404, "invalid_data": 400, "experience_mismatch": 422, "foreign_request": 403}
    return _page(
        request, "access_denied", "denied",
        status=status.get(reason, 200), reason_title=title, detail=detail, is_demo=denial is None,
    )
