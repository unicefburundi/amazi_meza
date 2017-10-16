# -*- coding: utf-8 -*-
from django.contrib import admin
from public_administration_structure_app.models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(Province)
class ProvinceAdmin(ImportExportModelAdmin):
    pass


@admin.register(Commune)
class CommuneAdmin(ImportExportModelAdmin):
    pass


@admin.register(Colline)
class CollineAdmin(ImportExportModelAdmin):
    pass


@admin.register(SousColline)
class SousCollineAdmin(ImportExportModelAdmin):
    pass
