from django.contrib.auth.models import User

uname = 'admin'
all_su = User.objects.filter(username=uname)
if len(all_su):
    su = all_su.first()
else:
    su = User()
su.username = uname
su.set_password(uname)
su.is_active = True
su.is_superuser = True
su.is_staff = True
su.save()

for u in User.objects.all():
    print("Found user: %s " % u.username)
