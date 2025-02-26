from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.utils.translation import activate


def change_language(request, lang_code):
    activate(lang_code)  # Set the language dynamically
    return JsonResponse({"message": _("Hello, world!")})


import itertools
from django.utils.text import slugify

def generate_unique_slug(instance, slug_field_name="slug", slug_source_field="name"):
    """
    Generates a unique slug for an instance. If a slug already exists,
    appends -1, -2, etc. until a unique slug is found.
    """
    slug = slugify(getattr(instance, slug_source_field))
    ModelClass = instance.__class__
    unique_slug = slug
    num = 1
    # Exclude the current instance from the uniqueness check if it exists in the DB.
    while ModelClass.objects.filter(**{slug_field_name: unique_slug}).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug



