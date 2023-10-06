from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    tax_number = models.CharField(max_length=10)
    authorized_person = models.CharField(max_length=50)
    contact_info = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    plate = models.CharField(max_length=10)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    inspection_date = models.DateField(null=True, blank=True)
    insurance_date = models.DateField()
    maintenance_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.plate
