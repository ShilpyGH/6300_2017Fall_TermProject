from django import forms

class VitalsForm(forms.Form):
    systolic = forms.IntegerField(label='systolic', max_value=200, min_value=0, widget=forms.TextInput(attrs={'style': 'width:100px'}))
    diastolic = forms.IntegerField(label='diastolic', max_value=200, min_value=0, widget=forms.TextInput(attrs={'style': 'width:100px'}))
    temperature = forms.IntegerField(label="temperature", widget=forms.TextInput(attrs={'style': 'width:100px'}))
    heartrate = forms.IntegerField(label="heartrate", widget=forms.TextInput(attrs={'style': 'width:100px'}))
    cancelButtonValue = forms.CharField(label="cancelButton")


class LabsForm (forms.Form):
    Labtype = forms.IntegerField(label='creatinine', max_value=200, min_value=0, widget=forms.TextInput(attrs={'style': 'width:100px'}))
    Labvalue = forms.IntegerField(label='anc_current', max_value=200, min_value=0, widget=forms.TextInput(attrs={'style': 'width:100px'}))


class Labs2Form (forms.Form):
    Ancvalue = forms.IntegerField(label='anc_current', max_value=200, min_value=0, widget=forms.TextInput(attrs={'style': 'width:100px'}))
    Serumvalue = forms.IntegerField(label='creatinine', max_value=200, min_value=0, widget=forms.TextInput(attrs={'style': 'width:100px'}))
