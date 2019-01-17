# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import loader, Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.db.models import Count
from django.contrib.sessions.models import Session
from models import *
from intranet import *
from sendsms import api
from sendsms.message import SmsMessage
from datetime import *
from helpers import *
from api import *
import re
# from intranet.forms import UploadPhotographForm
# from intranet.templatetags.website_extras import *


# Create your views here.
@login_required
def index(request, user_id):
    photo = None
    if user_id is None:
        return HttpResponseRedirect("/panel/login/")
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    leave_requests = LeaveRequest.objects.filter(employee=employee)
    photo = get_photo(user)
    offerings = []
    sales = []
    tithes = []
    attendance = []
    ministries = []
    departments = Department.objects.all()
    employees = []
    assets = []
    testaments = []
    businesses = []
    maintenance = []
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)
    print(photo)
    data = {'request': request, 'user': user, 'photo': photo, 'attendance': attendance, 'testaments': testaments,
            'tithes': tithes, 'businesses': businesses, 'assets': assets, 'ministries': ministries,
            'maintenance': maintenance, 'departments': departments, 'sales': sales, 'offerings': offerings,
            'employees': employees, 'employee': employee, 'leave_requests': leave_requests,
            'show_profiles': show_profiles, 'show_approvals': show_approvals}
    # return render_to_response('panel/index.html', data, context_instance=Requestdict(request))
    # return render_to_response('panel/index.html', data)
    return render_to_response('panel/employee/leave_requests.html', data)
    # count = [i for i in range(10)]
    # data = dict(count=count)
    # return render_to_response('index.html', data)


def handler400(request, *args, **argv):
    response = render(request, 'panel/includes/404.html', {})
    response.status_code = 404
    return response


def handler403(request, *args, **argv):
    response = render(request, 'panel/includes/404.html', {})
    response.status_code = 404
    return response


def handler404(request, *args, **argv):
    response = render(request, 'panel/includes/404.html', {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, 'panel/includes/404.html', {})
    response.status_code = 500
    return response


@login_required
@csrf_exempt
def admin_departments(request, user_id, department_id):
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    departments = Department.objects.all()
    photo = get_photo(user)
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)
    return render_to_response('panel/profiles/departments.html',
                              {'request': request, 'user': user, 'photo': photo, 'employee': employee,
                               'departments': departments, 'show_profiles': show_profiles,
                               'show_approvals': show_approvals})


def add_education_record(education, employee, programme, qualification, institution, start_date, end_date, short_course,
                         present):
    # months = [m.lower() for m in get_months()]
    # if month.lower().strip() in months:
    #     print month
    #     for i in range(0, len(months) - 1):
    #         if month.lower().strip() == months[i].lower():
    #             print months[i]
    #             month = i + 1
    # print "month: ", month
    # month = 6
    short_course = short_course if short_course is not None else False
    present = present if present is not None else False
    education_record = \
        Education.objects.create(employee=employee, courses=programme, qualification=qualification,
                                 institution=institution, start_date=start_date, end_date=end_date,
                                 short_course=short_course, present=present)
    if education_record is not None:
        education.append(education_record)
    return education


def add_beneficiary_record(beneficiaries, employee, name, dob, phone, email, relationship, residential, percentage):
    beneficiary_record = \
        ProvidentFundBeneficiary.objects.create(employee=employee, full_name=name, date_of_birth=dob, phone=phone,
                                                email=email, relationship=relationship, residential=residential,
                                                percentage=percentage)
    if beneficiary_record is not None:
        beneficiaries.append(beneficiary_record)
    return beneficiaries


def add_dependent_record(dependents, employee, name, relationship, dob, age, photo):
    dependent_record = \
        Dependant.objects.create(employee=employee, name=name, relationship=relationship, date_of_birth=dob, age=age,
                                 photo=photo)
    dependent_record.save()
    if dependent_record is not None:
        dependents.append(dependent_record)
        # dep_photo = DependantPhoto.objects.create(dependent=dependent_record, photo=photo)
        # dep_photo.save()
    return dependents


def add_reference_record(references, employee, name, type, organization, position, phone, email, address):
    reference_record = \
        EmployeeReference.objects.create(employee=employee, name=name, organisation=organization, position=position,
                                         phone=phone, email=email, address=address, type=type)
    if reference_record is not None:
        references.append(reference_record)
    return references


def calculate_age(date_of_birth):
    today = date.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


@login_required
def admin_employees(request, user_id, employee_id):
    employees = Employee.objects.all()
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    count = len(employees)
    photo = get_photo(user)

    if employee_id is not None:
        single_employee = Employee.objects.get(pk=employee_id)
        employee_education = None
        employee_info = None
        dependants = None
        if single_employee.user is not None:
            employee_info = UserInfo.objects.filter(user=single_employee.user)
            # employee_employments = Employment.objects.filter(user=employee_profile)
            employee_education = Education.objects.filter(employee=single_employee)
            dependants = Dependant.objects.filter(employee=single_employee)
        emergency_contacts = EmergencyContact.objects.filter(employee=single_employee)
        beneficiaries = ProvidentFundBeneficiary.objects.filter(employee=single_employee)
        references = EmployeeReference.objects.filter(employee=single_employee)
        # employees = get_assets_data(employee_id, None, False, False)
        employees = get_assets_data(None, None, False, False)
        employee_photo = Photograph.objects.filter(user=single_employee.user) \
            if single_employee.user is not None else None
        # recent_employees = get_assets_data(None, get_past_date(7), True, False)

        employee_education = employee_education if employee_education is not None else None
        employee_info = employee_info[0] if employee_info is not None and len(employee_info) > 0 else None
        employee_photo = employee_photo[0] if employee_photo is not None and len(employee_photo) > 0 else None
        emergency_contacts = emergency_contacts[0] if emergency_contacts is not None and len(emergency_contacts) > 0 else None
        dependants = dependants if dependants is not None else None
        show_profiles = display_profiles(employee)
        show_approvals = display_approvals(employee)
        t = loader.get_template('panel/profiles/employee.html')
        c = dict({'user': user, 'single_employee': single_employee, 'employees': employees, 'photo': photo,
                  'employee': employee, 'employee_profile': single_employee.user, 'employee_photo': employee_photo,
                  'employee_info': employee_info, 'dependants': dependants, 'employee_education': employee_education,
                  'emergency_contacts': emergency_contacts, 'beneficiaries': beneficiaries, 'references': references,
                  'show_profiles': show_profiles, 'show_approvals': show_approvals})
        return HttpResponse(t.render(c))
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)

    # t = loader.get_template('panel/index.html')
    # c = dict({'user': user, 'employees': employees, 'employee': employee, 'photo': photo})
    return render_to_response('panel/profiles/employees.html',
                              {'user': user, 'employees': employees, 'employee': employee, 'count': count,
                               'photo': photo, 'show_profiles': show_profiles, 'show_approvals': show_approvals})


@login_required
def admin_employees_registered(request, user_id, employee_id):
    employees = Employee.objects.all()
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    count = len(employees)
    photo = get_photo(user)
    created_employee = Employee.objects.get(pk=employee_id)

    registered = True
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)

    return render_to_response('panel/employee/employee_registered.html',
                              {'user': user, 'employees': employees, 'employee': employee, 'count': count,
                               'photo': photo, 'registered': registered, 'created_employee': created_employee,
                               'default_password': '%s' % RANDOM_PASSWORD, 'show_profiles': show_profiles,
                               'show_approvals': show_approvals})


