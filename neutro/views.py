# from django.shortcuts import render

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader

from fhirclient import client

import datetime
from dateutil.relativedelta import relativedelta

import fhirclient.models.patient as p

import fhirclient.models.observation as obs
import fhirclient.models.condition as c

import fhirclient.models.medicationadministration as m
from datetime import datetime
from dateutil.relativedelta import relativedelta

from .forms import VitalsForm
from .forms import Labs2Form
from .forms import LabsForm

from neutro.models import Patient as PatientModel
from neutro.models import PatientVitals as PatientVitalsModel
from neutro.models import PatientLabs2 as PatientLabs2Model
from neutro.models import PatientLabs as PatientLabsModel

# from neutro.models import PatientTempNeutro as PatientTempNeutroModel

MASCC_score = 0
penicillin_allergy = False

def index(request):
    patientId = 'cf-1508345037261'
    errorMessage = ""

    settings = {
        'app_id': 'my_web_app',
        'api_base': 'https://fhirtest.uhn.ca/baseDstu3'
    }
    smart = client.FHIRClient(settings=settings)
    patient = p.Patient.read(patientId, smart.server)

    firstName = patient.name[0].given[0]
    middleName = patient.name[0].given[1]
    familyName = patient.name[0].family
    dob = patient.birthDate.isostring
    dob2 = datetime.strptime(dob, '%Y-%m-%d')
    gender = patient.gender
    now = datetime.today()

    rdelta = relativedelta(now, dob2)
    age = rdelta.years

    # Data for MASCC score
    age_score = 2
    if age >= 60:
        age_score = 0

    # spb_score
    sbp_score = 5
    search = obs.Observation.where(struct={'patient': "cf-1508345037261", 'code': "8480-6"})
    sbp = search.perform_resources(smart.server)
    if sbp:
        sbp_value = sbp[0].valueQuantity.value
        sbp_units = sbp[0].valueQuantity.unit
    if sbp_value <= 90:
        sbp_score = 0

    # Identify patient medication
    smart = client.FHIRClient(settings=settings)
    search = m.MedicationAdministration.where(struct={'patient': "cf-1508345037261"})
    medications = search.perform_resources(smart.server)

    # Determine if Patient Recieved Saline IV Fluids and Calculate Saline_score
    saline_score = 3
    for medication in medications:
        if 'saline' in medication.medicationCodeableConcept.coding[0].display.lower():
            saline_score = 0

    # Identify Patient Conditions
    smart = client.FHIRClient(settings=settings)
    search = c.Condition.where(struct={'patient': "cf-1508345037261"})
    conditions = search.perform_resources(smart.server)

    # Determine if Patient has COPD, Fungemia, Hematologic Malignancies, Sepsis
    COPD_score = 4
    sepsis_score = 5
    cancer_score = 4
    hematologic_malignancy = 0
    fungemia = 0
    for condition in conditions:
        if 'chronic obstructive pulmonary disease' in condition.code.coding[0].display.lower():
            COPD_score = 0
        if 'sepsis' in condition.code.coding[0].display.lower():
            sepsis_score = 0
        if 'fungemia' in condition.code.coding[0].display.lower():
            fungemia = 1
        if 'leukemia' in condition.code.coding[0].display.lower():
            hematologic_malignancy = 1

    if hematologic_malignancy == 1 and fungemia == 1:
        cancer_score = 0

    # Calculator
    # The expected Score is a MASCC Score of 5, High Risk Patient
    MASCC_score = 0
    MASCC_score = age_score + sbp_score + saline_score + COPD_score + sepsis_score + cancer_score

    MASCC_score = 22

    observation = {}

    patient = {}
    patient['firstName'] = firstName
    patient['middleName'] = middleName
    patient['familyName'] = familyName
    patient['gender'] = gender
    patient['dob'] = dob
    patient['age'] = age
    patient['id'] = patientId
    patient['condition'] = conditions  # this is a list of conditions
    patient['sbp'] = sbp_value

    form = VitalsForm()


    if request.method == 'POST':
        form = VitalsForm(request.POST)
        if form.is_valid():
            patientLinkage = PatientModel.objects.get(patientID=patientId)
            # where does the data for temperature and anc coming from? is it from forms.py
            tempObj = PatientVitalsModel(patientID=patientLinkage, temperature=form.cleaned_data["temperature"],
                                         systolic=form.cleaned_data["systolic"],
                                         diastolic=form.cleaned_data["diastolic"],
                                         heartrate=form.cleaned_data["heartrate"], )
            tempObj.save()
            # return redirect("https://www.djangoproject.com")

            if form.cleaned_data['cancelButtonValue'] == 'true':
                return render(request, 'proceed.html',
                          {'form': form, 'patient': patient, 'observation': observation, 'errorMessage': errorMessage,
                           'masscore': MASCC_score, })

            elif MASCC_score < 21:
                return render(request, 'cpoehigh.html',
                          {'form': form, 'patient': patient, 'observation': observation, 'errorMessage': errorMessage,
                           'masscore': MASCC_score, })
            else:
                return render(request, 'cpoe.html',
                          {'form': form, 'patient': patient, 'observation': observation, 'errorMessage': errorMessage,
                           'masscore': MASCC_score, })

        else:
            errorMessage = "Values are incorrect"



    return render(request, 'index.html',
                  {'form': form, 'patient': patient, 'observation': observation, 'errorMessage': errorMessage, 'masscore':MASCC_score,})

