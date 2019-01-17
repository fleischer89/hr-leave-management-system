# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Document, Photograph, Country, Currency, Employee, UserProfile, UserInfo, ProvidentFundBeneficiary, \
    Department, Dependent, EmergencyContact, EmployeeReference, BankDetail, Education, EmployeeLeave, LeaveType, \
    LeaveRequest, AbsenceCertification


# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'created')
    search_fields = ('id', 'document', 'created')
    list_filter = ('id', 'document', 'created')


class PhotographAdmin(admin.ModelAdmin):
    list_display = ('id', 'document', 'created')
    search_fields = ('id', 'document', 'created')
    list_filter = ('id', 'document', 'created')


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'name', 'symbol', 'created')
    search_fields = ('id', 'country', 'name', 'symbol', 'created')
    list_filter = ('id', 'country', 'name', 'symbol', 'created')


class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'name', 'created')
    search_fields = ('id', 'short_name', 'name', 'created')
    list_filter = ('id', 'short_name', 'name', 'created')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'phone', 'created')
    search_fields = ('id', 'username', 'first_name', 'last_name', 'phone', 'created')
    list_filter = ('id', 'username', 'first_name', 'last_name', 'phone', 'created')


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created')
    search_fields = ('id', 'user', 'created')
    list_filter = ('id', 'user', 'created')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created')
    search_fields = ('id', 'user', 'created')
    list_filter = ('id', 'user', 'created')


class ProvidentFundBeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'full_name', 'relationship', 'created')
    search_fields = ('id', 'employee', 'full_name', 'relationship', 'created')
    list_filter = ('id', 'employee', 'full_name', 'relationship', 'created')


class DependentAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'name', 'relationship', 'created')
    search_fields = ('id', 'employee', 'name', 'relationship', 'created')
    list_filter = ('id', 'employee', 'name', 'relationship', 'created')


class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'full_name', 'relationship', 'phone', 'created')
    search_fields = ('id', 'employee', 'full_name', 'relationship', 'phone', 'created')
    list_filter = ('id', 'employee', 'full_name', 'relationship', 'phone', 'created')


class EmployeeReferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'name', 'position', 'created')
    search_fields = ('id', 'employee', 'name', 'position', 'created')
    list_filter = ('id', 'employee', 'name', 'position', 'created')


class EducationAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'courses', 'qualification', 'institution', 'year', 'month', 'day', 'created')
    search_fields = ('id', 'employee', 'courses', 'qualification', 'institution', 'year', 'month', 'day', 'created')
    list_filter = ('id', 'employee', 'courses', 'qualification', 'institution', 'year', 'month', 'day', 'created')


class EmployeeLeaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'no_of_days_allowed', 'no_of_days_taken', 'no_of_days_left', 'updated')
    search_fields = ('id', 'employee', 'no_of_days_allowed', 'no_of_days_taken', 'no_of_days_left', 'updated')
    list_filter = ('id', 'employee', 'no_of_days_allowed', 'no_of_days_taken', 'no_of_days_left', 'updated')


class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'start_date', 'end_date', 'no_of_days', 'approved', 'updated')
    search_fields = ('id', 'employee', 'start_date', 'end_date', 'no_of_days', 'approved', 'updated')
    list_filter = ('id', 'employee', 'start_date', 'end_date', 'no_of_days', 'approved', 'updated')


class AbsenceCertificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'start_date', 'end_date', 'manager_name', 'manager_signed', 'updated')
    search_fields = ('id', 'employee', 'start_date', 'end_date', 'manager_name', 'manager_signed', 'updated')
    list_filter = ('id', 'employee', 'start_date', 'end_date', 'manager_name', 'manager_signed', 'updated')


class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'updated')
    search_fields = ('id', 'category', 'updated')
    list_filter = ('id', 'category', 'updated')


class BankDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'bank_name', 'branch', 'account_number', 'created')
    search_fields = ('id', 'employee', 'bank_name', 'branch', 'account_number', 'created')
    list_filter = ('id', 'employee', 'bank_name', 'branch', 'account_number', 'created')


# Department
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created')
    search_fields = ('id', 'name', 'created')
    list_filter = ('id', 'name', 'created')


admin.site.site_header = 'Barbex Technical Services Limited'
admin.site.site_title = 'Barbex Technical Services Limited'
admin.site.index_title = 'Database Models'
# admin.site.index_template = 'Database Models'


admin.site.register(AbsenceCertification, AbsenceCertificationAdmin)
admin.site.register(BankDetail, BankDetailAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Dependent, DependentAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(EmergencyContact, EmergencyContactAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeReference, EmployeeReferenceAdmin)
admin.site.register(EmployeeLeave, EmployeeLeaveAdmin)
admin.site.register(LeaveType, LeaveTypeAdmin)
admin.site.register(LeaveRequest, LeaveRequestAdmin)
admin.site.register(Photograph, PhotographAdmin)
admin.site.register(ProvidentFundBeneficiary, ProvidentFundBeneficiaryAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

