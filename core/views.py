from urllib.parse import urlencode
from uuid import uuid4

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods

from .forms import StudentRequestForm
from .models import Course, StudentRequest


PRODUCT_NAME = "IT-Школа"
VERSION = "0.0.4"
DENIALS = {
    "age_mismatch": (
        "Возраст не подходит для курса",
        "Возраст ребёнка выходит за диапазон выбранного курса. Заявка не сохранена. Выберите подходящее направление и отправьте форму снова.", 422,
    ),
    "foreign_request": (
        "Чужая заявка",
        "Указанный телефон родителя не совпадает с телефоном в заявке. Действие отклонено, данные заявки не изменены.", 403,
    ),
    "not_found": (
        "Заявка не найдена",
        "Заявки с таким номером нет. Вернитесь к списку и выберите существующую запись.", 404,
    ),
}


def _page(request, template, active_nav, *, status=200, **context):
    return render(request, f"core/{template}.html", {
        "product_name": PRODUCT_NAME, "version": VERSION, "active_nav": active_nav, **context,
    }, status=status)


def _deny(reason):
    return redirect(f"{reverse('access_denied')}?{urlencode({'reason': reason})}")


@require_GET
def home(request):
    return _page(request, "home", "home", courses=Course.objects.order_by("min_age", "pk"))


@require_GET
def request_list(request):
    items = StudentRequest.objects.select_related("course").order_by("-pk")
    return _page(request, "request_list", "list", requests=items)


@require_http_methods(["GET", "POST"])
def request_create(request):
    form = StudentRequestForm(
        request.POST if request.method == "POST" else None,
        initial={"course": request.GET.get("course")},
    )
    if request.method == "POST" and form.is_valid():
        record = form.save(commit=False)
        if not record.course.min_age <= record.child_age <= record.course.max_age:
            return _deny("age_mismatch")
        # UUID-based numbers avoid a race between simultaneous form submissions.
        record.public_number = f"REQ-{uuid4().hex[:12].upper()}"
        record.save()
        return redirect("request_detail", pk=record.pk)
    return _page(request, "request_form", "new", form=form,
                 status=400 if request.method == "POST" else 200)


@require_GET
def request_detail(request, pk):
    record = StudentRequest.objects.select_related("course").filter(pk=pk).first()
    if record is None:
        return _deny("not_found")
    # Preserve the phone-mismatch demonstration from labs 2 and 3.
    # This shared educational interface does not implement account authentication.
    if "parent_phone" in request.GET:
        digits = lambda value: "".join(c for c in value if c.isdigit())
        if digits(request.GET["parent_phone"]) != digits(record.parent_phone):
            return _deny("foreign_request")
    return _page(request, "request_detail", "list", item=record)


@require_GET
def access_denied(request):
    reason = request.GET.get("reason", "")
    denial = DENIALS.get(reason)
    title, detail, status = denial or (
        "Как проверить отказ",
        "Откройте форму и укажите возраст, который не входит в диапазон курса. Например, выберите Scratch для начинающих и укажите 12 лет. Новая запись не появится в списке.", 200,
    )
    return _page(request, "access_denied", "denied", status=status,
                 reason_title=title, detail=detail, reason_code=reason, is_demo=denial is None)
