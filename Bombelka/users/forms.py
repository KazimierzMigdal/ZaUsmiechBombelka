from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email','password1', 'password2']:
            self.fields[fieldname].help_text = None


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', "class":"form-control"}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', "class":"form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email']:
            self.fields[fieldname].help_text = None


class ProfileUpdateForm(forms.ModelForm):
    SEX_TAG_CHOISE = [('Boy','dla chłopca'),('Girl', 'dla dziewczynki'), ('Unisex', 'zarówno dla chłopca jaki i dziewczynki')]
    AGE_TAG_CHOISE =[(1,'< 1 miesiąca'),(2,'< 3 miesiący'),(3,'< 6 miesięcy'),(4,'< 1 rok'),(5,'< 1.5 roku'),(6,'< 2 lat'),(7,'Ponad 2 lat')]

    description = forms.CharField(label='',widget=forms.Textarea(attrs={"rows":"6", "class":"form-control"}))
    interested_sex_tag = forms.ChoiceField(widget=forms.Select(attrs={'class':"form-control-sm mx-sm-1"}), label='', choices=SEX_TAG_CHOISE)
    interested_age_tag = forms.ChoiceField(widget=forms.Select(attrs={'class':"form-control-sm mx-sm-1"}),label='', choices=AGE_TAG_CHOISE)
    sold_sex_tag = forms.ChoiceField(widget=forms.Select(attrs={'class':"form-control-sm mx-sm-1"}),label='', choices=SEX_TAG_CHOISE)
    sold_age_tag = forms.ChoiceField(widget=forms.Select(attrs={'class':"form-control-sm mx-sm-1"}),label='', choices=AGE_TAG_CHOISE)

    class Meta:
        model = Profile
        fields = ['image', 'description', 'interested_sex_tag', 'interested_age_tag', 'sold_sex_tag', 'sold_age_tag']


