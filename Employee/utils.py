from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.utils.translation import activate


def change_language(request, lang_code):
    activate(lang_code)  # Set the language dynamically
    return JsonResponse({"message": _("Hello, world!")})


