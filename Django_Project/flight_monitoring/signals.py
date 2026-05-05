from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def ensure_default_admin_user(sender, **kwargs):
	if getattr(sender, "name", None) != "flight_monitoring":
		return

	User = get_user_model()
	admin_user, _ = User.objects.get_or_create(
		username="admin",
		defaults={
			"is_staff": True,
			"is_superuser": True,
		},
	)

	admin_user.is_staff = True
	admin_user.is_superuser = True
	admin_user.set_password("admin")
	admin_user.save(update_fields=["password", "is_staff", "is_superuser"])