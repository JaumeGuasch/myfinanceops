from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
import uuid
from django.conf import settings
from django.db.models import Max
from django.db import transaction, IntegrityError
from django.utils import timezone
from multiselectfield import MultiSelectField


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
    mic = models.CharField(max_length=4)  # Market Identifier Code
    DAY_CHOICES = (
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    )
    trading_days = MultiSelectField(choices=DAY_CHOICES, max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=3)  # ISO currency code
    notes = models.TextField(blank=True)


class OperationCommission(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    operation = GenericForeignKey('content_type', 'object_id')
    commission = models.ForeignKey('Commissions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=4)  # Amount charged

    class Meta:
        unique_together = ('content_type', 'object_id', 'commission')


class Commissions(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='created_commissions', on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, related_name='modified_commissions', on_delete=models.CASCADE)


class OperationChain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    chain_number = models.CharField(max_length=10, unique=True, editable=False)

    def __str__(self):
        return f"OperationChain {self.chain_number} created at {self.created_at}"

    @property
    def operations_list(self):
        return self.operations.all()

    def save(self, *args, **kwargs):
        if not self.chain_number:
            for _ in range(3):  # Retry mechanism to handle race conditions
                try:
                    with transaction.atomic():
                        current_year = timezone.now().year
                        max_chain_number = \
                            OperationChain.objects.filter(chain_number__startswith=str(current_year)).aggregate(
                                Max('chain_number'))['chain_number__max']
                        if max_chain_number:
                            next_number = int(max_chain_number[-6:]) + 1
                        else:
                            next_number = 1
                        self.chain_number = f"{current_year}{next_number:06d}"
                        super(OperationChain, self).save(*args, **kwargs)
                        break
                except IntegrityError:
                    continue
            else:
                raise IntegrityError("Failed to generate a unique chain_number after multiple attempts.")
        else:
            super(OperationChain, self).save(*args, **kwargs)


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
    TRANSACTION_CHOICES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, editable=False)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='created_operations')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='modified_operations')

    class Meta:
        abstract = True


class StockOperation(Operation):
    stock_code = models.CharField(max_length=255)
    shares_amount = models.PositiveIntegerField()
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='created_stock_operations')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='modified_stock_operations')
    operation_chain = models.ForeignKey('OperationChain', on_delete=models.CASCADE,
                                        related_name='stock_operation_chain')
    commissions = GenericRelation(OperationCommission, related_query_name='stock_operations')

    def save(self, *args, **kwargs):
        self.type = 'Stock'  # Set the type for StockOperation
        super(StockOperation, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Stocks operation"


class FuturesOperation(Operation):
    contract = models.CharField(max_length=255)
    price_per_contract = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='created_futures_operations')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='modified_futures_operations')
    operation_chain = models.ForeignKey('OperationChain', on_delete=models.CASCADE,
                                        related_name='futures_operation_chain')
    commissions = GenericRelation(OperationCommission, related_query_name='futures_operations')

    def save(self, *args, **kwargs):
        self.type = 'Futures'  # Set the type for FuturesOperation
        super(FuturesOperation, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Futures operation"


class FuturesOptionsOperation(Operation):
    strike_price = models.DecimalField(max_digits=10, decimal_places=2)
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_contract = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='created_futures_options_operations')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='modified_futures_options_operations')
    operation_chain = models.ForeignKey('OperationChain', on_delete=models.CASCADE,
                                        related_name='futures_options_operation_chain')
    commissions = GenericRelation(OperationCommission, related_query_name='futures_options_operations')

    def save(self, *args, **kwargs):
        self.type = 'Options'  # Set the type for FuturesOptionsOperation
        super(FuturesOptionsOperation, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Options operation"


class Contracts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=255)
    name_underlying = models.CharField(max_length=255)
    contract = models.CharField(max_length=255)
    expiry_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='created_contracts')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='modified_contracts')
