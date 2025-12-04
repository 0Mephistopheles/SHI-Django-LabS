# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def get_current_year():
    return date.today().year

class Author(models.Model):
    authorid = models.AutoField(db_column='AuthorID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=100)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=100)  # Field name made lowercase.
    birthdate = models.DateField(db_column='BirthDate', blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=100, blank=True, null=True)  # Field name made lowercase.
    biography = models.TextField(db_column='Biography', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'author'
        unique_together = (('firstname', 'lastname'),)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Book(models.Model):
    bookid = models.AutoField(db_column='BookID', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=200)  # Field name made lowercase.
    isbn = models.CharField(db_column='ISBN', unique=True, max_length=13)  # Field name made lowercase.
    publicationyear = models.IntegerField(default=get_current_year, db_column='PublicationYear', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    genre = models.CharField(db_column='Genre', max_length=100, blank=True, null=True)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50, blank=True, null=True)  # Field name made lowercase.
    authorid = models.ForeignKey(Author, models.DO_NOTHING, db_column='AuthorID')  # Field name made lowercase.
    publisherid = models.ForeignKey('Publisher', models.DO_NOTHING, db_column='PublisherID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'book'

    def __str__(self):
        return self.title

class Bookedition(models.Model):
    editionid = models.AutoField(db_column='EditionID', primary_key=True)  # Field name made lowercase.
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='BookID')  # Field name made lowercase.
    editionnumber = models.PositiveIntegerField(db_column='EditionNumber', blank=True, null=True)  # Field name made lowercase.
    printrun = models.PositiveIntegerField(db_column='PrintRun', blank=True, null=True)  # Field name made lowercase.
    printingorderid = models.ForeignKey('Printingorder', models.DO_NOTHING, db_column='PrintingOrderID', blank=True, null=True)  # Field name made lowercase.
    releasedate = models.DateField(db_column='ReleaseDate', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bookedition'


class Bookorder(models.Model):
    orderid = models.AutoField(db_column='OrderID', primary_key=True)  # Field name made lowercase.
    customerid = models.ForeignKey('Customer', models.DO_NOTHING, db_column='CustomerID')  # Field name made lowercase.
    orderdate = models.DateTimeField(db_column='OrderDate')  # Field name made lowercase.
    totalamount = models.DecimalField(db_column='TotalAmount', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    paymentstatus = models.CharField(db_column='PaymentStatus', max_length=9, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bookorder'


class Bookorderitem(models.Model):
    orderitemid = models.AutoField(db_column='OrderItemID', primary_key=True)  # Field name made lowercase.
    orderid = models.ForeignKey(Bookorder, models.DO_NOTHING, db_column='OrderID')  # Field name made lowercase.
    bookid = models.ForeignKey(Book, models.DO_NOTHING, db_column='BookID')  # Field name made lowercase.
    quantity = models.PositiveIntegerField(db_column='Quantity')  # Field name made lowercase.
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bookorderitem'
        unique_together = (('orderid', 'bookid'),)


class Customer(models.Model):
    customerid = models.AutoField(db_column='CustomerID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=100)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=100)  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=150)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customer'


class Printingorder(models.Model):
    printingorderid = models.AutoField(db_column='PrintingOrderID', primary_key=True)  # Field name made lowercase.
    orderdate = models.DateTimeField(db_column='OrderDate')  # Field name made lowercase.
    completiondate = models.DateTimeField(db_column='CompletionDate', blank=True, null=True)  # Field name made lowercase.
    quantity = models.PositiveIntegerField(db_column='Quantity')  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=10, blank=True, null=True)  # Field name made lowercase.
    publisherid = models.ForeignKey('Publisher', models.DO_NOTHING, db_column='PublisherID')  # Field name made lowercase.
    printingpressid = models.ForeignKey('Printingpress', models.DO_NOTHING, db_column='PrintingPressID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'printingorder'


class Printingpress(models.Model):
    printingpressid = models.AutoField(db_column='PrintingPressID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=150)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=150, blank=True, null=True)  # Field name made lowercase.
    capacityperday = models.PositiveIntegerField(db_column='CapacityPerDay', blank=True, null=True)  # Field name made lowercase.
    machinetype = models.CharField(db_column='MachineType', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'printingpress'


class Publisher(models.Model):
    publisherid = models.AutoField(db_column='PublisherID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=150)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=100, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=100, blank=True, null=True)  # Field name made lowercase.
    contactemail = models.CharField(db_column='ContactEmail', max_length=150, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'publisher'

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    warehouseid = models.AutoField(db_column='WarehouseID', primary_key=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=150)  # Field name made lowercase.
    capacity = models.PositiveIntegerField(db_column='Capacity', blank=True, null=True)  # Field name made lowercase.
    managername = models.CharField(db_column='ManagerName', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'warehouse'


class Warehousestock(models.Model):
    stockid = models.AutoField(db_column='StockID', primary_key=True)  # Field name made lowercase.
    warehouseid = models.ForeignKey(Warehouse, models.DO_NOTHING, db_column='WarehouseID')  # Field name made lowercase.
    editionid = models.ForeignKey(Bookedition, models.DO_NOTHING, db_column='EditionID')  # Field name made lowercase.
    quantity = models.PositiveIntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    lastupdated = models.DateTimeField(db_column='LastUpdated', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'warehousestock'
        unique_together = (('warehouseid', 'editionid'),)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - {self.balance} грн"

# Автоматичне створення профілю при створенні юзера
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()