@login_required
@csrf_exempt
def admin_delete_employee(request, user_id, employee_id):
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    employees = Employee.objects.all()
    count = len(employees)
    photo = get_photo(user)
    deleted_employee = False
    default_password = '%s' % RANDOM_PASSWORD
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)

    if request.method == 'POST':
        delete_employee = request.POST['delete_employee'] if 'delete_employee' in request.POST.keys() else None
        if employee_id is not None:
            emp = Employee.objects.get(pk=employee_id)
            if emp is not None and delete_employee == 'Delete':
                bank_details = BankDetail.objects.filter(employee=emp).delete()
                EmployeeLeave.objects.filter(employee=emp).delete()
                LeaveRequest.objects.filter(employee=emp).delete()
                Photograph.objects.filter(user=emp.user).delete()
                Dependant.objects.filter(employee=emp).delete()
                ProvidentFundBeneficiary.objects.filter(employee=emp).delete()
                Education.objects.filter(employee=emp).delete()
                EmergencyContact.objects.filter(employee=emp).delete()
                EmployeeReference.objects.filter(employee=emp).delete()
                UserInfo.objects.filter(user=emp.user).delete()
                emp_name = "%s\t%s" % (emp.user.first_name, emp.user.last_name)
                emp_user_id = emp.user.id
                emp.delete()
                UserProfile.objects.filter(id=emp_user_id).delete()
                deleted_employee = True
                return HttpResponseRedirect("/panel/%s/employees/" % user.id)
                # return render_to_response('panel/profiles/employees.html',
                #                   {'user': user, 'employees': employees, 'employee': employee, 'count': count,
                #                    'photo': photo, 'deleted': deleted_employee, 'deleted_employee': deleted_employee,
                #                    'default_password': default_password, 'emp_name': emp_name,
                #                    'show_profiles': show_profiles, 'show_approvals': show_approvals})

    registered = True
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)

    return render_to_response('panel/profiles/employees.html',
                              {'user': user, 'employees': employees, 'employee': employee, 'count': count,
                               'photo': photo, 'registered': registered, 'deleted_employee': deleted_employee,
                               'default_password': default_password, 'show_profiles': show_profiles,
                               'show_approvals': show_approvals})


@login_required
@csrf_exempt
def admin_new_employee(request, user_id):
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)
    if request.method == 'POST':
        # spiritual_name = request.POST['spiritual_name'] if 'spiritual_name' in request.POST.keys() else None
        employee_photo = request.FILES['employee_photo'] if 'employee_photo' in request.FILES.keys() else None
        first_name = request.POST['first_name'] if 'first_name' in request.POST.keys() else None
        last_name = request.POST['last_name'] if 'last_name' in request.POST.keys() else None
        other_names = request.POST['other_names'] if 'other_names' in request.POST.keys() else None
        dob = request.POST['dob_date'] if 'dob_date' in request.POST.keys() else None
        gender = request.POST['gender'] if 'gender' in request.POST.keys() else None
        marital_status = request.POST['marital_status'] if 'marital_status' in request.POST.keys() else None
        phone = request.POST['phone'] if 'phone' in request.POST.keys() else None
        email = request.POST['email'] if 'email' in request.POST.keys() else None

        second_phone = request.POST['second_phone'] if 'second_phone' in request.POST.keys() else None
        second_email = request.POST['second_email'] if 'second_email' in request.POST.keys() else None
        nationality = request.POST['nationality'] if 'nationality' in request.POST.keys() else None
        ethnicity = request.POST['ethnicity'] if 'ethnicity' in request.POST.keys() else None
        hometown = request.POST['hometown'] if 'hometown' in request.POST.keys() else None
        region = request.POST['region'] if 'region' in request.POST.keys() else None
        postal = request.POST['postal'] if 'postal' in request.POST.keys() else None
        residential = request.POST['residential'] if 'residential' in request.POST.keys() else None
        residence_country = request.POST['residence_country'] if 'residence_country' in request.POST.keys() else None
        residence_city = request.POST['residence_city'] if 'residence_city' in request.POST.keys() else None
        day_of_birth = request.POST['day_of_birth'] if 'day_of_birth' in request.POST.keys() else None
        place_of_birth = request.POST['place_of_birth'] if 'place_of_birth' in request.POST.keys() else None
        interests = request.POST['interests'] if 'interests' in request.POST.keys() else None
        spouse_name = request.POST['spouse_name'] if 'spouse_name' in request.POST.keys() else None
        spouse_phone = request.POST['spouse_phone'] if 'spouse_phone' in request.POST.keys() else None
        social_security_number = request.POST['social_security_no'] if 'social_security_no' in request.POST.keys() else None

        leave_days_allowed = request.POST['leave_days_allowed'] if 'leave_days_allowed' in request.POST.keys() else None

        bank_name = request.POST['bank_name'] if 'bank_name' in request.POST.keys() else None
        bank_branch = request.POST['bank_branch'] if 'bank_branch' in request.POST.keys() else None
        bank_account_name = request.POST['bank_account_name'] if 'bank_account_name' in request.POST.keys() else None
        bank_account_number = request.POST['bank_account_number'] if 'bank_account_number' in request.POST.keys() else None

        emergency_contact_name = request.POST['emergency_contact_name'] if 'emergency_contact_name' in request.POST.keys() else None
        emergency_contact_relationship = request.POST['emergency_contact_relationship'] if 'emergency_contact_relationship' in request.POST.keys() else None
        emergency_contact_phone = request.POST['emergency_contact_phone'] if 'emergency_contact_phone' in request.POST.keys() else None
        emergency_contact_phone_2 = request.POST['emergency_contact_phone_2'] if 'emergency_contact_phone_2' in request.POST.keys() else None
        emergency_contact_email = request.POST['emergency_contact_email'] if 'emergency_contact_email' in request.POST.keys() else None
        emergency_contact_address = request.POST['emergency_contact_address'] if 'emergency_contact_address' in request.POST.keys() else None

        languages = request.POST['languages'] if 'languages' in request.POST.keys() else None

        department_id = request.POST['department_id'] if 'department_id' in request.POST.keys() else None
        # is_member = request.POST['is_member'] if '' in request.POST.keys() else None
        is_employee = True
        is_supervisor = False  # request.POST['is_coordinator']
        is_coordinator = False  # request.POST['is_coordinator']
        is_leadership = False  # request.POST['is_leadership']

        username = "%s.%s" % (first_name.lower(), last_name.lower())
        # password = User.objects.make_random_password()
        password = RANDOM_PASSWORD
        new_user = User.objects.create_user(username=username, email=email, password=password, is_staff=True)

        department = Department.objects.filter(pk=department_id) if int(department_id) is not None else None
        if new_user is not None:
            user_profile = \
                UserProfile.objects.create(user=new_user, first_name=first_name, last_name=last_name, dob=dob,
                                           other_names=other_names, gender=gender, marital_status=marital_status,
                                           phone=phone, email=email, is_logged_in=False)

            if user_profile is not None:
                user_info = \
                    UserInfo.objects.create(user=user_profile, nationality=nationality, ethnicity=ethnicity,
                                            region=region, hometown=hometown, postal=postal, residential=residential,
                                            residence_city=residence_city, day_of_birth=day_of_birth,
                                            residence_country=residence_country, place_of_birth=place_of_birth,
                                            interests=interests, languages=languages, second_phone=second_phone,
                                            spouse_phone=spouse_phone, spouse_name=spouse_name,
                                            social_security_number=social_security_number)
                user_info.save()
                employee = Employee.objects.create(user=user_profile, is_employee=is_employee, is_supervisor=is_supervisor)
                if len(department) > 0:
                    employee.department = department[0]
                employee.save()
                if employee is not None:
                    if employee_photo is not None:
                        emp_photo = Photograph.objects.create(user=user_profile, document=employee_photo)
                        emp_photo.save()
                    #  EMERGENCY CONTACT
                    emergency_contact = \
                        EmergencyContact.objects.create(employee=employee, full_name=emergency_contact_name,
                                                        relationship=emergency_contact_relationship,
                                                        phone=emergency_contact_phone, second_phone=emergency_contact_phone_2,
                                                        email=emergency_contact_email, residential=emergency_contact_address)
                    emergency_contact.save()

                    #  BANK DETAILS
                    bank_detail = \
                        BankDetail.objects.create(employee=employee, bank_name=bank_name, branch=bank_branch,
                                                  account_name=bank_account_name, account_number=bank_account_number)
                    bank_detail.save()

                    #  BANK DETAILS
                    leave_days_allowed = 0 if len(leave_days_allowed) == 0 or leave_days_allowed is None else leave_days_allowed
                    employee_leave = \
                        EmployeeLeave.objects.create(employee=employee, no_of_days_allowed=int(leave_days_allowed),
                                                     no_of_days_taken=0, no_of_days_left=int(leave_days_allowed))
                    employee_leave.save()

                    #  EMPLOYMENT RECORDS
                    employment_records = list()
                    # for i in range(1, 5):
                    #     keys = ['employment_company_', 'employment_position_', 'employment_date_', 'resignation_date_',
                    #             'company_description_', 'employment_current_']
                    #     employment_company = request.POST[keys[0] + str(i)] if keys[0] + str(i) in request.POST.keys() else ""
                    #     employment_position = request.POST[keys[1] + str(i)] if keys[1] + str(i) in request.POST.keys() else None
                    #     employment_date = request.POST[keys[2] + str(i)] if keys[2] + str(i) in request.POST.keys() else None
                    #     resignation_date = request.POST[keys[3] + str(i)] if keys[3] + str(i) in request.POST.keys() else None
                    #     company_description = request.POST[keys[4] + str(i)] if keys[4] + str(i) in request.POST.keys() else ""
                    #     employment_current = request.POST[keys[5] + str(i)] if keys[5] + str(i) in request.POST.keys() else False
                    #
                    #     if (employment_company is not None) and len(employment_company) > 0:
                    #         employment_records = add_employment_record(employment_records, user_profile, employment_position,
                    #                                                    employment_date, resignation_date, employment_company,
                    #                                                    company_description, employment_current)

                    # EDUCATION RECORDS
                    education_records = list()
                    for i in range(1, 5):
                        keys = ['programme_', 'qualification_', 'institution_', 'education_start_date_',
                                'education_end_date_', 'short_course_', 'education_present_']
                        programme = request.POST[keys[0] + str(i)] if keys[0] + str(i) in request.POST.keys() else None
                        qualification = request.POST[keys[1] + str(i)] if keys[1] + str(i) in request.POST.keys() else None
                        institution = request.POST[keys[2] + str(i)] if keys[2] + str(i) in request.POST.keys() else None
                        start_date = request.POST[keys[3] + str(i)] if keys[3] + str(i) in request.POST.keys() else None
                        end_date = request.POST[keys[4] + str(i)] if keys[4] + str(i) in request.POST.keys() else None
                        short_course = request.POST[keys[5] + str(i)] if keys[5] + str(i) in request.POST.keys() else None
                        education_present = request.POST[keys[6] + str(i)] if keys[6] + str(i) in request.POST.keys() else False

                        if (programme is not None) and len(programme) > 0:
                            education_records = add_education_record(education_records, employee, programme,
                                                                     qualification, institution, start_date, end_date,
                                                                     short_course, education_present)

                    # PROVIDENT FUND BENEFICIARIES
                    beneficiary_records = list()
                    for i in range(1, 5):
                        keys = ['beneficiary_name_', 'beneficiary_dob_', 'beneficiary_phone_', 'beneficiary_email_',
                                'beneficiary_address_', 'beneficiary_relationship_', 'beneficiary_percentage_']
                        name = request.POST[keys[0] + str(i)] if keys[0] + str(i) in request.POST.keys() else None
                        dob = request.POST[keys[1] + str(i)] if keys[1] + str(i) in request.POST.keys() else None
                        phone = request.POST[keys[2] + str(i)] if keys[2] + str(i) in request.POST.keys() else None
                        email = request.POST[keys[3] + str(i)] if keys[3] + str(i) in request.POST.keys() else None
                        residential = request.POST[keys[4] + str(i)] if keys[4] + str(i) in request.POST.keys() else None
                        relationship = request.POST[keys[5] + str(i)] if keys[5] + str(i) in request.POST.keys() else None
                        percentage = request.POST[keys[6] + str(i)] if keys[6] + str(i) in request.POST.keys() else False

                        if (name is not None) and len(name) > 0:
                            dob = dob if (re.compile("\d{0,4}-\d{0,2}-\d{0,2}")).match(dob) else None
                            beneficiary_records = add_beneficiary_record(beneficiary_records, employee, name, dob, phone,
                                                                         email, relationship, residential, percentage)

                    # DEPENDENTS
                    dependents = list()
                    for i in range(1, 5):
                        keys = ['dependent_name_', 'dependent_dob_', 'dependent_relationship_', 'dependent_age_',
                                'dependent_photo_']
                        name = request.POST[keys[0] + str(i)] if keys[0] + str(i) in request.POST.keys() else None
                        dob = request.POST[keys[1] + str(i)] if keys[1] + str(i) in request.POST.keys() else None
                        relationship = request.POST[keys[2] + str(i)] if keys[2] + str(i) in request.POST.keys() else None
                        age = request.POST[keys[3] + str(i)] if keys[3] + str(i) in request.POST.keys() else False
                        dep_photo = request.FILES[keys[4] + str(i)] if keys[4] + str(i) in request.FILES.keys() else None

                        if (name is not None) and len(name) > 0:
                            if (dob is not None) and len(dob) > 0:
                                dob = dob if (re.compile("\d{0,4}-\d{0,2}-\d{0,2}")).match(dob) else None
                                birth_date = datetime.strptime(dob, DATE_FORMAT)
                                age = calculate_age(birth_date)
                            dependents = add_dependent_record(dependents, employee, name, relationship, dob, age,
                                                              dep_photo)

                    # EMPLOYEE REFERENCES
                    references = list()
                    for i in range(1, 5):
                        keys = ['reference_name_', 'reference_type_', 'reference_organization_', 'reference_position_',
                                'reference_phone_', 'reference_email_', 'reference_address_']
                        name = request.POST[keys[0] + str(i)] if keys[0] + str(i) in request.POST.keys() else None
                        type = request.POST[keys[1] + str(i)] if keys[1] + str(i) in request.POST.keys() else None
                        organization = request.POST[keys[2] + str(i)] if keys[2] + str(i) in request.POST.keys() else None
                        position = request.POST[keys[3] + str(i)] if keys[3] + str(i) in request.POST.keys() else ''
                        phone = request.POST[keys[4] + str(i)] if keys[4] + str(i) in request.POST.keys() else ''
                        email = request.POST[keys[5] + str(i)] if keys[5] + str(i) in request.POST.keys() else ''
                        address = request.POST[keys[6] + str(i)] if keys[6] + str(i) in request.POST.keys() else ''

                        if (name is not None) and len(name) > 0:
                            references = add_reference_record(references, employee, name, type, organization, position,
                                                              phone, email, address)

            return HttpResponseRedirect("/panel/%s/employee_registered/%s" % (user.id, employee.id))
    user = UserProfile.objects.get(pk=user_id)
    photo = get_photo(user)
    relatives_count = [1, 2, 3, 4, 5, 6, 7]
    education_count = [1, 2, 3, 4]
    dependent_count = [1, 2, 3, 4]
    beneficiary_count = [1, 2, 3]
    reference_count = [1, 2, 3]
    employees = Employee.objects.all()
    departments = Department.objects.all()
    months = get_months()
    # t = loader.get_template('panel/items/new_asset.html')
    # c = dict({'user': user, 'assets': assets, 'currencies': currencies, 'photo': photo, 'member': member})
    return render_to_response('panel/profiles/new_employee.html',
                              {'request': request, 'user': user, 'photo': photo, 'employees': employees,
                               'employee': employee, 'months': months, 'relatives_count': relatives_count,
                               'departments': departments, 'education_count': education_count,
                               'dependent_count': dependent_count, 'reference_count': reference_count,
                               'beneficiary_count': beneficiary_count, 'show_profiles': show_profiles,
                               'show_approvals': show_approvals})


