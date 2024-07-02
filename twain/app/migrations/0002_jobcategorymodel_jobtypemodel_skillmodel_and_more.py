# Generated by Django 5.0.3 on 2024-03-07 09:05

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobCategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_title', models.CharField(max_length=45)),
                ('category_desc', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='JobTypeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type_title', models.CharField(max_length=45)),
                ('job_type_desc', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='SkillModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_title', models.CharField(max_length=45)),
                ('skill_desc', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CostomerProfileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_desc', models.CharField(max_length=100)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(max_length=20)),
                ('linkedin_profile', models.URLField(blank=True, max_length=255, null=True)),
                ('github_profile', models.URLField(blank=True, max_length=255, null=True)),
                ('profile_picture', models.ImageField(blank=True, default='costomer/images/profile_pic/default_profile_Is8arW2.png', upload_to='costomer/images/profile_pic')),
                ('resume', models.FileField(blank=True, upload_to='costomer/files/resumes')),
                ('long_description', models.TextField(null=True)),
                ('language', models.CharField(blank=True, max_length=255, null=True)),
                ('education', models.TextField(blank=True, null=True)),
                ('available', models.CharField(blank=True, max_length=255, null=True)),
                ('verification', models.BooleanField(default=False)),
                ('experience', models.IntegerField(blank=True, null=True)),
                ('dob', models.DateField(blank=True, max_length=8, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.jobcategorymodel')),
                ('skills', models.ManyToManyField(blank=True, to='app.skillmodel')),
            ],
        ),
        migrations.CreateModel(
            name='DealerProfileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_logo', models.ImageField(blank=True, default='dealer/company/logos/default_profile.png', upload_to='dealer/company/logos')),
                ('company_address', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('company_short_desc', models.CharField(max_length=100)),
                ('company_desc', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='PostjobModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('short_desc', models.CharField(max_length=2000)),
                ('full_desc', ckeditor.fields.RichTextField()),
                ('deadline', models.DateField(blank=True, null=True)),
                ('askamount', models.IntegerField(blank=True, null=True)),
                ('askamount_2', models.IntegerField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('file_upload', models.FileField(blank=True, null=True, upload_to='seller/files/Job')),
                ('slug', models.SlugField(blank=True, max_length=150, null=True, unique=True)),
                ('Attachment', models.FileField(blank=True, null=True, upload_to='buyer/files/Job')),
                ('category_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.jobcategorymodel')),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.dealerprofilemodel')),
                ('job_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.jobtypemodel')),
                ('skills', models.ManyToManyField(to='app.skillmodel')),
            ],
        ),
        migrations.CreateModel(
            name='BidAmountModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_amount', models.IntegerField()),
                ('is_accepted', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('pitch', models.CharField(blank=True, max_length=2000, null=True)),
                ('days', models.CharField(blank=True, max_length=1500, null=True)),
                ('costomer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.costomerprofilemodel')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.postjobmodel')),
            ],
        ),
    ]
