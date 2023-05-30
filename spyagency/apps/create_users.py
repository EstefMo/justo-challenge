from django.contrib.auth.models import User
from apps.hit_management.models import Hitman, Manager


# Create big boss hitman
if not User.objects.filter(username='bigboss@example.com').exists():
    bigboss_user = User.objects.create_user('bigboss@example.com', 'bigboss@example.com', 'admin123', first_name='Big Boss', is_superuser=True)
    bigboss_hitman = Hitman.objects.create(user=bigboss_user, description='Big Boss', status='ACTIVE')

# Create hitmen
for i in range(1, 11):
    email = f'hitman{i}@example.com'
    if not User.objects.filter(username=email).exists():
        user = User.objects.create_user(email, email, 'password', first_name=f'Hitman {i}')
        hitman = Hitman.objects.create(user=user, description=f'Hitman {i}', status='ACTIVE')

# Create managers
hitmen = Hitman.objects.all()[:4]
for hitman in hitmen:
    if not hitman.user.is_superuser:
        manager, created = Manager.objects.get_or_create(user=hitman)
        if created:
            # Set is_staff to True for managers
            hitman.user.is_staff = True
            hitman.user.save()