def checkTempAnc(request):
    patientId = 'cf-1508345037261'
    errorMessage = ""
    if request.method == 'POST':
        form = VitalsForm(request.POST)

    settings = {
        'app_id': 'my_web_app',
        'api_base': 'https://fhirtest.uhn.ca/baseDstu3'
    }
    smart = client.FHIRClient(settings=settings)
    patient = p.Patient.read(patientId, smart.server)

    observation = {}

    temp = request.POST['temperature']
    neutro = request.POST['anc_count']
    if temp > 101 and neutro < 500:
        return render(request, 'MASCC.html.html',
                      {'form': form, 'patient': patient, 'observation': observation, 'errorMessage': errorMessage})
    return render(request, 'proceed.html',
                  {'form': form, 'patient': patient, 'observation': observation, 'errorMessage': errorMessage})

def labEntry(request):
    patientId = 'cf-1508345037261'
    errorMessage = ""
    if request.method == 'POST':
        form = Labs2Form(request.POST)
        patientLinkage = PatientModel.objects.get(patientID=patientId)
        tempObj = PatientVitalsModel(patientID=patientLinkage,
                                         Ancvalue=form.cleaned_data["anc_current"],
                                         Serumvalue=form.cleaned_data["creatinine"], )
        tempObj.save()

    settings = {
        'app_id': 'my_web_app',
        'api_base': 'https://fhirtest.uhn.ca/baseDstu3'
    }
    smart = client.FHIRClient(settings=settings)
    patient = p.Patient.read(patientId, smart.server)

    firstName = patient.name[0].given[0]
    middleName = patient.name[0].given[1]
    familyName = patient.name[0].family
    dob = patient.birthDate.isostring
    dob2 = datetime.strptime(dob, '%Y-%m-%d')
    gender = patient.gender
    now = datetime.today()

    rdelta = relativedelta(now, dob2)
    age = rdelta.years

    observation = {}

    patient = {}
    patient['firstName'] = firstName
    patient['middleName'] = middleName
    patient['familyName'] = familyName
    patient['gender'] = gender
    patient['dob'] = dob
    patient['age'] = age
    patient['id'] = patientId

    patientVitals = PatientVitalsModel.objects.only('temperature').filter(patientID=PatientModel.objects.get(patientID=patientId)).order_by('datetime')
    #print( list(patientVitals.last()) )

    temperature=100
    patient['temperature'] =100

    form = Labs2Form()
    #print(temperature[0:1])
    return render(request, 'labEntry.html',
                  {'form': form, 'patient': patient, 'observation': observation, 'errorMessage': errorMessage, })

def MASCC(request):
    '''a = 1 '''
    patientId = 'cf-1508345037261'
    errorMessage = ""

    settings = {
        'app_id': 'my_web_app',
        'api_base': 'https://fhirtest.uhn.ca/baseDstu3'
    }
    smart = client.FHIRClient(settings=settings)
    patient = p.Patient.read(patientId, smart.server)

    firstName = patient.name[0].given[0]
    middleName = patient.name[0].given[1]
    familyName = patient.name[0].family
    dob = patient.birthDate.isostring
    dob2 = datetime.strptime(dob, '%Y-%m-%d')
    gender = patient.gender
    now = datetime.today()

    rdelta = relativedelta(now, dob2)
    age = rdelta.years

    search = obs.Observation.where(struct={'patient': "cf-1508345037261", 'code': "8480-6"})
    sbp = search.perform_resources(smart.server)
    if sbp:
        sbp_value = sbp[0].valueQuantity.value

    # firstName = 'John  '
    # middleName = 'Edmund'
    # familyName = 'Smit'
    # dob = '1953-05-05'
    # dob2 = '1953-05-05'
    # gender = 'Male'
    # # now = datetime.today()
    #
    # # rdelta=relativedelta(now,dob2)
    # age='60'

    patient = {}
    patient['firstName'] = firstName
    patient['middleName'] = middleName
    patient['familyName'] = familyName
    patient['gender'] = gender
    patient['dob'] = dob
    patient['age'] = age
    patient['id'] = patientId
    patient['sbp'] = sbp_value

    form = VitalsForm()

    return render(request, 'MASCC.html',
                  {'form': '', 'patient': patient, 'observation': '', 'errorMessage': errorMessage,
                    })

