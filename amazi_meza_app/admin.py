from django.contrib import admin
from amazi_meza_app.models import *
from import_export.admin import ImportExportModelAdmin
from leaflet.admin import LeafletGeoAdmin

from django.contrib.gis.admin import OSMGeoAdmin
from import_export.admin import ImportExportModelAdmin


@admin.register(LocalLevelReporter)
class LocalLevelReporterAdmin(ImportExportModelAdmin):
    pass


@admin.register(NumberOfWaterPointCommittee)
class NumberOfWaterPointCommitteeAdmin(ImportExportModelAdmin):
    pass


@admin.register(NumberOfHouseHold)
class NumberOfHouseHoldAdmin(ImportExportModelAdmin):
    pass


@admin.register(WaterNetworkProblemType)
class WaterNetworkProblemTypeAdmin(ImportExportModelAdmin):
    pass


@admin.register(NumberOfWaterNetworkProblems)
class NumberOfWaterNetworkProblemsAdmin(ImportExportModelAdmin):
    pass


@admin.register(MonthlyIncome)
class MonthlyIncomeAdmin(ImportExportModelAdmin):
    pass


@admin.register(ExpenditureCategory)
class ExpenditureCategoryAdmin(ImportExportModelAdmin):
    pass


@admin.register(MonthlyExpenditure)
class MonthlyExpenditureAdmin(ImportExportModelAdmin):
    pass


@admin.register(ExpectedBudgetExpenditureAndAnnualBudget)
class TemporaryAdmin(ImportExportModelAdmin):
    pass


@admin.register(WaterPointProblemTypes)
class ExpectedBudgetExpenditureAndAnnualBudgetAdmin(ImportExportModelAdmin):
    pass


@admin.register(WaterPointType)
class WaterPointTypeAdmin(ImportExportModelAdmin):
    pass


@admin.register(NumberOfWaterSourceEndPoint)
class NumberOfWaterSourceEndPointAdmin(ImportExportModelAdmin):
    pass


@admin.register(CommuneLevelReporters)
class CommuneLevelReportersAdmin(ImportExportModelAdmin):
    pass


@admin.register(WaterNetWork)
class WaterNetWorkAdmin(ImportExportModelAdmin):
    pass


@admin.register(WaterSourceEndPoint)
class WaterSourceEndPointAdmin(OSMGeoAdmin, ImportExportModelAdmin):
    list_display = ('water_point_name', 'water_point_type', 'get_location', 'get_commune_name', 'get_province_name')

    def get_location(self, obj):
        lat_long = obj.geom['coordinates']
        return lat_long

    def get_province_name(self, obj):
        return obj.colline.commune.province.name

    def get_commune_name(self, obj):
        return obj.colline.commune.name

    get_location.short_description = "Location"
    get_province_name.short_description = "Province"
    get_commune_name.short_description = "Commune"

    list_filter = ('colline__commune__province__name', 'colline__commune__name', 'water_point_type')


@admin.register(ActionsForWaterPointProblem)
class ActionsForWaterPointProblemAdmin(ImportExportModelAdmin):
    pass


@admin.register(WaterPointProblemResolver)
class WaterPointProblemResolverAdmin(ImportExportModelAdmin):
    pass

@admin.register(WaterPointProblem)
class WaterPointProblemAdmin(ImportExportModelAdmin):
    pass


@admin.register(TemporaryLocalLevelReporter)
class TemporaryLocalLevelReporterAdmin(ImportExportModelAdmin):
    pass


@admin.register(TemporaryCommuneLevelReporters)
class TemporaryCommuneLevelReportersAdmin(ImportExportModelAdmin):
    pass


@admin.register(TimeMeasuringUnit)
class TimeMeasuringUnitAdmin(ImportExportModelAdmin):
    pass


@admin.register(Setting)
class SettingAdmin(ImportExportModelAdmin):
    pass