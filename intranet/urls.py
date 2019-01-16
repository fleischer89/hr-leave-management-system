__author__ = 'Smart Empire'


from django.conf.urls import *
from intranet.views import *


# handler404 = 'intranet.views.handler404'
# handler500 = 'intranet.views.handler500'

urlpatterns = [
    url(r'^/?(?P<user_id>\d+)?/?$', index, name='index'),
    url(r'^login/?$', admin_login, name='admin_login'),
    url(r'^logout/?(?P<user_id>\d+)?/?$', admin_logout, name='admin_logout'),
    url(r'^signup/?$', admin_signup, name='admin_signup'),
    url(r'^signup/complete/(?P<id>\d+)?$', admin_complete, name='admin_complete'),

    url(r'^(?P<user_id>\d+)?/attendance/?((?P<attendance_id>\d+)|)?/?$', admin_attendance, name='admin_attendance'),
    # url(r'^(?P<user_id>\d+)?/attendance/new/?$', admin_new_attendance, name='admin_new_attendance'),

    url(r'^(?P<user_id>\d+)?/departments/?((?P<department_id>\d+)|)?/?$', admin_departments, name='admin_departments'),
    url(r'^(?P<user_id>\d+)?/departments/new/?$', admin_new_department, name='admin_new_department'),
    url(r'^(?P<user_id>\d+)?/update_department/?((?P<department_id>\d+)|)?/?$', admin_update_department,
        name=', admin_update_department'),
    url(r'^(?P<user_id>\d+)?/delete_department/?((?P<department_id>\d+)|)?/?$', admin_delete_department,
        name='admin_delete_department'),

    url(r'^(?P<user_id>\d+)?/employee_registered/((?P<employee_id>\d+)|)?/?$', admin_employees_registered,
        name='admin_employees_registered'),
    url(r'^(?P<user_id>\d+)?/delete_employee/((?P<employee_id>\d+)|)?/?$', admin_delete_employee,
        name='admin_delete_employee'),
    url(r'^(?P<user_id>\d+)?/employees/?((?P<employee_id>\d+)|)?/?$', admin_employees, name='admin_employees'),
    url(r'^(?P<user_id>\d+)?/employees/new/?$', admin_new_employee, name='admin_new_employee'),
    url(r'^(?P<user_id>\d+)?/update_employee/?((?P<employee_id>\d+)|)?/?$', admin_update_employee,
        name='admin_update_employee'),

    url(r'^(?P<user_id>\d+)?/leave_approval/?((?P<leave_request_id>\d+)|)?/?$', admin_leave_approvals,
        name='admin_leave_approvals'),
    url(r'^(?P<user_id>\d+)?/leave_approval/new/?$', admin_leave_request, name='admin_leave_request'),

    url(r'^(?P<user_id>\d+)?/leave_request/?((?P<leave_request_id>\d+)|)?/?$', admin_leave_requests,
        name='admin_leave_requests'),
    url(r'^(?P<user_id>\d+)?/delete_leave_request/?((?P<leave_request_id>\d+)|)?/?$', admin_delete_leave_request,
        name='admin_delete_leave_request'),
    url(r'^(?P<user_id>\d+)?/leave_request/new/?$', admin_leave_request, name='admin_leave_request'),

    url(r'^(?P<user_id>\d+)?/absence_certification/?((?P<absence_certification_id>\d+)|)?/?$',
        admin_absence_certifications, name='admin_absence_certifications'),
    url(r'^(?P<user_id>\d+)?/absence_certification/new/?$', admin_absence_certification,
        name='admin_absence_certification'),

    url(r'^(?P<user_id>\d+)?/user_password/?$', admin_change_password, name='admin_change_password'),

    url(r'^(?P<user_id>\d+)?/sales/?((?P<sale_id>\d+)|)?/?$', admin_sales, name='admin_sales'),


    # ------- APIs -------- #
    url(r'^chart.json/?$', get_chart_data, name='get_chart_data'),
    url(r'^chart/frequency/options.json/?$', get_chart_frequency_options, name='get_chart_frequency_options'),
]