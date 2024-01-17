from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Enter an email address")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user
