from django.contrib import admin
from .models import Activities, Activityassignments, Admins, Authentications
from .models import Courses, Enrollments, Grades, Groupactivities
from .models import Groupmembers, Groupmessages
from .models import Laboratories, Seminars, Students, Studygroups, Superadmins
from .models import Teachers, Users, Studentenrollments

# Register your models here.

admin.site.register(Activities)
admin.site.register(Activityassignments)
admin.site.register(Admins)
admin.site.register(Authentications)
admin.site.register(Courses)
admin.site.register(Enrollments)
admin.site.register(Grades)
admin.site.register(Groupactivities)
admin.site.register(Groupmembers)
admin.site.register(Groupmessages)
admin.site.register(Laboratories)
admin.site.register(Seminars)
admin.site.register(Students)
admin.site.register(Studygroups)
admin.site.register(Superadmins)
admin.site.register(Teachers)
admin.site.register(Users)
admin.site.register(Studentenrollments)
