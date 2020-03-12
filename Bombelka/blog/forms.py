from django import forms
from .models import  Comment, Post


class CommentForm(forms.ModelForm):
    text = forms.CharField(label="",widget=forms.Textarea(attrs={"rows":"2", "class":"form-control", "placeholder": "Napisz komentarz"}))

    class Meta:
        model = Comment
        fields = ('text',)

class PostForm(forms.ModelForm):

    content = forms.CharField(label="",widget=forms.Textarea(attrs={"rows":"4", "class":"form-control"}))
    title = forms.CharField(label="",widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model = Post
        fields = ('title','content',)