@login_required
@csrf_exempt
def admin_update_employee(request, user_id, employee_id):
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    emp = Employee.objects.get(pk=employee_id)
    emp_info = UserInfo.objects.filter(user=emp.user)
    emp_photo = Photograph.objects.filter(user=emp.user)
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)
    if request.method == 'POST':
        print request.POST
        update_employee = request.POST['update_employee'] if 'update_employee' in request.POST.keys() else None
        if employee_id is not None:
            emp = Employee.objects.get(pk=employee_id)
            print emp
            if emp is not None:
                # spiritual_name = request.POST['spiritual_name'] if 'spiritual_name' in request.POST.keys() else None
                employee_photo = request.FILES['employee_photo'] if 'employee_photo' in request.FILES.keys() else None
                title = request.POST['employee_title'] if 'employee_title' in request.POST.keys() else None
                first_name = request.POST['first_name'] if 'first_name' in request.POST.keys() else None
                last_name = request.POST['last_name'] if 'last_name' in request.POST.keys() else None
                other_names = request.POST['other_names'] if 'other_names' in request.POST.keys() else None
                dob = request.POST['dob_date'] if 'dob_date' in request.POST.keys() else None
                gender = request.POST['gender'] if 'gender' in request.POST.keys() else None
                marital_status = request.POST['marital_status'] if 'marital_status' in request.POST.keys() else None
                phone = request.POST['phone'] if 'phone' in request.POST.keys() else None
                email = request.POST['email'] if 'email' in request.POST.keys() else None

                second_phone = request.POST['second_phone'] if 'second_phone' in request.POST.keys() else None
                second_email = request.POST['second_email'] if 'second_email' in request.POST.keys() else None
                nationality = request.POST['nationality'] if 'nationality' in request.POST.keys() else None
                ethnicity = request.POST['ethnicity'] if 'ethnicity' in request.POST.keys() else None
                hometown = request.POST['hometown'] if 'hometown' in request.POST.keys() else None
                region = request.POST['region'] if 'region' in request.POST.keys() else None
                postal = request.POST['postal'] if 'postal' in request.POST.keys() else None
                residential = request.POST['residential'] if 'residential' in request.POST.keys() else None
                residence_country = request.POST['residence_country'] if 'residence_country' in request.POST.keys() else None
                residence_city = request.POST['residence_city'] if 'residence_city' in request.POST.keys() else None
                day_of_birth = request.POST['day_of_birth'] if 'day_of_birth' in request.POST.keys() else None
                place_of_birth = request.POST['place_of_birth'] if 'place_of_birth' in request.POST.keys() else None
                interests = request.POST['interests'] if 'interests' in request.POST.keys() else None
                spouse_name = request.POST['spouse_name'] if 'spouse_name' in request.POST.keys() else None
                spouse_phone = request.POST['spouse_phone'] if 'spouse_phone' in request.POST.keys() else None
                social_security_number = request.POST['social_security_no'] if 'social_security_no' in request.POST.keys() else None

                employee_leave_id = request.POST['employee_leave_id'] if 'employee_leave_id' in request.POST.keys() else None
                leave_days_allowed = request.POST['leave_days_allowed'] if 'leave_days_allowed' in request.POST.keys() else None

                bank_name = request.POST['bank_name'] if 'bank_name' in request.POST.keys() else None
                bank_branch = request.POST['bank_branch'] if 'bank_branch' in request.POST.keys() else None
                bank_account_name = request.POST['bank_account_name'] if 'bank_account_name' in request.POST.keys() else None
                bank_account_number = request.POST['bank_account_number'] if 'bank_account_number' in request.POST.keys() else None

                emergency_contact_name = request.POST['emergency_contact_name'] if 'emergency_contact_name' in request.POST.keys() else None
                emergency_contact_relationship = request.POST['emergency_contact_relationship'] if 'emergency_contact_relationship' in request.POST.keys() else None
                emergency_contact_phone = request.POST['emergency_contact_phone'] if 'emergency_contact_phone' in request.POST.keys() else None
                emergency_contact_phone_2 = request.POST['emergency_contact_phone_2'] if 'emergency_contact_phone_2' in request.POST.keys() else None
                emergency_contact_email = request.POST['emergency_contact_email'] if 'emergency_contact_email' in request.POST.keys() else None
                emergency_contact_address = request.POST['emergency_contact_address'] if 'emergency_contact_address' in request.POST.keys() else None

                languages = request.POST['languages'] if 'languages' in request.POST.keys() else None

                department_id = request.POST['department_id'] if 'department_id' in request.POST.keys() else None
                emergency_contact_id = request.POST['emergency_contact_id'] if 'emergency_contact_id' in request.POST.keys() else None
                bank_detail_id = request.POST['bank_detail_id'] if 'bank_detail_id' in request.POST.keys() else None
                # is_member = request.POST['is_member'] if '' in request.POST.keys() else None
                is_employee = True

                print request.POST

                user_profile = emp.user
                department = emp.department
                user_profile.title = title
                user_profile.first_name = first_name
                user_profile.last_name = last_name
                user_profile.dob = dob
                user_profile.other_names = other_names
                user_profile.gender = gender
                user_profile.marital_status = marital_status
                user_profile.phone = phone
                user_profile.email = email
                user_profile.is_logged_in = False
                user_profile.save()

                if user_profile is not None:
                    user_info_id = request.POST['user_info_id'] if 'user_info_id' in request.POST.keys() else None
                    if user_info_id is not None:
                        user_info = UserInfo.objects.get(pk=user_info_id)
                        if user_info:
                            user_info.nationality = nationality
                            user_info.ethnicity = ethnicity
                            user_info.region=region
                            user_info.hometown=hometown
                            user_info.postal=postal
                            user_info.residential=residential
                            user_info.residence_city=residence_city
                            user_info.day_of_birth=day_of_birth
                            user_info.residence_country=residence_country
                            user_info.place_of_birth=place_of_birth
                            user_info.interests=interests
                            user_info.languages=languages
                            user_info.second_phone=second_phone
                            user_info.spouse_phone=spouse_phone
                            user_info.spouse_name=spouse_name
                            user_info.social_security_number=social_security_number
                            user_info.save()

                    emp.department = department
                    emp.save()
                    if emp is not None:
                        if employee_photo is not None:
                            emp_photo = Photograph.objects.create(user=user_profile, document=employee_photo)
                            emp_photo.save()
                        #  EMERGENCY CONTACT
                        emergency_contact = EmergencyContact.objects.get(pk=emergency_contact_id) \
                            if emergency_contact_id is not None and len(emergency_contact_id) > 0 else None
                        if emergency_contact is not None:
                            emergency_contact.full_name=emergency_contact_name
                            emergency_contact.relationship=emergency_contact_relationship
                            emergency_contact.phone=emergency_contact_phone
                            emergency_contact.second_phone=emergency_contact_phone_2
                            emergency_contact.email=emergency_contact_email
                            emergency_contact.residential=emergency_contact_address
                            emergency_contact.save()

                        #  BANK DETAILS
                        bank_detail = BankDetail.objects.get(pk=bank_detail_id) \
                            if bank_detail_id is not None and len(bank_detail_id) > 0 else None
                        if bank_detail is not None:
                            bank_detail.bank_name=bank_name
                            bank_detail.branch=bank_branch
                            bank_detail.account_name=bank_account_name
                            bank_detail.account_number=bank_account_number
                            bank_detail.save()

                        #  BANK DETAILS
                        leave_days_allowed = 0 if len(leave_days_allowed) == 0 or leave_days_allowed is None else leave_days_allowed
                        if employee_leave_id is not None and len(employee_leave_id) > 0:
                            employee_leave = EmployeeLeave.objects.get(pk=employee_leave_id)
                            if employee_leave is not None:
                                employee_leave.no_of_days_allowed=int(leave_days_allowed)
                                employee_leave.save()

                        # EDUCATION RECORDS
                        for key in request.POST.keys():
                            keys = ['programme_', 'qualification_', 'institution_', 'education_start_date_',
                                    'education_end_date_', 'short_course_', 'education_present_']
                            if 'programme_' in key:
                                i = int(key.replace('programme_', ''))
                                programme = request.POST[keys[0] + str(i)] if keys[0] + str(i) in request.POST.keys() else None
                                qualification = request.POST[keys[1] + str(i)] if keys[1] + str(i) in request.POST.keys() else None
                                institution = request.POST[keys[2] + str(i)] if keys[2] + str(i) in request.POST.keys() else None
                                start_date = request.POST[keys[3] + str(i)] if keys[3] + str(i) in request.POST.keys() else None
                                end_date = request.POST[keys[4] + str(i)] if keys[4] + str(i) in request.POST.keys() else None
                                short_course = request.POST[keys[5] + str(i)] if keys[5] + str(i) in request.POST.keys() else None
                                education_present = request.POST[keys[6] + str(i)] if keys[6] + str(i) in request.POST.keys() else False

                                if (programme is not None) and len(programme) > 0:
                                    education_record = Education.objects.filter(pk=i)
                                    if education_record is not None and len(education_record) > 0:
                                        education_record = education_record[0]
                                        education_record.courses = programme
                                        education_record.qualification = qualification
                                        education_record.institution = institution
                                        education_record.start_date = start_date
                                        education_record.end_date = end_date
                                        education_record.short_course = short_course
                                        education_record.present = education_present

                        # PROVIDENT FUND BENEFICIARIES
                        beneficiary_records = list()
                        for key in request.POST.keys():
                            keys = ['beneficiary_name_', 'beneficiary_dob_', 'beneficiary_phone_', 'beneficiary_email_',
                                    'beneficiary_address_', 'beneficiary_relationship_', 'beneficiary_percentage_']
                            if 'beneficiary_name_' in key:
                                i = int(key.replace('beneficiary_name_', ''))
                                name = request.POST[keys[0] + str(i)] if keys[0] + str(i) in request.POST.keys() else None
                                dob = request.POST[keys[1] + str(i)] if keys[1] + str(i) in request.POST.keys() else None
                                phone = request.POST[keys[2] + str(i)] if keys[2] + str(i) in request.POST.keys() else None
                                email = request.POST[keys[3] + str(i)] if keys[3] + str(i) in request.POST.keys() else None
                                residential = request.POST[keys[4] + str(i)] if keys[4] + str(i) in request.POST.keys() else None
                                relationship = request.POST[keys[5] + str(i)] if keys[5] + str(i) in request.POST.keys() else None
                                percentage = request.POST[keys[6] + str(i)] if keys[6] + str(i) in request.POST.keys() else False

                                if (name is not None) and len(name) > 0:
                                    beneficiary_record = ProvidentFundBeneficiary.objects.filter(pk=i)
                                    if beneficiary_record is not None and len(beneficiary_record) > 0:
                                        beneficiary_record = beneficiary_record[0]
                                        beneficiary_record.full_name = name
                                        beneficiary_record.date_of_birth = dob
                                        beneficiary_record.phone = phone
                                        beneficiary_record.email = email
                                        beneficiary_record.relationship = relationship
                                        beneficiary_record.residential = residential
                                        beneficiary_record.percentage = percentage
                                        beneficiary_record.save()

                        # DEPENDENTS
                        for key in request.POST.keys():
                            keys = ['dependent_name_', 'dependent_dob_', 'dependent_relationship_', 'dependent_age_',
                                    'dependent_photo_']
                            if 'dependent_name_' in key:
                                i = int(key.replace('dependent_name_', ''))
                                name = request.POST[keys[0] + str(i)] if keys[0] + str(i) in request.POST.keys() else None
                                dob = request.POST[keys[1] + str(i)] if keys[1] + str(i) in request.POST.keys() else None
                                relationship = request.POST[keys[2] + str(i)] if keys[2] + str(i) in request.POST.keys() else None
                                age = request.POST[keys[3] + str(i)] if keys[3] + str(i) in request.POST.keys() else False
                                dep_photo = request.FILES[keys[4] + str(i)] if keys[4] + str(i) in request.FILES.keys() else None

                                if (name is not None) and len(name) > 0:
                                    if (dob is not None) and len(dob) > 0:
                                        birth_date = datetime.strptime(dob, DATE_FORMAT)
                                        age = calculate_age(birth_date)
                                    dependent_record = Dependant.objects.filter(pk=i)
                                    if dependent_record is not None and len(dependent_record) > 0:
                                        dependent_record = dependent_record[0]
                                        dependent_record.name = name
                                        dependent_record.relationship = relationship
                                        dependent_record.date_of_birth = dob
                                        dependent_record.age = age
                                        if dep_photo is not None:
                                            dependent_record.photo = dep_photo
                                        dependent_record.save()

                        # EMPLOYEE REFERENCES
                        for key in request.POST.keys():
                            keys = ['reference_name_', 'reference_type_', 'reference_organization_',
                                    'reference_position_', 'reference_phone_', 'reference_email_', 'reference_address_']
                            if 'reference_name_' in key:
                                i = int(key.replace('reference_name_', ''))
                                name = request.POST[keys[0] + str(i)] if keys[0] + str(i) in request.POST.keys() else None
                                type = request.POST[keys[1] + str(i)] if keys[1] + str(i) in request.POST.keys() else None
                                organization = request.POST[keys[2] + str(i)] if keys[2] + str(i) in request.POST.keys() else None
                                position = request.POST[keys[3] + str(i)] if keys[3] + str(i) in request.POST.keys() else ''
                                phone = request.POST[keys[4] + str(i)] if keys[4] + str(i) in request.POST.keys() else ''
                                email = request.POST[keys[5] + str(i)] if keys[5] + str(i) in request.POST.keys() else ''
                                address = request.POST[keys[6] + str(i)] if keys[6] + str(i) in request.POST.keys() else ''

                                if (name is not None) and len(name) > 0:
                                    # references = add_reference_record(references, emp, name, type, organization,
                                    #                                   position, phone, email, address)
                                    reference = EmployeeReference.objects.filter(pk=i)
                                    if reference is not None and len(reference) > 0:
                                        reference = reference[0]
                                        reference.name = name
                                        reference.position = position
                                        reference.phone = phone
                                        reference.email = email
                                        reference.address = address
                                        reference.organisation = organization
                                        reference.type = type
                                        reference.save()

                print "/panel/%s/employees/%s" % (user.id, emp.id)
                return HttpResponseRedirect("/panel/%s/employees/%s" % (user.id, emp.id))
    user = UserProfile.objects.get(pk=user_id)
    photo = get_photo(user)
    relatives_count = [1, 2, 3, 4, 5, 6, 7]
    education_count = [1, 2, 3, 4]
    dependent_count = [1, 2, 3, 4]
    beneficiary_count = [1, 2, 3]
    reference_count = [1, 2, 3]
    employees = Employee.objects.all()
    departments = Department.objects.all()
    dependents = Dependant.objects.filter(employee=emp)
    education = Education.objects.filter(employee=emp)
    beneficiaries = ProvidentFundBeneficiary.objects.filter(employee=emp)
    bank_detail = BankDetail.objects.filter(employee=emp)
    emergency_cntct = EmergencyContact.objects.filter(employee=emp)
    employee_leave = EmployeeLeave.objects.filter(employee=emp)
    references = EmployeeReference.objects.filter(employee=emp)
    months = get_months()
    return render_to_response('panel/profiles/update_employee.html',
                              {'request': request, 'user': user, 'photo': photo, 'employees': employees,
                               'employee': employee, 'months': months, 'relatives_count': relatives_count, 'emp': emp,
                               'emp_photo': emp_photo, 'departments': departments, 'education_count': education_count,
                               'dependent_count': dependent_count, 'reference_count': reference_count,
                               'beneficiary_count': beneficiary_count, 'show_profiles': show_profiles,
                               'emp_info': emp_info[0] if len(emp_info) > 0 else emp_info, 'dependents': dependents,
                               'show_approvals': show_approvals, 'education_records': education, 'beneficiaries': beneficiaries,
                               'bank_detail': bank_detail[0] if len(bank_detail) > 0 else bank_detail,
                               'emergency_contact': emergency_cntct[0] if len(emergency_cntct) > 0 else emergency_cntct,
                               'employee_leave': employee_leave[0] if len(employee_leave) > 0 else employee_leave,
                               'references': references})


