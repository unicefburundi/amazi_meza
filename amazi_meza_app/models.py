from __future__ import unicode_literals

from django.db import models
from public_administration_structure_app.models import *


class LocalLevelReporter(models.Model):
    ''' In this model will be stored reporters who reports from collines '''
    reporter_phone_number = models.CharField(max_length=20)
    reporter_name = models.CharField(max_length=50)
    date_registered = models.DateTimeField(auto_now_add=True)
    colline = models.ForeignKey(Colline)

    def __unicode__(self):
        return "{0} - {1}".format(self.reporter_name, self.reporter_phone_number)


class TemporaryLocalLevelReporter(models.Model):
    ''' This model will be used to temporary store colline level Reporter who doesn't finish his self registration '''
    reporter_phone_number = models.CharField(max_length=20)
    reporter_name = models.CharField(max_length=50)
    date_registered = models.DateTimeField(auto_now_add=True)
    colline = models.ForeignKey(Colline)

    def __unicode__(self):
        return "{0} - {1}".format(self.reporter_name, self.reporter_phone_number)


class NumberOfWaterPointCommittee(models.Model):
    ''' In this model will be stored reports (from communes)
    about number of water points committees '''
    commune = models.ForeignKey(Commune)
    number_of_water_point_committees = models.IntegerField()
    reporting_year = models.IntegerField()
    reporting_month = models.IntegerField()
    reception_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0} - {1} - {2} - {3}".format(self.commune, self.reporting_month, self.reporting_year, self.number_of_water_point_committees)


class NumberOfHouseHold(models.Model):
    ''' In this model will be stored reports (from communes) 
    about number of households and number of vulnerable households '''
    commune = models.ForeignKey(Commune)
    number_of_house_holds = models.IntegerField()
    number_of_vulnerable_house_holds = models.IntegerField()
    reporting_year = models.IntegerField()
    reporting_month = models.IntegerField()
    reception_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0} - {1} - {2} - {3} - {4}".format(self.commune, self.reporting_month, self.reporting_year, self.number_of_house_holds, self.number_of_vulnerable_house_holds)


class WaterNetworkProblemType(models.Model):
    ''' In this model will be stored names of water networks problems types '''
    water_network_problem_type_name = models.CharField(max_length=100)
    water_network_problem_code = models.CharField(max_length=10)

    def __unicode__(self):
        return "{0} code {1}".format(self.water_network_problem_type_name, self.water_network_problem_code)


class NumberOfWaterNetworkProblems(models.Model):
    ''' In this model will be stored reports (from communes)
    about water network problems '''
    commune = models.ForeignKey(Commune)
    most_frequent_water_network_problem_type = models.ForeignKey(WaterNetworkProblemType)
    number_of_water_network_problems = models.IntegerField()
    number_of_days = models.IntegerField()
    reporting_year = models.IntegerField()
    reporting_month = models.IntegerField()
    reception_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0} - {1} - {2} - {3} - {4}".format(self.commune, self.reporting_month, self.reporting_year, self.most_frequent_water_network_problem_type, self.number_of_water_network_problems)


class MonthlyIncome(models.Model):
    ''' In this model will be stored reports (from communes)
    about incomes '''
    commune = models.ForeignKey(Commune)
    total_income = models.IntegerField()
    reporting_year = models.IntegerField()
    reporting_month = models.IntegerField()
    reception_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0} - {1} - {2} - {3}".format(self.commune, self.reporting_month, self.reporting_year, self.total_income)


class ExpenditureCategory(models.Model):
    ''' In this model will be stored categories of expenditures '''
    expenditure_category_name = models.CharField(max_length=100)
    priority = models.IntegerField(default=1, help_text="La plus petite valeur est 1")

    def __unicode__(self):
        return "{0} Priorite {1}".format(self.expenditure_category_name, self.priority)


class MonthlyExpenditure(models.Model):
    ''' In this model will be stored reports (from communes)
    about expenditures '''
    commune = models.ForeignKey(Commune)
    expenditure = models.ForeignKey(ExpenditureCategory)
    expenditure_amount = models.IntegerField()
    reporting_year = models.IntegerField()
    reporting_month = models.IntegerField()
    reception_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0} - {1} - {2} - {3} - {4}".format(self.commune, self.reporting_month, self.reporting_year, self.expenditure, self.expenditure_amount)


class ExpectedBudgetExpenditureAndAnnualBudget(models.Model):
    ''' In this model will be stored reports (from communes) 
    about expected annual expenditure and annual budget '''
    commune = models.ForeignKey(Commune)
    annual_badget = models.IntegerField(null=True)
    expected_annual_expenditure = models.IntegerField(null=True)
    reporting_year = models.IntegerField()
    reception_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0} - {1} - {2} - {3}".format(self.commune, self.reporting_year, self.annual_badget, self.expected_annual_expenditure)


