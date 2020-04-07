from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    text = forms.CharField(label="",widget=forms.Textarea(attrs={"rows":"2", "class":"form-control", "placeholder": "Napisz wiadomość"}))

    class Meta:
        model = Message
        fields = ('text',)
