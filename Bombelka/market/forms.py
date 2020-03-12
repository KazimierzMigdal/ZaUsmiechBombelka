from django import forms
from .models import Product


class ProductCreationForm(forms.ModelForm):

    class Meta:
        model = Product
        helper.form_show_labels = False
        fields = ['title', 'description', 'photo_1', 'photo_2', 'photo_3', 'tag_age', 'tag_sex']

    def __init__(self, *args, **kwargs):
        self.helper.form_show_labels = False
        self.
        super(ProductCreationForm, self).__init__(*args, **kwargs)


        for fieldname in ['title', 'description','photo_1', 'photo_2', 'photo_3', 'tag_age', 'tag_sex']:
            # self.fields[fieldname].help_text = None
            self.fields[fieldname].label = ''