class WaterPointProblemTypes(models.Model):
    ''' In this model will be stored water points problem types '''
    problem_type_name = models.CharField(max_length=50)
    problem_type_description = models.CharField(max_length=50, default='')

    def __unicode__(self):
        return "{0}".format(self.problem_type_name)


class WaterPointType(models.Model):
    ''' In this model will be stored water point types '''
    name = models.CharField(max_length=50)
    priority = models.IntegerField(default=1, help_text="La plus petite valeur est 1")

    def __unicode__(self):
        return "{0}; priorite : {1}".format(self.name, self.priority)


class NumberOfWaterSourceEndPoint(models.Model):
    ''' In this model will be recorded reports (from communes)
    about water source end points '''
    commune = models.ForeignKey(Commune)
    water_point_type = models.ForeignKey(WaterPointType)
    existing_number = models.IntegerField(null=True)
    additional_number = models.IntegerField(null=True)
    functional_number = models.IntegerField(null=True)
    reporting_year = models.IntegerField()
    reporting_month = models.IntegerField()
    reception_date = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(max_length=50)

    def __unicode__(self):
        return "{0} - {1} - {2} - {3} - {4} - {5} - {6}".format(self.commune, self.reporting_month, self.reporting_year, self.water_point_type, self.existing_number, self.additional_number, self.functional_number)


class CommuneLevelReporters(models.Model):
    ''' In this model will be recorded commune level Reporters '''
    commune = models.ForeignKey(Commune)
    reporter_phone_number = models.CharField(max_length=20)
    reporter_name = models.CharField(max_length=100)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0} - {1} - {2}".format(self.commune, self.reporter_phone_number, self.reporter_name)


class TemporaryCommuneLevelReporters(models.Model):
    ''' This model will be used to temporary store commune level Reporter who doesn't finish his self registration '''
    commune = models.ForeignKey(Commune)
    reporter_phone_number = models.CharField(max_length=20)
    reporter_name = models.CharField(max_length=100)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0} - {1} - {2}".format(self.commune, self.reporter_phone_number, self.reporter_name)


class WaterNetWork(models.Model):
    ''' In this model will be stored water networks '''
    commune = models.ForeignKey(Commune)
    water_network_name = models.CharField(max_length=50)
    reporter = models.ForeignKey(CommuneLevelReporters)
    date_registered = models.DateTimeField(auto_now_add=True)
    length_of_network = models.IntegerField()
    water_network_code = models.CharField(max_length=10)

    def __unicode__(self):
        return "Commune : {0}; Name : {1}; length : {2}; Registered : {3}; Registered by : {4}; Code : {5}".format(self.commune, self.water_network_name, self.length_of_network, self.date_registered, self.reporter, self.water_network_code)


class WaterSourceEndPoint(models.Model):
    ''' In this model will be stored water source end points '''
    water_point_name = models.CharField(max_length=50)
    water_point_type = models.ForeignKey(WaterPointType)
    colline = models.ForeignKey(Colline)
    network = models.ForeignKey(WaterNetWork)
    reporter = models.ForeignKey(LocalLevelReporter)
    date_registered = models.DateTimeField(auto_now_add=True)
    number_of_households = models.IntegerField(default=0)
    number_of_vulnerable_households = models.IntegerField(default=0)
    water_point_functional = models.BooleanField(default=True)

    def __unicode__(self):
        return "{0} - {1} - {2} - {3} - {4} - {5}".format(self.water_point_name, self.water_point_type, self.colline, self.network, self.reporter, self.date_registered)


class ActionsForWaterPointProblem(models.Model):
    ''' In this model will be stored possible actions for water point
    problems '''
    action_code = models.CharField(max_length=10)
    action_description = models.CharField(max_length=500)

    def __unicode__(self):
        return "{0} - {1}".format(self.action_code, self.action_description)


class WaterPointProblem(models.Model):
    ''' In this model will be stored reported water point problems '''
    water_point = models.ForeignKey(WaterSourceEndPoint)
    problem = models.ForeignKey(WaterPointProblemTypes)
    action_taken = models.ForeignKey(ActionsForWaterPointProblem)
    days = models.IntegerField()
    problem_solved = models.BooleanField(default=False)
    case_of_diarrhea = models.BooleanField(default=False)
    report_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0} - {1} - {2} - {3} - {4} - {5}".format(self.water_point, self.problem, self.days, self.action_taken, self.problem_solved, self.report_date)
