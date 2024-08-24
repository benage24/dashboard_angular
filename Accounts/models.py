from django.contrib.auth.models import Permission
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser


# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, role=None, module=None, **extra_fields):
        """
             Creates and saves a User with the given email, username
             and password.
             """
        # if not email:
        #     raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(

            username=username,
            role=role,
            module=module,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(

            password=password,
            username=username
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)

        # Create a superuser role with all permissions and assign it to the superuser
        superuser_role, created = Role.objects.get_or_create(name='Superuser')
        print(superuser_role)
        if created:
            superuser_role.permissions.add(*Permission.objects.all())
        user.role = superuser_role
        user.save(using=self._db)

        return user


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission)  # Use Django's built-in Permission model
    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class CustomPermission(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    permission = models.ManyToManyField(Permission)


class MyUser(AbstractBaseUser):
    """
       Custom user class inheriting AbstractBaseUser class
     """
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True)

    objects = MyUserManager()
    USERNAME_FIELD = 'username'

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True



