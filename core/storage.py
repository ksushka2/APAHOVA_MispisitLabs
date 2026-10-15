import os
import json
from django.conf import settings

PRODUCT_NAME = ("Информационная система детской IT-школы: приём заявок на курсы, "
    "просмотр статусов и работа с учебными группами.")
VERSION = "0.0.2"

COURSES_FILE = os.path.join(settings.BASE_DIR, 'core', 'data', 'courses.json')
REQUESTS_FILE = os.path.join(settings.BASE_DIR, 'core', 'data', 'requests.json')

_REQUESTS_MEMORY_CACHE = []

def _init_requests_cache():
    global _REQUESTS_MEMORY_CACHE
    if not _REQUESTS_MEMORY_CACHE:
        if os.path.exists(REQUESTS_FILE):
            try:
                with open(REQUESTS_FILE, 'r', encoding='utf-8') as f:
                    _REQUESTS_MEMORY_CACHE = json.load(f)
            except Exception:
                _REQUESTS_MEMORY_CACHE = []
    return _REQUESTS_MEMORY_CACHE

def load_courses():
    if os.path.exists(COURSES_FILE):
        try:
            with open(COURSES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def get_course(course_id):
    for c in load_courses():
        if c.get("id") == int(course_id):
            return c
    return {}

def load_requests():
    return _init_requests_cache()

def get_request(pk):
    for r in load_requests():
        if r.get("id") == int(pk):
            return r
    return None

def age_fits_course(age, course_id):
    """Валидация возраста ребенка под требования курса"""
    course = get_course(course_id)
    if not course:
        return False, "Выбранный курс не найден в системе."
    
    min_age = course.get("min_age", 7)
    max_age = course.get("max_age", 17)
    
    if age < min_age or age > max_age:
        return False, f"Возраст ребенка ({age} лет) не подходит для курса '{course.get('name')}'. Допустимый возраст: от {min_age} до {max_age} лет."
    return True, "ОК"

def add_request(post_data):
    requests_list = load_requests()
    
    new_id = max([r.get('id', 0) for r in requests_list]) + 1 if requests_list else 1
    
    new_record = {
        "id": new_id,
        "public_number": f"REQ-{new_id:04d}",
        "child_full_name": post_data.get("child_full_name", "").strip(),
        "child_age": int(post_data.get("child_age", 0)),
        "parent_full_name": post_data.get("parent_full_name", "").strip(),
        "parent_phone": post_data.get("parent_phone", "").strip(),
        "parent_email": post_data.get("parent_email", "").strip(),
        "course_id": int(post_data.get("course_id", 0)),
    }
    requests_list.append(new_record)
    
    try:
        with open(REQUESTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(requests_list, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
        
    return new_record
