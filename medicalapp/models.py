from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

class Feedback(models.Model):
    register = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

class Doctor(models.Model):
    doc_name = models.CharField(max_length=100, null=True, blank=True)
    doc_email = models.CharField(max_length=100, null=True, blank=True)
    doc_contact = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    hospital_name = models.CharField(max_length=100, null=True, blank=True)
    hospital_address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    qualified = models.CharField(max_length=100, null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    apt_fees = models.CharField(max_length=100, null=True, blank=True)
    abl_day = models.CharField(max_length=100, null=True, blank=True)
    abl_time = models.CharField(max_length=100, null=True, blank=True)
    treat_cond = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.doc_name

class Prediction(models.Model):
    register = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    symptoms = models.CharField(max_length=100, null=True, blank=True)
    predicted_disease = models.CharField(max_length=100, null=True, blank=True)
    dis_des = models.CharField(max_length=100, null=True, blank=True)
    my_precautions = models.CharField(max_length=100, null=True, blank=True)
    medications = models.CharField(max_length=100, null=True, blank=True)
    my_diet = models.CharField(max_length=100, null=True, blank=True)
    workout = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symptoms
