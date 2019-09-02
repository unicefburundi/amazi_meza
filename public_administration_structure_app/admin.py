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
    list_display = ('code', 'name', 'get_commune_name', 'get_province_name')

    def get_province_name(self, obj):
        return obj.commune.province.name

    def get_commune_name(self, obj):
        return obj.commune.name

    get_province_name.short_description = "Province"
    get_commune_name.short_description = "Commune"

    list_filter = ('commune__province__name', 'commune__name')


@admin.register(SousColline)
class SousCollineAdmin(ImportExportModelAdmin):
    pass
