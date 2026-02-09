from enum import Enum
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            return ValueError('The given email must be set!')
        email = self.normalize_email(email=email)
        user = self.model(email=email, **kwargs)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        # kwargs.setdefault('role', 'intern')
        return self._create_user(email, password, **kwargs)
    
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        # kwargs.setdefault('role')
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have status is_staff=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have status is_superuser=True')
        return self._create_user(email, password, **kwargs)


class PositionEnum(Enum):
    Back="Backend"
    Front="Frontend"
    PM="PM"
    Design="Design"

class DepartmentEnum(Enum):
    IT="IT"
    Other="Other"
    

class CustomUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    
    activation_code = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    position = models.CharField(
        max_length=50,
        choices=[(tag.name, tag.value) for tag in PositionEnum],
        blank=True,
        null=True,
        default=None
    )
    department = models.CharField(
        max_length=50,
        choices=[(tag.name, tag.value) for tag in DepartmentEnum],
        blank=True,
        null=True,
        default=None
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True,
        help_text='Фото профиля'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Телефон'
    )
    telegram = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Telegram username'
    )
    linkedin = models.URLField(
        blank=True,
        null=True,
        help_text='LinkedIn профиль'
    )
    github = models.URLField(
        blank=True,
        null=True,
        help_text='GitHub профиль'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.')
    )
    # is_staff = models.BooleanField(default=False)  # Добавлено!
    # is_superuser = models.BooleanField(default=False)
    objects = UserManager()  
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'custom_users' 

    def __str__(self):
        return self.email
    
    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code


# from enum import Enum
# from django.db import models
# from django.contrib.auth.base_user import BaseUserManager
# from django.contrib.auth.models import AbstractUser, AbstractBaseUser
# # Create your models here.


# class UserManager(BaseUserManager):
#     use_in_migrations = True

#     def _create_user(self, email, password, **kwargs):
#         if not email:
#             return ValueError('The given email must be set!')
#         email = self.normalize_email(email=email)
#         user = self.model(email=email, **kwargs)
        
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
    
#     def create_user(self, email, password=None, **kwargs):
#         kwargs.setdefault('is_staff', False)
#         kwargs.setdefault('is_superuser', False)
#         # kwargs.setdefault('role', 'intern')
#         return self._create_user(email, password, **kwargs)
    
#     def create_superuser(self, email, password, **kwargs):
#         kwargs.setdefault('is_staff', True)
#         kwargs.setdefault('is_superuser', True)
#         kwargs.setdefault('is_active', True)
#         # kwargs.setdefault('role')
#         if kwargs.get('is_staff') is not True:
#             raise ValueError('Superuser must have status is_staff=True')
#         if kwargs.get('is_superuser') is not True:
#             raise ValueError('Superuser must have status is_superuser=True')
#         return self._create_user(email, password, **kwargs)

# class DepartmentEnum(Enum):
#     IT="IT"
#     Other="Other"
    
# class PositionEnum(Enum):
#     # IT
#     BACKEND = ("Backend", DepartmentEnum.IT)
#     FRONTEND = ("Frontend", DepartmentEnum.IT)
#     DEVOPS = ("DevOps", DepartmentEnum.IT)
#     HR=("HR", DepartmentEnum.Other)

#     def __init__(self, label, department):
#         self.label = label
#         self.department = department
# position_choices = [(pos.name, pos.label) for pos in PositionEnum]
# class CustomUser(AbstractUser):
#     email = models.EmailField('email address', unique=True)
    
    
#     username = models.CharField(max_length=255, blank=True, null=True)
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=100, blank=True)
#     department = models.CharField(
#         max_length=50,
#         choices=[(dep.name, dep.value) for dep in DepartmentEnum],
#         blank=True,
#         default=DepartmentEnum.IT.name
#     )

#     position = models.CharField(
#         max_length=50,
#         blank=True,
#         choices=position_choices
#     )

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     is_active = models.BooleanField(
#         ('active'),
#         default=True,
#         help_text=(
#             'Designates whether this user should be treated as active. '
#             'Unselect this instead of deleting accounts.')
#     )
#     # is_staff = models.BooleanField(default=False)  # Добавлено!
#     # is_superuser = models.BooleanField(default=False)
#     objects = UserManager()  
#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
#         db_table = 'custom_users' 

#     def __str__(self):
#         return self.email
    

#     @staticmethod
#     def get_positions_for_department(department_name):
#         return [
#             (pos.name, pos.label)
#             for pos in PositionEnum
#             if pos.department.name == department_name
#         ]