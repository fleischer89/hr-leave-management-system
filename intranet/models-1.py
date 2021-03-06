# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Document(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Document: %s" % self.document.name


# Country
class Country(models.Model):
    class Meta:
        verbose_name_plural = "countries"
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Country: %s" % self.name


# Currency
class Currency(models.Model):
    class Meta:
        verbose_name_plural = "currencies"
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Currency: %s" % self.name


# User Profile
class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    # user = models.OneToOneField(User)
    user = models.OneToOneField(User, null=True, blank=True)
    title = models.CharField(max_length=60, null=True, blank=True)
    username = models.CharField(max_length=60, null=True, blank=True)
    first_name = models.CharField(max_length=60, null=True, blank=True)
    last_name = models.CharField(max_length=60, null=True, blank=True)
    other_names = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, null=True, blank=True)
    marital_status = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_logged_in = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s\t%s" % (self.first_name, self.last_name)


class UserInfo(models.Model):
    class Meta:
        verbose_name_plural = "user information"
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(UserProfile)
    second_phone = models.CharField(max_length=15, null=True, blank=True)
    spouse_name = models.CharField(max_length=50, null=True, blank=True)
    spouse_phone = models.CharField(max_length=15, null=True, blank=True)
    social_security_number = models.CharField(max_length=30, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    ethnicity = models.CharField(max_length=30, null=True, blank=True)
    hometown = models.CharField(max_length=50, null=True, blank=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    postal = models.TextField(null=True, blank=True)
    residential = models.TextField(null=True, blank=True)
    residence_country = models.CharField(max_length=50, null=True, blank=True)
    residence_city = models.CharField(max_length=50, null=True, blank=True)
    day_of_birth = models.CharField(max_length=15, blank=True, null=True)
    place_of_birth = models.TextField(blank=True, null=True)
    interests = models.TextField(null=True, blank=True)
    languages = models.CharField(max_length=150, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s\t%s" % (self.nationality, self.nationality)


# Photograph
class Photograph(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, default=None)
    document = models.FileField(upload_to='photographs')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# Department
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Department: %s" % self.name


# Employee
class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(UserProfile)
    title = models.CharField(max_length=100, blank=True, null=True)
    departments = models.ForeignKey(Department, blank=True, null=True)
    supervisor = models.CharField(max_length=100, null=True, blank=True)
    is_employee = models.BooleanField(default=True)
    is_supervisor = models.BooleanField(default=False)
    office_location = models.CharField(max_length=100, null=True, blank=True)
    office_email = models.CharField(max_length=50, null=True, blank=True)
    office_phone = models.CharField(max_length=15, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s\t%s" % (self.user.first_name, self.user.last_name)


# Next of Kin / Emergency Contact
class EmergencyContact(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    relationship = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    second_phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    residential = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s\t%s" % (self.full_name, self.employee)


# Education
class Education(models.Model):
    class Meta:
        verbose_name_plural = "education"
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, default=None)
    courses = models.CharField(max_length=150, null=True, blank=True)
    qualification = models.CharField(max_length=150, null=True, blank=True)
    institution = models.CharField(max_length=150, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Education: %s: %s, %s, %s" % (self.user, self.qualification, self.courses, self.institution)


# References
class EmployeeReference(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, default=None)
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=30)
    organisation = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Reference: %s: %s, %s" % (self.employee, self.name, self.position)


# Provident Fund Beneficiary
class ProvidentFundBeneficiary(models.Model):
    class Meta:
        verbose_name_plural = "provident fund beneficiaries"
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, default=None)
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    relationship = models.CharField(max_length=50, null=True, blank=True)
    residential = models.TextField(null=True, blank=True)
    percentage = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Provident Fund Beneficiary: %s: %s, %s" % (self.employee, self.full_name, self.percentage)


# Dependent
class Dependent(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, default=None)
    name = models.CharField(max_length=150)
    relationship = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Provident Fund Beneficiary: %s: %s, %s, %s" % (self.employee, self.name, self.relationship, self.age)


# Bank Details
class BankDetail(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee)
    bank_name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    account_number = models.CharField(max_length=30)
    account_name = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.bank_name


# Employee Leave
class EmployeeLeave(models.Model):
    class Meta:
        verbose_name_plural = "employee leave"
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee)
    # category = models.CharField(max_length=100)
    no_of_days_allowed = models.IntegerField()
    no_of_days_taken = models.IntegerField()
    no_of_days_left = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s: Leave days left: %s" % (self.employee, self.no_of_days_left)


# Leave Type
class LeaveType(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.category


# Leave Request
class LeaveRequest(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee)
    type = models.ForeignKey(LeaveType)
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_days = models.IntegerField()
    # account_number = models.CharField(max_length=30)
    reliever = models.CharField(max_length=100, null=True, blank=True)
    hand_over_notes = models.BooleanField(default=False)
    hod_signed = models.BooleanField(default=False)
    hr_signed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    approval_reason = models.TextField(null=True, blank=True)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.employee


# Absence Certification
class AbsenceCertification(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee)
    type = models.ForeignKey(LeaveType)
    # department = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    return_date = models.DateField()
    no_of_days = models.IntegerField()
    reason = models.TextField(null=True, blank=True)
    description_of_symptoms = models.TextField(null=True, blank=True)
    doctor_consulted = models.BooleanField(default=False)
    date_consulted = models.DateField(null=True, blank=True)
    treatment = models.TextField(null=True, blank=True)
    name_of_doctor = models.CharField(max_length=100, null=True, blank=True)
    address_of_doctor = models.TextField(null=True, blank=True)
    declaration = models.BooleanField(default=False)
    employee_signed = models.BooleanField(default=False)
    date = models.DateField()

    manager_name = models.CharField(max_length=100, null=True, blank=True)
    overview_of_absence = models.TextField(null=True, blank=True)
    summary_of_interview = models.TextField(null=True, blank=True)
    recommendations_and_actions = models.TextField(null=True, blank=True)
    sick_pay_entitlement = models.FloatField(null=True, blank=True)
    sick_pay_received = models.FloatField(null=True, blank=True)
    payment_authorized = models.BooleanField(default=False)
    manager_signed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.employee


