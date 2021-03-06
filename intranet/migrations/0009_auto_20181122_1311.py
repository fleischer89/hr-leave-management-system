# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-22 13:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intranet', '0008_userprofile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyValue',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dependant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('relationship', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DependantPhoto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('dependant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Dependant')),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Photograph')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAppraisal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('reviewer_role', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeTargetSetting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('goal', models.CharField(max_length=100)),
                ('implementation_strategy', models.TextField(blank=True, null=True)),
                ('first_qtr', models.IntegerField(blank=True, null=True)),
                ('second_qtr', models.IntegerField(blank=True, null=True)),
                ('third_qtr', models.IntegerField(blank=True, null=True)),
                ('fourth_qtr', models.IntegerField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeTraining',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comments', models.TextField(blank=True, null=True)),
                ('attended', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeValueEvaluation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_qtr', models.IntegerField(blank=True, null=True)),
                ('second_qtr', models.IntegerField(blank=True, null=True)),
                ('third_qtr', models.IntegerField(blank=True, null=True)),
                ('fourth_qtr', models.IntegerField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.IntegerField()),
                ('label', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(blank=True, max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReviewerStage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='dependent',
            name='employee',
        ),
        migrations.AlterModelOptions(
            name='bankdetail',
            options={'verbose_name_plural': 'Bank Details'},
        ),
        migrations.AlterModelOptions(
            name='education',
            options={'verbose_name_plural': 'Education'},
        ),
        migrations.AlterModelOptions(
            name='employeeleave',
            options={'verbose_name_plural': 'Employee Leave'},
        ),
        migrations.AlterModelOptions(
            name='leavetype',
            options={'verbose_name_plural': 'Leave Types'},
        ),
        migrations.AlterModelOptions(
            name='providentfundbeneficiary',
            options={'verbose_name_plural': 'Provident Fund Beneficiaries'},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name_plural': 'User Information'},
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='departments',
            new_name='department',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='title',
            new_name='job_title',
        ),
        migrations.AddField(
            model_name='department',
            name='purpose',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='supervisors',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='education',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='education',
            name='present',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='education',
            name='short_course',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='education',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.DeleteModel(
            name='Dependent',
        ),
        migrations.AddField(
            model_name='reviewer',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Employee'),
        ),
        migrations.AddField(
            model_name='employeevalueevaluation',
            name='rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Rating'),
        ),
        migrations.AddField(
            model_name='employeevalueevaluation',
            name='value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.CompanyValue'),
        ),
        migrations.AddField(
            model_name='employeetraining',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Employee'),
        ),
        migrations.AddField(
            model_name='employeetraining',
            name='training',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Training'),
        ),
        migrations.AddField(
            model_name='employeetargetsetting',
            name='rating',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Rating'),
        ),
        migrations.AddField(
            model_name='employeeappraisal',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Employee'),
        ),
        migrations.AddField(
            model_name='employeeappraisal',
            name='reviewer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Reviewer'),
        ),
        migrations.AddField(
            model_name='employeeappraisal',
            name='reviewer_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.ReviewerStage'),
        ),
        migrations.AddField(
            model_name='dependant',
            name='employee',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='intranet.Employee'),
        ),
        migrations.AddField(
            model_name='dependant',
            name='photo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Photograph'),
        ),
    ]