@login_required
@csrf_exempt
def admin_delete_leave_request(request, user_id, leave_request_id):
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    department = employee.department
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)
    if request.method == 'POST':
        delete_leave = request.POST['delete_leave_request'] if 'delete_leave_request' in request.POST.keys() else None
        if leave_request_id is not None:
            leave_request = LeaveRequest.objects.get(pk=leave_request_id)
            if leave_request is not None and delete_leave == 'Delete':
                leave_request.delete()
                return HttpResponseRedirect("/panel/%s/leave_request/" % user.id)

    leave_requests = list()
    department_employees = Employee.objects.filter(department=department)
    for emp in department_employees:
        if emp != employee:
            leave_requests += LeaveRequest.objects.filter(employee=emp)
    photo = get_photo(user)
    return render_to_response('panel/employee/leave_requests.html',
                              {'request': request, 'user': user, 'photo': photo, 'employee': employee,
                               'leave_requests': leave_requests, 'employees': department_employees,
                               'show_profiles': show_profiles, 'show_approvals': show_approvals})


@login_required
@csrf_exempt
def admin_leave_approvals(request, user_id, leave_request_id):
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    department = employee.department
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)
    if request.method == 'POST':
        approve_leave = request.POST['approve_leave'] if 'approve_leave' in request.POST.keys() else None
        if leave_request_id is not None:
            leave_request = LeaveRequest.objects.get(pk=leave_request_id)
            if leave_request is not None and approve_leave == 'Approve':
                leave_request.approved = True
                leave_request.save()
                employee_leave = EmployeeLeave.objects.filter(employee=leave_request.employee)
                if employee_leave is not None and len(employee_leave) > 0:
                    employee_leave[0].no_of_days_taken += leave_request.no_of_days
                    employee_leave[0].no_of_days_left -= leave_request.no_of_days
                    employee_leave[0].save()

                    return HttpResponseRedirect("/panel/%s/leave_approval/" % user.id)

    leave_requests = list()
    department_employees = Employee.objects.filter(department=department)
    for emp in department_employees:
        if emp != employee:
            leave_requests += LeaveRequest.objects.filter(employee=emp)
    if employee.role.name == 'Administrator':
        leave_requests = LeaveRequest.objects.filter()
    photo = get_photo(user)
    return render_to_response('panel/employee/leave_approvals.html',
                              {'request': request, 'user': user, 'photo': photo, 'employee': employee,
                               'leave_requests': leave_requests, 'employees': department_employees,
                               'show_profiles': show_profiles, 'show_approvals': show_approvals})


