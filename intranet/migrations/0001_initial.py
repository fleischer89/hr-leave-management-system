# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-04 06:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('headline', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=300)),
                ('date', models.DateField(null=True)),
                ('purpose', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('video', models.URLField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(blank=True, max_length=100, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('purchase_date', models.DateField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='assets')),
                ('cost', models.FloatField(blank=True, null=True)),
                ('has_receipt', models.BooleanField(default=False)),
                ('barcode', models.ImageField(blank=True, null=True, upload_to='barcodes')),
                ('has_barcode', models.BooleanField(default=False)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qr_codes')),
                ('purpose', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssetCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField()),
                ('men', models.IntegerField(blank=True, null=True)),
                ('women', models.IntegerField(blank=True, null=True)),
                ('children', models.IntegerField(blank=True, null=True)),
                ('family_online', models.IntegerField(blank=True, null=True)),
                ('family_men_online', models.IntegerField(blank=True, null=True)),
                ('family_women_online', models.IntegerField(blank=True, null=True)),
                ('family_children_online', models.IntegerField(blank=True, null=True)),
                ('guests', models.IntegerField(blank=True, null=True)),
                ('invited_guests', models.IntegerField(blank=True, null=True)),
                ('media', models.IntegerField(blank=True, null=True)),
                ('performers', models.IntegerField(blank=True, null=True)),
                ('other', models.IntegerField(blank=True, null=True)),
                ('members', models.IntegerField(blank=True, null=True)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceCategory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('second_member', models.CharField(blank=True, max_length=100, null=True)),
                ('purpose', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('logo', models.FileField(blank=True, null=True, upload_to='logo')),
                ('location', models.TextField(blank=True, null=True)),
                ('postal', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('incorporation_date', models.DateField(blank=True, null=True)),
                ('commencement_date', models.DateField(blank=True, null=True)),
                ('employee_number', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessCoverage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessEmployeeEstimate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Commitment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('custodian', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('custodian', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(blank=True, max_length=10, null=True)),
                ('coordinators', models.CharField(max_length=300)),
                ('member_count', models.IntegerField(null=True)),
                ('purpose', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('document', models.FileField(upload_to='documents/%Y/%m/%d')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('custodian', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='Dues',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('custodian', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('programme', models.CharField(blank=True, max_length=150, null=True)),
                ('qualification', models.CharField(blank=True, max_length=150, null=True)),
                ('institution', models.CharField(blank=True, max_length=150, null=True)),
                ('level', models.CharField(blank=True, max_length=50, null=True)),
                ('house', models.CharField(blank=True, max_length=150, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('month', models.IntegerField(blank=True, null=True)),
                ('day', models.IntegerField(blank=True, null=True)),
                ('expected_completion_year', models.IntegerField(blank=True, null=True)),
                ('school_location', models.TextField(blank=True, null=True)),
                ('present', models.NullBooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('company', models.CharField(blank=True, max_length=150, null=True)),
                ('position', models.CharField(max_length=150)),
                ('employment_date', models.DateField(blank=True, null=True)),
                ('resignation_date', models.DateField(blank=True, null=True)),
                ('company_description', models.TextField(blank=True, null=True)),
                ('present', models.NullBooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EquipmentClass',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(blank=True, max_length=100, null=True)),
                ('tag', models.CharField(blank=True, max_length=10, null=True)),
                ('custodian', models.CharField(max_length=100)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('category', models.CharField(blank=True, max_length=20, null=True)),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
                ('occupation', models.CharField(blank=True, max_length=50, null=True)),
                ('is_deceased', models.NullBooleanField(default=False)),
                ('is_retired', models.NullBooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MaintenanceRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('service_provider', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateField()),
                ('cost', models.FloatField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Asset')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_member', models.BooleanField(default=True)),
                ('is_coordinator', models.BooleanField(default=False)),
                ('is_leadership', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('departments', models.ManyToManyField(blank=True, null=True, to='intranet.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Ministry',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(blank=True, max_length=10, null=True)),
                ('coordinators', models.CharField(max_length=300)),
                ('purpose', models.CharField(blank=True, max_length=200, null=True)),
                ('member_count', models.IntegerField(null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Offering',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField(null=True)),
                ('amount', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Currency')),
                ('custodian', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Photograph',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('document', models.FileField(upload_to='photographs')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pledge',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('custodian', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Currency')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('custodian', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Currency')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Testament',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=100)),
                ('series', models.CharField(max_length=100)),
                ('place', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField(null=True)),
                ('price', models.FloatField(null=True)),
                ('enabled', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('is_free', models.BooleanField(default=False)),
                ('url', models.URLField(null=True)),
                ('year', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Currency')),
                ('custodian', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Tithe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('custodian', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('amount', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Currency')),
                ('member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Member')),
            ],
        ),
        migrations.CreateModel(
            name='UserAcademicInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('education', models.ManyToManyField(null=True, to='intranet.Education')),
            ],
        ),
        migrations.CreateModel(
            name='UserEmploymentInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('employment', models.ManyToManyField(null=True, to='intranet.Employment')),
            ],
        ),
        migrations.CreateModel(
            name='UserFamilyInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('relations', models.ManyToManyField(null=True, to='intranet.FamilyMember')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('second_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('second_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('nationality', models.CharField(blank=True, max_length=50, null=True)),
                ('ethnicity', models.CharField(blank=True, max_length=30, null=True)),
                ('hometown', models.CharField(blank=True, max_length=50, null=True)),
                ('region', models.CharField(blank=True, max_length=50, null=True)),
                ('postal', models.TextField(blank=True, null=True)),
                ('residential', models.TextField(blank=True, null=True)),
                ('residence_country', models.CharField(blank=True, max_length=50, null=True)),
                ('residence_city', models.CharField(blank=True, max_length=50, null=True)),
                ('day_of_birth', models.CharField(blank=True, max_length=15, null=True)),
                ('place_of_birth', models.TextField(blank=True, null=True)),
                ('interests', models.TextField(blank=True, null=True)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=150, null=True)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('emergency_contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('languages', models.CharField(blank=True, max_length=150, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('spiritual_name', models.CharField(max_length=100, null=True)),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('other_names', models.TextField(blank=True, null=True)),
                ('dob', models.DateField(null=True)),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=10, null=True)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('is_logged_in', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Photograph')),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='intranet.UserProfile'),
        ),
        migrations.AddField(
            model_name='userfamilyinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='intranet.UserProfile'),
        ),
        migrations.AddField(
            model_name='useremploymentinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='intranet.UserProfile'),
        ),
        migrations.AddField(
            model_name='useracademicinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='intranet.UserProfile'),
        ),
        migrations.AddField(
            model_name='member',
            name='ministry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Ministry'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='intranet.UserProfile'),
        ),
        migrations.AddField(
            model_name='maintenancerecord',
            name='custodian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Member'),
        ),
        migrations.AddField(
            model_name='familymember',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='intranet.UserProfile'),
        ),
        migrations.AddField(
            model_name='employment',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='intranet.UserProfile'),
        ),
        migrations.AddField(
            model_name='education',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='intranet.UserProfile'),
        ),
        migrations.AddField(
            model_name='dues',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Member'),
        ),
        migrations.AddField(
            model_name='donation',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Member'),
        ),
        migrations.AddField(
            model_name='contribution',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Currency'),
        ),
        migrations.AddField(
            model_name='contribution',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Member'),
        ),
        migrations.AddField(
            model_name='commitment',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Currency'),
        ),
        migrations.AddField(
            model_name='commitment',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Member'),
        ),
        migrations.AddField(
            model_name='businesstype',
            name='custodian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Member'),
        ),
        migrations.AddField(
            model_name='business',
            name='coverage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.BusinessCoverage'),
        ),
        migrations.AddField(
            model_name='business',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Member'),
        ),
        migrations.AddField(
            model_name='business',
            name='no_employee_estimate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.BusinessEmployeeEstimate'),
        ),
        migrations.AddField(
            model_name='business',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.BusinessType'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.AttendanceCategory'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='custodian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Member'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.AttendanceEvent'),
        ),
        migrations.AddField(
            model_name='asset',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Currency'),
        ),
        migrations.AddField(
            model_name='asset',
            name='custodian',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.Member'),
        ),
        migrations.AddField(
            model_name='asset',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='intranet.EquipmentClass'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='custodian',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intranet.Member'),
        ),
    ]