def proceed(request):
    patientId = 'cf-1507833566732'

    errorMessage = ""
    settings = {
        'app_id': 'my_web_app',
        'api_base': 'https://fhirtest.uhn.ca/baseDstu3'
    }
    smart = client.FHIRClient(settings=settings)
    patient = p.Patient.read(patientId, smart.server)

    firstName = patient.name[0].given[0]
    middleName = patient.name[0].given[1]
    familyName = patient.name[0].family
    dob = patient.birthDate.isostring
    dob2 = datetime.strptime(dob, '%Y-%m-%d')
    gender = patient.gender
    now = datetime.today()

    rdelta = relativedelta(now, dob2)
    age = rdelta.years

    patient = {}
    patient['firstName'] = firstName
    patient['middleName'] = middleName
    patient['familyName'] = familyName
    patient['gender'] = gender
    patient['dob'] = dob
    patient['age'] = age
    patient['id'] = patientId

    return render(request, 'proceed.html',
                  {'form': '', 'patient': patient, 'observation': '', 'errorMessage': errorMessage, })

def cpoe(request):
    patientId = 'cf-1507833566732'

    errorMessage = ""
    settings = {
        'app_id': 'my_web_app',
        'api_base': 'https://fhirtest.uhn.ca/baseDstu3'
    }
    smart = client.FHIRClient(settings=settings)
    patient = p.Patient.read(patientId, smart.server)

    firstName = patient.name[0].given[0]
    middleName = patient.name[0].given[1]
    familyName = patient.name[0].family
    dob = patient.birthDate.isostring
    dob2 = datetime.strptime(dob, '%Y-%m-%d')
    gender = patient.gender
    now = datetime.today()

    rdelta = relativedelta(now, dob2)
    age = rdelta.years

    patient = {}
    patient['firstName'] = firstName
    patient['middleName'] = middleName
    patient['familyName'] = familyName
    patient['gender'] = gender
    patient['dob'] = dob
    patient['age'] = age
    patient['id'] = patientId

def infobutton(request):
    # template = loader.get_template('infobutton.html')
    # return HttpResponse(template.render(patient, request))
    return

def chooseAntibiotics():
    medication = []
    rxNorm = []
    MRSA_status = False
    vanco_resistance = False
    hypo_tension = False
    pneumonia = False
    renal_function = 1  # 1=normal, 0=abnormal

    if MASCC_score >= 21:  # low risk, outpatient, oral antibiotics
        if penicillin_allergy == True:
            medication.append("Ciprofloxacin", "Amoxicillin-Clavulanate")
            rxNorm.append("2551", "19711")
        else:
            medication.append("Ciprofloxacin", "Clindamycin")
            rxNorm.append("2551", "2582")

    if MASCC_score < 21:  # high risk, in-patient, IV antibiotics
        if hypo_tension == True or pneumonia == True:
            medication.append("Ciprofloxacin/Fluocinolone")
            rxNorm.append("1792385")
        elif MRSA_status == True:
            if vanco_resistance == True:
                medication.append("Linezolid")
                rxNorm.append("190376")
            else:
                medication.append("Vancomycin")
                rxNorm.append("313572")
        elif penicillin_allergy == True:
            if vanco_resistance == False:
                medication.append("Aztreonam", "Vancomycin")
                rxNorm.append("1272", "313572")
            else:
                medication.append("Ciprofloxacin", "Clindamycin")
                rxNorm.append("2551", "2582")
        elif penicillin_allergy == False:
            medication.append("Meropenem")
            rxNorm.append("29561")




def getPatient(patientId):
        settings = {
            'app_id': 'my_web_app',
            'api_base': 'https://fhirtest.uhn.ca/baseDstu3'
        }

        try:
            smart = client.FHIRClient(settings=settings)
            patient = p.Patient.read(patientId, smart.server)

            first_name = patient.name[0].given[0]
            family_name = patient.name[0].family
            dob = patient.birthDate.isostring
            dob2 = datetime.datetime.strptime(dob, '%Y-%m-%d')
            gender = patient.gender
            now = datetime.datetime.today()
            rdelta = relativedelta(now, dob2)
            age = rdelta.years

        except:
            first_name = 'Captain'
            family_name = 'America'
            gender = 'Male'
            dob = '1920-07-04'
            dob2 = datetime.strptime(dob, '%Y-%m-%d')
            age = relativedelta(datetime.today(), dob2).years

        patient = {}
        patient['first_name'] = first_name
        patient['family_name'] = family_name
        patient['gender'] = gender
        patient['dob'] = dob
        patient['age'] = age
        patient['id'] = patientId
        patient['vitals'] = PatientVitalsModel.objects.filter(patientID=PatientModel.objects.get(patientID=patientId))

        return patient