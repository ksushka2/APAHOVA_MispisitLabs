from urllib.parse import urlencode
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Course, StudentRequest

def home(request):
    return render(
        request,
        "core/home.html",
        {
            "product_name": "IT-Школа",
            "description": "Информационная система детской IT-школы.",
            "version": "0.0.3",  
            "active_nav": "home",
        },
    )

def _base_context(**extra):
    return {
        "product_name": "IT-Школа",
        "version": "0.0.3",
        **extra
    }

def request_list(request):
    items = StudentRequest.objects.select_related('course').all()
    formatted_items = []
    for item in items:
        formatted_items.append({
            "id": item.id,
            "public_number": item.public_number,
            "child_full_name": item.child_full_name,
            "child_age": item.child_age,
            "parent_full_name": item.parent_full_name,
            "parent_phone": item.parent_phone,
            "parent_email": item.parent_email,
            "course_name": item.course.name
        })
    return render(request, "core/request_list.html", _base_context(requests=formatted_items))

def request_create(request):
    #первичное автонаполнение справочника курсов, если база пустая
    if not Course.objects.exists():
        Course.objects.create(name="Python Junior (Робототехника)", min_age=10, max_age=13)
        Course.objects.create(name="Scratch для начинающих", min_age=7, max_age=9)
        Course.objects.create(name="Web-разработка (HTML/CSS)", min_age=14, max_age=17)

    courses = Course.objects.all()

    if request.method == "POST":
        required = ["child_full_name", "child_age", "parent_full_name", "parent_phone", "parent_email", "course_id"]
        if not all(str(request.POST.get(f, "")).strip() for f in required):
            params = urlencode({"reason": "empty_fields", "detail": "Заполните все обязательные поля заявки."})
            return redirect(f"{reverse('access_denied')}?{params}")

        try:
            child_age = int(request.POST["child_age"])
            course_id = int(request.POST["course_id"])
            course = Course.objects.get(id=course_id)
        except (TypeError, ValueError, Course.DoesNotExist):
            params = urlencode({"reason": "invalid_data", "detail": "Указаны некорректные параметры данных."})
            return redirect(f"{reverse('access_denied')}?{params}")

        #сценарий логического отказа по возрасту ребенка
        if child_age < course.min_age or child_age > course.max_age:
            message = f"Возраст ребенка ({child_age} лет) не подходит для курса '{course.name}'. Допустимый возраст: от {course.min_age} до {course.max_age} лет."
            params = urlencode({"reason": "age_mismatch", "detail": message})
            return redirect(f"{reverse('access_denied')}?{params}")

        #сохранение записи в СУБД
        next_id = (StudentRequest.objects.latest('id').id + 1) if StudentRequest.objects.exists() else 1
        record = StudentRequest.objects.create(
            public_number=f"REQ-{next_id:04d}",
            child_full_name=request.POST["child_full_name"].strip(),
            child_age=child_age,
            parent_full_name=request.POST["parent_full_name"].strip(),
            parent_phone=request.POST["parent_phone"].strip(),
            parent_email=request.POST["parent_email"].strip(),
            course=course
        )
        return redirect("request_detail", pk=record.id)

    return render(request, "core/request_form.html", _base_context(courses=courses))

def request_detail(request, pk):
    try:
        record = StudentRequest.objects.select_related('course').get(id=pk)
    except StudentRequest.DoesNotExist:
        params = urlencode({"reason": "not_found", "detail": f"Заявка №{pk} не найдена."})
        return redirect(f"{reverse('access_denied')}?{params}")

    # Ошибочный сценарий: просмотр чужой заявки
    viewer_phone = (request.GET.get("parent_phone") or "").strip()
    if viewer_phone and viewer_phone != record.parent_phone:
        params = urlencode({
            "reason": "foreign_request",
            "detail": "Родитель пытался открыть заявку с чужим номером телефона. Просмотр доступен только владельцу.",
            "attempted": record.public_number,
        })
        return redirect(f"{reverse('access_denied')}?{params}")

    formatted_record = {
        "id": record.id,
        "public_number": record.public_number,
        "child_full_name": record.child_full_name,
        "child_age": record.child_age,
        "parent_full_name": record.parent_full_name,
        "parent_phone": record.parent_phone,
        "parent_email": record.parent_email,
        "course_id": record.course.id
    }
    return render(request, "core/request_detail.html", _base_context(item=formatted_record, course=record.course, viewer_phone=viewer_phone))

def access_denied(request):
    reason = request.GET.get("reason", "unknown")
    detail = request.GET.get("detail", "Система отклонила действие из-за ошибки.")
    attempted = request.GET.get("attempted", "")

    reason_titles = {
        "empty_fields": "Пустые обязательные поля",
        "invalid_data": "Недопустимые значения",
        "age_mismatch": "Возраст не подходит к курсу",
        "foreign_request": "Чужая заявка",
        "not_found": "Заявка не найдена",
        "unknown": "Отказ",
    }
    return render(request, "core/access_denied.html", _base_context(reason_code=reason, reason_title=reason_titles.get(reason, "Отказ"), detail=detail, attempted=attempted))
