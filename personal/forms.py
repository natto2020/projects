from django import forms

class TestForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    your_name2 = forms.CharField(label='Your name', max_length=100)
