from django.contrib import admin
from amazi_meza_app.models import *
from import_export.admin import ImportExportModelAdmin
from leaflet.admin import LeafletGeoAdmin


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



admin.site.register(WaterSourceEndPoint, LeafletGeoAdmin)


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