from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
import uuid
from django.conf import settings


# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, surnames, organization, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surnames=surnames,
                          organization=organization, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surnames, organization, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, surnames, organization, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    surnames = models.CharField(max_length=50)
    organization = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surnames', 'organization']

    def __str__(self):
        return self.email


class Market(models.Model):
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=3)  # ISO currency code


class OperationChain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OperationChain {self.id} created at {self.created_at}"

    @property
    def operations_list(self):
        return self.operations.all()


class Operation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    market = models.ForeignKey('Market', on_delete=models.CASCADE)
    trader = models.CharField(max_length=255)
    description = models.TextField()
    operation_chain = models.ForeignKey('OperationChain', on_delete=models.CASCADE, related_name='operations')
    TYPE_CHOICES = (
        ('stock', 'Stock'),
        ('futures', 'Futures'),
        ('options', 'Options'),
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='created_operations')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='modified_operations')

    class Meta:
        abstract = True


class StockOperation(Operation):
    shares_amount = models.PositiveIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='created_stock_operations')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='modified_stock_operations')
    operation_chain = models.ForeignKey('OperationChain', on_delete=models.CASCADE,
                                        related_name='stock_operation_chain')

    def save(self, *args, **kwargs):
        self.type = 'Stock'  # Set the type for StockOperation
        super(StockOperation, self).save(*args, **kwargs)


class FuturesOperation(Operation):
    contract = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='created_futures_operations')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='modified_futures_operations')
    operation_chain = models.ForeignKey('OperationChain', on_delete=models.CASCADE,
                                        related_name='futures_operation_chain')

    def save(self, *args, **kwargs):
        self.type = 'Futures'  # Set the type for FuturesOperation
        super(FuturesOperation, self).save(*args, **kwargs)


class FuturesOptionsOperation(Operation):
    strike_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='created_futures_options_operations')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='modified_futures_options_operations')
    operation_chain = models.ForeignKey('OperationChain', on_delete=models.CASCADE,
                                        related_name='futures_options_operation_chain')

    def save(self, *args, **kwargs):
        self.type = 'Options'  # Set the type for FuturesOptionsOperation
        super(FuturesOptionsOperation, self).save(*args, **kwargs)
