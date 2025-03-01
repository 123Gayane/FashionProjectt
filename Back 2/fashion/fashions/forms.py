from django import forms
from .models import Fashion, Contact, Trend, Outfit, Fashion2


class FashionForm(forms.ModelForm):
    class Meta:
        model = Fashion
        fields = ['name', 'description', 'size', 'color', 'quantity', 'email', 'number']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']


class FashionForm1(forms.ModelForm):
    class Meta:
        model = Trend
        fields = ['name','description', 'email', 'number']


class Fashion2Form(forms.ModelForm):
    class Meta:
        model = Fashion2
        fields = ['name', 'description', 'price']
