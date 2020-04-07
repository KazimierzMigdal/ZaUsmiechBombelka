from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


SEX_TAG_CHOISE = [('Boy','dla chłopca'),('Girl', 'dla dziewczynki'), ('Unisex', 'zarówno dla chłopca jaki i dziewczynki')]
AGE_TAG_CHOISE =[(1,'< 1 miesiąca'),(2,'< 3 miesiący'),(3,'< 6 miesięcy'),(4,'< 1 rok'),(5,'< 1.5 roku'),(6,'< 2 lat'),(7,'Ponad 2 lat')]


class MyAuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']

    def __init__(self, *args, **kwargs):
        super(MyAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'})
        self.fields['password'].label = False

class MyResetForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(MyResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
        self.fields['email'].label = False

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    interested_sex_tag = forms.ChoiceField(widget=forms.Select(attrs={'class':"form-control"}),label='', choices=SEX_TAG_CHOISE)
    interested_age_tag = forms.ChoiceField(widget=forms.Select(attrs={'class':"form-control"}),label='', choices=AGE_TAG_CHOISE)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.fields.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'})

        for fieldname in ['username', 'email','password1', 'password2', 'interested_sex_tag', 'interested_age_tag']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ""


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
    description = forms.CharField(label='',widget=forms.Textarea(attrs={"rows":"6", "class":"form-control"}))
    interested_sex_tag = forms.ChoiceField(widget=forms.Select(attrs={'class':"form-control-sm mx-sm-1"}), label='', choices=SEX_TAG_CHOISE)
    interested_age_tag = forms.ChoiceField(widget=forms.Select(attrs={'class':"form-control-sm mx-sm-1"}),label='', choices=AGE_TAG_CHOISE)
    sold_sex_tag = forms.ChoiceField(widget=forms.Select(attrs={'class':"form-control-sm mx-sm-1"}),label='', choices=SEX_TAG_CHOISE)
    sold_age_tag = forms.ChoiceField(widget=forms.Select(attrs={'class':"form-control-sm mx-sm-1"}),label='', choices=AGE_TAG_CHOISE)

    class Meta:
        model = Profile
        fields = ['image', 'description', 'interested_sex_tag', 'interested_age_tag', 'sold_sex_tag', 'sold_age_tag']


