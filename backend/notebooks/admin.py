from django.contrib import admin
from .models import Notebook, Document, Chunk

admin.site.register(Notebook)
admin.site.register(Document)
admin.site.register(Chunk)

# Register your models here.