@login_required
@csrf_exempt
def admin_leave_requests(request, user_id, leave_request_id):
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    leave_requests = LeaveRequest.objects.filter(employee=employee)
    employee_leave = EmployeeLeave.objects.filter(employee=employee)
    photo = get_photo(user)
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)
    return render_to_response('panel/employee/leave_requests.html',
                              {'request': request, 'user': user, 'photo': photo, 'employee': employee,
                               'leave_requests': leave_requests,
                               'employee_leave': employee_leave[0] if len(employee_leave) > 0 else employee_leave,
                               'show_profiles': show_profiles, 'show_approvals': show_approvals})


@login_required
@csrf_exempt
def admin_leave_request(request, user_id):
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)
    if request.method == 'POST':
        leave_type_id = request.POST['leave_type_id'] if 'leave_type_id' in request.POST.keys() else None
        employee_id = request.POST['employee_id'] if 'employee_id' in request.POST.keys() else None
        no_days = request.POST['no_days'] if 'no_days' in request.POST.keys() else None
        start_date = request.POST['start_date'] if 'start_date' in request.POST.keys() else None
        end_date = request.POST['end_date'] if 'end_date' in request.POST.keys() else None
        reliever = request.POST['reliever'] if 'reliever' in request.POST.keys() else None

        # handover_notes = request.POST['handover_notes'] if 'handover_notes' in request.POST.keys() else False
        # hod_signed = request.POST['hod_signed'] if 'hod_signed' in request.POST.keys() else False
        # hr_signed = request.POST['hr_signed'] if 'hr_signed' in request.POST.keys() else False
        # is_approved = request.POST['is_approved'] if 'is_approved' in request.POST.keys() else False
        # approval_reason = request.POST['handover_notes'] if 'handover_notes' in request.POST.keys() else False
        request_date = request.POST['request_date'] if 'request_date' in request.POST.keys() else date.today().strftime("%Y-%m-%d")

        leave_type = LeaveType.objects.get(pk=leave_type_id)
        emp = Employee.objects.get(pk=employee_id)
        if leave_type is not None and emp is not None:
            leave_request = \
                LeaveRequest.objects.create(employee=emp, type=leave_type, start_date=start_date,
                                            end_date=end_date, no_of_days=no_days, reliever=reliever,
                                            hand_over_notes=False, hod_signed=False,
                                            hr_signed=False, approved=False, approval_reason=None,
                                            date=request_date)
            leave_request.save()
        return HttpResponseRedirect("/panel/%s/leave_request/" % user.id)
    user = UserProfile.objects.get(pk=user_id)
    leave_requests = LeaveRequest.objects.filter(employee=employee)
    employee_leave = EmployeeLeave.objects.filter(employee=employee)
    employees = Employee.objects.all()
    leave_types = LeaveType.objects.all()
    photo = get_photo(user)
    return render_to_response('panel/employee/leave_request.html',
                              {'request': request, 'user': user, 'photo': photo, 'employee': employee,
                               'employees': employees, 'leave_types': leave_types, 'leave_requests': leave_requests,
                               'employee_leave': employee_leave[0] if len(employee_leave) > 0 else employee_leave,
                               'show_profiles': show_profiles, 'show_approvals': show_approvals})


