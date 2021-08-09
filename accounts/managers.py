from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, roll_number, password, **extra_fields):
        '''
        Create and save a user with the given email, and password.
        '''
        if not roll_number:
            raise ValueError('Email is missing')
        roll_number = self.normalize_email(roll_number)
        user = self.model(roll_number=roll_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, roll_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(roll_number, password, **extra_fields)

    def create_superuser(self, roll_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(roll_number, password, **extra_fields)