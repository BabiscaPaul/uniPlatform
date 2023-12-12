# Generated by Django 3.2.12 on 2023-12-12 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_activityregistrations_delete_authgroup_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Activities',
        ),
        migrations.DeleteModel(
            name='Activityassignments',
        ),
        migrations.DeleteModel(
            name='Activityregistrations',
        ),
        migrations.RemoveField(
            model_name='admins',
            name='admin',
        ),
        migrations.DeleteModel(
            name='Authentications',
        ),
        migrations.DeleteModel(
            name='Courses',
        ),
        migrations.DeleteModel(
            name='Enrollments',
        ),
        migrations.DeleteModel(
            name='Grades',
        ),
        migrations.DeleteModel(
            name='Groupactivities',
        ),
        migrations.DeleteModel(
            name='Groupmembers',
        ),
        migrations.DeleteModel(
            name='Groupmessages',
        ),
        migrations.DeleteModel(
            name='Laboratories',
        ),
        migrations.DeleteModel(
            name='Seminars',
        ),
        migrations.RemoveField(
            model_name='students',
            name='student',
        ),
        migrations.DeleteModel(
            name='Studygroups',
        ),
        migrations.RemoveField(
            model_name='superadmins',
            name='super_admin',
        ),
        migrations.RemoveField(
            model_name='teachers',
            name='teacher',
        ),
        migrations.DeleteModel(
            name='Admins',
        ),
        migrations.DeleteModel(
            name='Students',
        ),
        migrations.DeleteModel(
            name='Superadmins',
        ),
        migrations.DeleteModel(
            name='Teachers',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
