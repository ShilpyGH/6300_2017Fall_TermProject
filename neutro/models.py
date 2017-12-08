from django.db import models
from datetime import date, datetime

class Patient(models.Model):
	patientID = models.CharField(max_length=200)
	def __str__(self):
		return self.patientID

class PatientLabs(models.Model):
	patientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
	datetime = models.DateTimeField(default=datetime.now)
	labtype = models.CharField(max_length=250,default=0)
	labvalue = models.FloatField(default=0)

class PatientLabs2(models.Model):
	patientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
	datetime = models.DateTimeField(default=datetime.now)
	ancvalue = models.FloatField(default=0)
	serumvalue = models.FloatField(default=0)

class PatientVitals(models.Model):
	patientID = models.ForeignKey(Patient, on_delete=models.CASCADE)
	datetime = models.DateTimeField(default=datetime.now)
	systolic = models.IntegerField(default=0)
	diastolic = models.IntegerField(default=0)
	heartrate = models.IntegerField(default=0)
	temperature = models.FloatField(default=0)



