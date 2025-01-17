from django.db import models
from django.utils import timezone

# Create your models here.

class Company(models.Model):
    # Initial Contact Information
    email = models.EmailField('Correo electrónico', blank=True)
    full_name = models.CharField('Nombres y apellidos', max_length=255, blank=True)
    company_name = models.CharField('Empresa', max_length=255, blank=True)
    country = models.CharField('País', max_length=100, blank=True)
    phone = models.CharField('Teléfono', max_length=20, blank=True)

    # Company Information
    legal_name = models.CharField('Nombre de la empresa (Razón social)', max_length=255, blank=True)
    commercial_name = models.CharField('Nombre comercial (Opcional)', max_length=255, blank=True)
    state = models.CharField('Estado', max_length=100, blank=True)
    city = models.CharField('Ciudad', max_length=100, blank=True)
    postal_code = models.CharField('Código postal', max_length=10, blank=True)
    address = models.CharField('Dirección', max_length=255, blank=True)
    website = models.URLField('Sitio Web (Opcional)', blank=True)
    tax_id = models.CharField('Tax ID', max_length=50, blank=True)
    start_date = models.DateField('Fecha de inicio de operaciones', default=timezone.now)
    
    COMPANY_TYPES = [
        ('individual', 'Individual/Propietario Único o LLC de un solo miembro'),
        ('corporation_c', 'Corporación C'),
        ('corporation_s', 'Corporación S'),
        ('association', 'Asociación'),
        ('trust', 'Fideicomiso/Patrimonio'),
        ('none', 'Ninguna opción aplica'),
    ]
    company_type = models.CharField('Tipo de empresa', max_length=20, choices=COMPANY_TYPES, blank=True)

    # Transaction Information
    transaction_purpose = models.TextField('Objetivo de las transacciones', blank=True)
    annual_volume = models.DecimalField('Volumen anual de transacciones (en USD)', max_digits=15, decimal_places=2, default=0)
    annual_transactions = models.IntegerField('Número anual de transacciones', default=0)
    currencies_needed = models.CharField('Divisas requeridas', max_length=255, blank=True)

    # Payment Method
    PAYMENT_METHODS = [
        ('ach', 'ACH Débito Directo'),
        ('check', 'Cheque'),
        ('transfer', 'Transferencia'),
        ('none', 'No aplicable'),
    ]
    payment_method = models.CharField('Método preferido de pago', max_length=20, choices=PAYMENT_METHODS, blank=True)
    bank_name = models.CharField('Nombre del banco', max_length=255, blank=True)
    bank_address = models.CharField('Dirección del banco', max_length=255, blank=True)
    account_number = models.CharField('Número de cuenta', max_length=50, blank=True)
    routing_number = models.CharField('Número ABA/Código de ruta', max_length=50, blank=True)
    
    ACCOUNT_TYPES = [
        ('checking', 'Cheques'),
        ('savings', 'Ahorros'),
    ]
    account_type = models.CharField('Tipo de cuenta', max_length=20, choices=ACCOUNT_TYPES, blank=True)
    
    # Status
    is_completed = models.BooleanField('Registro completado', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.company_name or self.legal_name or f'Company {self.id}'


class AuthorizedUser(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='authorized_users')
    full_name = models.CharField('Nombres y apellidos', max_length=255)
    position = models.CharField('Cargo en la empresa', max_length=255)
    phone = models.CharField('Teléfono celular', max_length=20)
    email = models.EmailField('Correo electrónico')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Authorized User'
        verbose_name_plural = 'Authorized Users'

    def __str__(self):
        return self.full_name


class CompanyPartner(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='partners')
    legal_name = models.CharField('Nombre legal (sin abreviaciones)', max_length=255)
    ownership_percentage = models.DecimalField('Porcentaje de propiedad', max_digits=5, decimal_places=2)
    birth_date = models.DateField('Fecha de nacimiento')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Company Partner'
        verbose_name_plural = 'Company Partners'

    def __str__(self):
        return self.legal_name
