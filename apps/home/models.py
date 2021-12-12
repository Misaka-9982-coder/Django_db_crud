from django.db import models

from django.contrib.auth.models import User

class Customer(models.Model):
    cid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    email = models.CharField(max_length=64)
    card = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=10, blank=True, null=True)
    uid = models.IntegerField(max_length=32, null=True)
    class Meta:
        db_table = 'customer'



class Designer(models.Model):
    did = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    price = models.FloatField()

    class Meta:
        db_table = 'designer'



class Bag(models.Model):
    bid = models.AutoField(primary_key=True)
    btype = models.CharField(max_length=32)
    color = models.CharField(max_length=32)
    did = models.ForeignKey('Designer', models.DO_NOTHING, db_column='did')
    already_rented = models.IntegerField()

    class Meta:
        db_table = 'bag'



class Rentals(models.Model):
    rid = models.AutoField(primary_key=True)
    cid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='cid')
    bid = models.ForeignKey(Bag, models.DO_NOTHING, db_column='bid')
    date_rented = models.DateField(blank=True, null=True)
    date_returned = models.DateField(blank=True, null=True)
    optional_insurance = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'rentals'
