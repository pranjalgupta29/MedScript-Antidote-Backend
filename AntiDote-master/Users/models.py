from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .managers import CustomUserManager
from .validators import validate_date

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)

    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Patient(models.Model):
    GENDER_CHOICES =( 
        ("Female", "F"), 
        ("Male", "M"), 
        ("Others", "Others"), 
    ) 
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="Patient")
    Name = models.CharField(max_length=80,default = None,null=True)
    Age = models.IntegerField(default = None,null=True)
    Address = models.TextField(max_length=300,null=True)
    Gender = models.CharField(max_length=30,choices = GENDER_CHOICES,default = 'F',null=True)

    def __str__(self):
        return self.Name


class Specialization(models.Model):
    Name = models.CharField(max_length=100,null=True,blank=True,default = None)

    def __str__(self):
        return self.Name

class Doctor(models.Model):
    GENDER_CHOICES =( 
        ("Female", "F"), 
        ("Male", "M"), 
        ("Others", "Others"), 
    ) 
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="Doctor")
    Name = models.CharField(max_length=80,default = None,null=True)
    Age = models.IntegerField(default = None,null=True)
    Address = models.TextField(max_length=300,null=True)
    Gender = models.CharField(max_length=30,choices = GENDER_CHOICES,default = 'F',null=True)
    Specialization = models.ForeignKey(Specialization,on_delete=models.PROTECT,related_name="Doctors")
    contact  = models.IntegerField(null=True)
    Qualification = models.CharField(max_length=30,null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6,null=True,default=None)
    lon = models.DecimalField(max_digits=9, decimal_places=6,null=True,default=None)

    def __str__(self):
        return self.Name

class Reports(models.Model):
    name= models.CharField(max_length=100)
    Description = models.CharField(max_length=500)
    Patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="Reports")
    filepath= models.FileField(upload_to='files/', null=True, verbose_name="")
    Doctors = models.ManyToManyField(Doctor,related_name="Reports",blank=True)
    def __str__(self):
        return self.name + ": " + str(self.filepath)

@receiver(post_delete, sender=Reports)
def submission_delete(sender, instance, **kwargs):
    instance.filepath.delete(False) 

class Disease(models.Model):
    Name = models.CharField(max_length=100,null=True,blank=True,default = None)
    Specialization = models.ForeignKey(Specialization,on_delete=models.PROTECT,related_name="Diseases")

    def __str__(self):
        return self.Name

class Symptom(models.Model):
    Name = models.CharField(max_length=100,null=True,blank=True,default = None)
    def __str__(self):
        return self.Name


class Treatment(models.Model):
    Patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="Treatments")
    Doctor = models.ForeignKey(Doctor,related_name="Treatments",null=True,on_delete=models.SET_NULL,default=None,blank=True)
    is_active = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    SymptomList = models.ManyToManyField(Symptom,blank=True)
    Disease = models.ForeignKey(Disease,on_delete=models.PROTECT,related_name="Patients")
    Prescription = models.TextField(max_length=800,null=True,default = None,blank=True)
    Appointment = models.DateField(null=True,default = None,blank=True, validators=[validate_date])
    lat = models.DecimalField(max_digits=9, decimal_places=6,null=True,default=None)
    lon = models.DecimalField(max_digits=9, decimal_places=6,null=True,default=None)

class QnA(models.Model):
    Made_By = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Questions")
    Question =  models.TextField(max_length=800,null=True,default = None,blank=True)
    Answer = models.TextField(max_length=800,null=True,default = None,blank=True)
    Is_Answered = models.BooleanField(default=False)
    Treatment = models.ForeignKey(Treatment,on_delete=models.CASCADE,related_name="Questions")
    def __str__(self):
        return self.Question


