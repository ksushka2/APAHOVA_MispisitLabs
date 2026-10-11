from django.shortcuts import render


def home(request):
    return render(
        request,
        "core/home.html",
        {
            "product_name": "IT-Школа",
            "description": (
                "Информационная система детской IT-школы."
            ),
            "version": "0.0.1",
        },
    )
