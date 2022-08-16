from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from stdimage import StdImageField
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, name=None, password=None, is_active=True, is_staff=False, is_admin=False, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Usuário deve ter email.')
        if not password:
            raise ValueError('Usuário deve ter senha.')
        if not name:
            raise ValueError('Usuário deve ter nome.')

        if 'is_funcionario' in kwargs:
            is_funcionario = kwargs.get('is_funcionario')
        else:
            is_funcionario = "0"

        user = self.model(
            email=self.normalize_email(email),
            name= name,
            is_funcionario=is_funcionario
        )

        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None, name=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            is_staff=True
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,
            name=name
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Endereço de Email',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    #personalizados
    is_funcionario = models.BooleanField(default=False)

    name = models.CharField(max_length=100, verbose_name='Nome')

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()

def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename

class TipoSeguro(models.Model):
    tipo = models.CharField(max_length=100, verbose_name="Tipo de seguro")

class OrdemServico(models.Model):
    cliente = models.ForeignKey('User', on_delete=models.CASCADE, related_name='cliente')
    tipo = models.ForeignKey('TipoSeguro', on_delete=models.CASCADE)
    descricao = models.CharField(max_length=500, verbose_name="Descrição")
    data = models.DateField(auto_now_add=True)
    funcionario = models.ForeignKey('User', on_delete=models.CASCADE, related_name='funcionario', null=True, blank=True)
    relatorio = models.CharField(max_length=500, verbose_name="Relatório", blank=True, null=True)
    status = models.IntegerField(default=0)