@login_required
@csrf_exempt
def admin_absence_certifications(request, user_id, absence_certification_id):
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    user = UserProfile.objects.get(pk=user_id)
    employees = Employee.objects.all()
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)
    absence_certifications = AbsenceCertification.objects.all()
    photo = get_photo(user)
    return render_to_response('panel/employee/absence_certifications.html',
                              {'request': request, 'user': user, 'photo': photo, 'employee': employee,
                               'employees': employees, 'absence_certifications': absence_certifications,
                               'show_profiles': show_profiles, 'show_approvals': show_approvals})


@login_required
@csrf_exempt
def admin_absence_certification(request, user_id):
    user = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user)
    employee = Employee.objects.get(user=user)
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)
    if request.method == 'POST':
        employee_id = request.POST['employee_id'] if 'employee_id' in request.POST.keys() else None
        leave_type_id = request.POST['leave_type_id'] if 'leave_type_id' in request.POST.keys() else None
        print leave_type_id
        no_days = request.POST['no_days'] if 'no_days' in request.POST.keys() else None
        start_date = request.POST['start_date'] if 'start_date' in request.POST.keys() else None
        end_date = request.POST['end_date'] if 'end_date' in request.POST.keys() else None
        return_date = request.POST['return_date'] if 'return_date' in request.POST.keys() else None
        reason = request.POST['reason'] if 'reason' in request.POST.keys() else None
        description_of_symptoms = request.POST['description_of_symptoms'] if 'description_of_symptoms' in request.POST.keys() else None
        doctor_consulted = request.POST['doctor_consulted'] if 'doctor_consulted' in request.POST.keys() else None
        date_consulted = request.POST['date_consulted'] if 'date_consulted' in request.POST.keys() else None
        treatment = request.POST['treatment'] if 'treatment' in request.POST.keys() else None
        name_of_doctor = request.POST['name_of_doctor'] if 'name_of_doctor' in request.POST.keys() else None
        address_of_doctor = request.POST['address_of_doctor'] if 'address_of_doctor' in request.POST.keys() else None
        declaration = request.POST['declaration'] if 'declaration' in request.POST.keys() else None
        employee_signed = True
        request_date = date.today().strftime("%Y-%m-%d")

        leave_type = LeaveType.objects.get(pk=leave_type_id)
        emp = Employee.objects.get(pk=employee_id) if employee_id is not None else employee
        if leave_type is not None:
            print leave_type, start_date, end_date, return_date, no_days, description_of_symptoms, doctor_consulted, \
                date_consulted, name_of_doctor, address_of_doctor, declaration, employee_signed, treatment, reason, \
                request_date
            absence_certification = \
                AbsenceCertification.objects.create(employee=emp, type=leave_type, start_date=start_date,
                                                    end_date=end_date, return_date=return_date, no_of_days=no_days,
                                                    description_of_symptoms=description_of_symptoms,
                                                    doctor_consulted=doctor_consulted, date_consulted=date_consulted,
                                                    name_of_doctor=name_of_doctor, address_of_doctor=address_of_doctor,
                                                    declaration=declaration, employee_signed=employee_signed,
                                                    treatment=treatment, reason=reason, date=request_date)
            absence_certification.save()
        return HttpResponseRedirect("/panel/%s/absence_certification/" % user.id)
    user = UserProfile.objects.get(pk=user_id)
    employees = Employee.objects.all()
    leave_types = LeaveType.objects.all()
    photo = get_photo(user)
    return render_to_response('panel/employee/absence_certification.html',
                              {'request': request, 'user': user, 'photo': photo, 'employee': employee,
                               'employees': employees, 'leave_types': leave_types, 'show_profiles': show_profiles,
                               'show_approvals': show_approvals})


@login_required
def admin_sales(request, user_id, sale_id):
    sales = Sale.objects.all()
    user = UserProfile.objects.get(pk=user_id)
    member = Employee.objects.filter(user=user)

    count = len(sales)
    total_amount = 0
    total = dict()
    frequency = dict()
    photo = None

    if sale_id is not None:
        sale = Sale.objects.get(pk=sale_id)
        sales = get_assets_data(sale_id, None, False, False)
        recent_sales = get_assets_data(sale_id, get_past_date(7), True, False)
        t = loader.get_template('panel/finances/sales.html')
        c = dict({'user': user, 'sale': sale, 'sales': sales, 'photo': photo, 'total': total,
                  'recent_sales': recent_sales, 'total_amount': total_amount, 'frequency': frequency, 'member': member})
        return HttpResponse(t.render(c))

    for sale in sales:
        total_amount += sale.amount
        amount = total[sale.type] if sale.type in total.keys() else 0
        frequency[sale.type] = frequency[sale.type] if sale.type in frequency.keys() else 0
        total[sale.type] = amount + sale.amount
        frequency[sale.type] += 1

    if user.photo is not None:
        photo = user.photo
    # t = loader.get_template('panel/index.html')
    # c = dict({'user': user, 'sales': sales, 'member': member, 'photo': photo})
    return render_to_response('panel/index.html',
                              {'user': user, 'sales': sales, 'member': member, 'count': count, 'photo': photo,
                               'total': total, 'total_amount': total_amount, 'frequency': frequency})


