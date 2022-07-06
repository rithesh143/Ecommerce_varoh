from django.contrib import admin
from .models import (
    Games,
    ActivityBox,
    SpecialBooks,
    KnowledgeCapsule,
    Standard,
    Pricing,
    APIRazor
)
# Register your models here.
admin.site.register(Standard)
admin.site.register(Games)
admin.site.register(ActivityBox)
admin.site.register(SpecialBooks)
admin.site.register(KnowledgeCapsule)
admin.site.register(Pricing)
admin.site.register(APIRazor)