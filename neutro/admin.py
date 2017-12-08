from django.contrib import admin

from .models import Patient, PatientLabs, PatientVitals, PatientLabs2

admin.site.register(Patient)
admin.site.register(PatientLabs)
admin.site.register(PatientLabs2)
admin.site.register(PatientVitals)