@login_required
@csrf_exempt
def admin_new_attendance(request, user_id):
    user = UserProfile.objects.get(pk=user_id)
    # user.user.
    member = Employee.objects.filter(user=user)
    if request.method == 'POST':
        name = request.POST['asset_name']
        type = request.POST['asset_type']
        brand = request.POST['asset_brand']
        currency_id = request.POST['asset_currency']
        cost = request.POST['asset_cost']
        purchase_date = request.POST['asset_purchase_date']
        quantity = request.POST['asset_quantity']
        has_receipt = request.POST['has_receipt']
        purpose = request.POST['asset_purpose']
        description = request.POST['asset_description']

        currency = Currency.objects.get(pk=currency_id)
        custodian = Employee.objects.filter(user=user)
        asset = Asset.objects.create(name=name, type=type, brand=brand, purchase_date=purchase_date, cost=cost,
                                     quantity=quantity, purpose=purpose, currency=currency, has_receipt=has_receipt,
                                     description=description, custodian=custodian)
        if asset is not None:
            return HttpResponseRedirect("/panel/%s/assets/" % user.id)
    assets = Asset.objects.all()
    # print assets.count(), assets
    user = UserProfile.objects.get(pk=user_id)
    currencies = Currency.objects.all()
    photo = None
    if user.photo is not None:
        photo = user.photo
    # t = loader.get_template('panel/items/new_asset.html')
    # c = dict({'user': user, 'assets': assets, 'currencies': currencies, 'photo': photo, 'member': member})
    return render_to_response('panel/asset/new_asset.html',
                              {'request': request, 'user': user, 'assets': assets, 'currencies': currencies,
                               'photo': photo, 'member': member})


@login_required
def admin_attendance(request, user_id, attendance_id):
    attendances = Attendance.objects.all()
    user = UserProfile.objects.get(pk=user_id)
    member = Employee.objects.filter(user=user)
    photo = None

    if attendance_id is not None:
        attendance = Asset.objects.get(pk=attendance_id)
        attendances = get_attendance_data(attendance_id, None, False, False)
        recent_attendances = get_attendance_data(attendance_id, get_past_date(7), True, False)
        t = loader.get_template('panel/attendance.html')
        c = dict({'user': user, 'attendance': attendance, 'attendances': attendances, 'photo': photo,
                  'recent_attendances': recent_attendances, 'member': member})
        return HttpResponse(t.render(c))

    if user.photo is not None:
        photo = user.photo
    # t = loader.get_template('panel/index.html')
    # c = dict({'user': user, 'assets': assets, 'member': member, 'photo': photo})
    return render_to_response('panel/index.html', {'user': user, 'attendances': attendances, 'member': member,
                                                   'photo': photo})


# ----- User Registration -------- #
@csrf_exempt
def admin_login(request):
    invalid_credentials = False
    account_disabled = False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_authenticated:
                login(request, user)
                # user_profile = UserProfile.objects.get(user=user)
                user_profile = UserProfile.objects.get(user=user)
                if password == RANDOM_PASSWORD:
                    return HttpResponseRedirect("/panel/%s/user_password/" % user_profile.id)
                else:
                    return HttpResponseRedirect("/panel/%s" % user_profile.id)
            else:
                account_disabled = True
                # print 'Your account has been disabled.'
                return render(request, 'panel/login.html',
                              {'request': request, 'invalid_credentials': invalid_credentials,
                               'account_disabled': account_disabled, 'username': username})
        else:
            invalid_credentials = True
            # print 'Invalid username or password.'
            return render(request, 'panel/login.html',
                          {'request': request, 'invalid_credentials': invalid_credentials,
                           'account_disabled': account_disabled, 'username': username})
    # t = loader.get_template('panel/login.html')
    # c = dict({'request': request})
    return render(request, 'panel/login.html', {'request': request})
    # return render_to_response('panel/login.html', dict(), context_instance=RequestContext(request))
    # return HttpResponse(t.render(c))


@csrf_exempt
def admin_signup(request):
    # print request, request.FILES
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        age = request.POST['age']
        user_photo = request.FILES['user_photo']
        session_key = request.POST['csrfmiddlewaretoken']
        photo = None
        if user_photo is not None:
            photo = Photograph(document=user_photo)
            photo.save()
            # rename_user_photo(photo, username)
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        session_key = session_key if session_key is not None else request.session.session_key
        # user = User.objects.get(username=username, password=password)
        if user is None:
            user = User.objects.create_user(username=username, email=email, password=password)
            args = request.POST.copy()
            args['user'] = user
            # print request
            user_profile = UserProfile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                                      photo=photo, phone=phone, email=email, is_logged_in=True,
                                                      session_id=session_key)
            # spiritual_name = request.POST['spiritual_name']
            # hometown = request.POST['hometown'] or None
            # ethnicity = request.POST['ethnicity'] or None
            # region = request.POST['region'] or None
            # nationality = request.POST['nationality'] or None
            # residence_country = request.POST['residence_country'] or None
            # residential = request.POST['residential'] or None
            # postal = request.POST['postal'] or None
            # second_phone = request.POST['second_phone'] or None
            # second_email = request.POST['second_email'] or None
            # user_info = UserInfo.objects.create(user=user, spiritual_name=spiritual_name, hometown=hometown,
            #                                     ethnicity=ethnicity, nationality=nationality, residential=residential,
            #                                     second_phone=second_phone, second_email=second_email, postal=postal,
            #                                     region=region, residence_country=residence_country)
            print user, user_profile
            # user_profile.save()
        else:
            print request.session
            user_profile = UserProfile.objects.filter(user__username=username)
            if user_profile is None or len(user_profile) == 0:
                user_profile = UserProfile.objects.create(user=user, first_name=first_name, last_name=last_name,
                                                          phone=phone, email=email, is_logged_in=True,
                                                          session_id=session_key)
            else:
                user_profile.update(first_name=first_name, last_name=last_name, photo=photo, email=email, phone=phone,
                                    is_logged_in=True, session_id=session_key)
            print user_profile
            # user_profile.save()
        # user_profile.user.set_password(request.POST['password'])
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/panel/signup/complete/%s" % user_profile.id)
            else:
                return 'Your account has been disabled.'
        else:
            return 'Invalid username or password.'
    # return render_to_response('panel/register.html', dict(), context_instance=RequestContext(request))
    return render_to_response('panel/register.html', dict())


@csrf_exempt
def admin_complete(request, id):
    user_profile = UserProfile.objects.get(pk=id)
    print user_profile
    data = dict()
    data['user_profile'] = user_profile
    return render_to_response('panel/register_complete.html', data, context_instance=RequestContext(request))


@login_required
@csrf_exempt
def admin_change_password(request, user_id):
    user_profile = UserProfile.objects.get(pk=user_id)
    check_logged_in_user(request, user_profile)
    employee = Employee.objects.get(user=user_profile)
    show_profiles = display_profiles(employee)
    show_approvals = display_approvals(employee)
    photo = Photograph.objects.filter(user=user_profile)
    employee_leave = EmployeeLeave.objects.filter(employee=employee)
    leave_requests = LeaveRequest.objects.filter(employee=employee)

    show_notification = False
    password_updated = False
    if request.method == 'POST':
        show_notification = True
        new_password = request.POST['new_password'] if 'new_password' in request.POST.keys() else None
        confirm_password = request.POST['confirm_password'] if 'confirm_password' in request.POST.keys() else None
        if new_password is not None and confirm_password is not None and new_password == confirm_password:
            user = user_profile.user
            if user is not None:
                user.set_password(new_password)
                user.save()
                password_updated = True
        return render_to_response('panel/employee/change_password.html',
                                  {'request': request, 'user': user_profile, 'photo': photo, 'employee': employee,
                                   'show_profiles': show_profiles, 'show_approvals': show_approvals,
                                   'leave_requests': leave_requests[0] if len(leave_requests) > 0 else leave_requests,
                                   'employee_leave': employee_leave[0] if len(employee_leave) > 0 else employee_leave,
                                   'show_notification': show_notification, 'password_updated': password_updated})

    return render_to_response('panel/employee/change_password.html',
                              {'request': request, 'user': user_profile, 'photo': photo, 'employee': employee,
                               'show_profiles': show_profiles, 'show_approvals': show_approvals,
                               'leave_requests': leave_requests[0] if len(leave_requests) > 0 else leave_requests,
                               'employee_leave': employee_leave[0] if len(employee_leave) > 0 else employee_leave,
                               'show_notification': show_notification, 'password_updated': password_updated})


@csrf_exempt
def admin_logout(request, user_id):
    user = UserProfile.objects.get(pk=user_id)
    user.is_logged_in = False
    # user.session_id = ""
    user.save()
    logout(request)
    # print user.user.is_authenticated(), user.user.is_active
    # return render_to_response('panel/login.html', dict(), context_instance=RequestContext(request))
    return render_to_response('panel/login.html', dict())


@csrf_exempt
def admin_send_email(request, user_id):
    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        sender = request.POST['sender']
        to = request.POST['to']
        cc = request.POST['cc']
        bcc = request.POST['bcc']
        attachments = request.FILES['attachments']
        email = EmailMessage(subject=subject, body=body, from_email=sender, to=to, cc=cc, bcc=bcc,
                             attachments=attachments)
        email.send()
    user = UserProfile.objects.get(pk=user_id)
    member = Employee.objects.filter(user=user)
    if user is None:
        return HttpResponseRedirect("/panel/login/")
    photo = None
    if user.photo is not None:
        photo = user.photo
    data = {'user': user, 'photo': photo, 'member': member}
    return render_to_response('panel/index.html', data, context_instance=RequestContext(request))


@csrf_exempt
def admin_send_sms(request, user_id):
    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        sender = request.POST['sender']
        to = request.POST['to']
        cc = request.POST['cc']
        bcc = request.POST['bcc']
        attachments = request.FILES['attachments']
        email = EmailMessage(subject=subject, body=body, from_email=sender, to=to, cc=cc, bcc=bcc,
                             attachments=attachments)
        email.send()
        # api.send_sms(body=body, from_phone=sender, to=to)
        message = SmsMessage(body=body, from_phone=sender, to=to)
        message.send()
    user = UserProfile.objects.get(pk=user_id)
    employee = Employee.objects.filter(user=user)
    if user is None:
        return HttpResponseRedirect("/panel/login/")
    photo = None
    if user.photo is not None:
        photo = user.photo
    data = {'user': user, 'photo': photo, 'employee': employee}
    # return render_to_response('panel/index.html', data, context_instance=RequestContext(request))
    return render_to_response('panel/index.html', data)


# ----- APIs -------- #
def get_chart_data(request):
    start = request.GET['start']
    end = request.GET['end']
    record = request.GET['record']
    trans_mode = request.GET['trans_mode'] if 'trans_mode' in request.GET.keys() else None
    trans_type = request.GET['trans_type'] if 'trans_type' in request.GET.keys() else None
    flag = request.GET['flag']
    chart = request.GET['chart']
    employee_id = request.GET['employeeId'] if 'employeeId' in request.GET.keys() else None
    product_id = request.GET['productId'] if 'productId' in request.GET.keys() else None

    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    dates, timestamps = get_range_of_dates(start_date, end_date)
    data = list()
    summary = dict()
    response = dict()
    response["start_date"] = dict(date=dates[0], timestamp=timestamps[0])

    if record == "offerings":
        data = get_offering_chart_data(data, flag, dates, timestamps, employee_id)

    # elif record == "sales":
    #     data, summary = get_sales_chart_data(data, flag, dates, timestamps, employee_id, product_id)
    #
    # # elif record == "receiving":
    #     data, summary = get_receiving_chart_data(data, flag, dates, timestamps, employee_id, product_id)
    #
    # elif record == "dispatch":
    #     data, summary = get_dispatch_chart_data(data, flag, dates, timestamps, employee_id, product_id)
    #
    # elif record == "calls":
    #     data, summary = get_call_chart_data(data, flag, dates, timestamps, employee_id)
    #
    # elif record == "banking":
    #     data, summary = get_banking_chart_data(data, flag, dates, timestamps, trans_mode, trans_type, employee_id)
    #
    # elif record == "pricing":
    #     data, summary = get_product_pricing_chart_data(data, flag, dates, timestamps, product_id)
    #
    # elif record == "order":
    #     data, summary = get_order_chart_data(data, flag, dates, timestamps, product_id)
    #
    # elif record == "invoice":
    #     data, summary = get_invoice_chart_data(data, flag, dates, timestamps, product_id)
    #
    # elif record == "enquiry":
    #     data = get_enquiry_chart_data(data, flag, dates, timestamps)
    #
    # elif record == "production":
    #     data, summary = get_production_chart_data(data, flag, dates, timestamps, employee_id, product_id)
    #
    # elif record == "production_expense":
    #     data, summary = get_production_expense_chart_data(data, flag, dates, timestamps, employee_id)
    #
    # elif record == "marketing_expense":
    #     data, summary = get_marketing_expense_chart_data(data, flag, dates, timestamps, employee_id)

    response["data"] = data
    response["summary"] = summary
    response["flag"] = flag
    response["chart"] = chart
    return HttpResponse(build_response(response), content_type="application/json")


def get_chart_frequency_options(request):
    record = request.GET['record']
    data = list()

    if record == "sales":
        data = [dict(amount="Amount"), dict(number="Number")]

    elif record == "accounting":
        data = [dict(marketing_expenses="Marketing Expenses"), dict(production_expenses="Production Expenses"),
                dict(sales_number="Sales Number"), dict(sales_amount="Sales Amount"), dict(cash_inflow="Cash Inflow"),
                dict(credited_product_payment="Credit Payments"), dict(total_amount="Total Amount")]

    elif record == "receiving":
        data = [dict(quantity="Quantity"), dict(number="Number")]

    elif record == "dispatch":
        data = [dict(quantity="Quantity"), dict(number="Number")]

    elif record == "banking":
        data = [dict(amount="Amount"),
                dict(number="Number")]

    elif record == "calls":
        data = [dict(number="Number")]

    elif record == "marketing_expense":
        data = [dict(amount="Amount"), dict(number="Number")]

    elif record == "production_expense":
        data = [dict(amount="Amount"), dict(number="Number")]

    elif record == "production":
        data = [dict(quantity="Quantity"), dict(bottles_issued="Bottles Issued"),
                dict(bottles_rejected="Bottles Rejected"), dict(bottles_returned="Bottles Returned"),
                dict(labels_issued="Labels Issued"), dict(labels_rejected="Labels Rejected"),
                dict(labels_returned="Labels Returned"), dict(number="Number")]

    elif record == "order":
        data = [dict(amount="Amount"), dict(number="Number")]

    elif record == "pricing":
        data = [dict(open_market="Open Market Price"), dict(supermarket="Supermarket Price"),
                dict(pharmacy="Pharmacy Price"), dict(wholesalers="Wholesalers Price"),
                dict(distributors="Distributors Price"), dict(retail="Retail Price"), dict(number="Number")]

    elif record == "enquiry":
        data = [dict(number="Number")]

    elif record == "invoice":
        data = [dict(total_price="Total Prices"), dict(discount="Discounts"), dict(number="Number")]

    return HttpResponse(build_response(data), content_type="application/json")


#####################################
#   AUTHENTICATION VIEW FUNCTIONS   #
#####################################
def check_logged_in_user(request, user):
    if (request.user is None) or (not request.user.is_authenticated()):
        return HttpResponseRedirect("/panel/login")


def display_profiles(employee):
    show_profile = False
    if employee.role is not None:
        print(employee.role)
        if employee.role.name in ("Administrator", "Manager", "HR"):
            show_profile = True
    return show_profile


def display_approvals(employee):
    show_approvals = False
    if employee.role is not None:
        if employee.role.name != "Employee":
            show_approvals = True
    return show_approvals


def get_photo(user):
    photo = Photograph.objects.filter(user=user)
    return photo[0] if photo is not None and len(photo) > 0 else photo

