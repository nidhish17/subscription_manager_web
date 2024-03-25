from django.forms import ModelForm
from .models import Category, Channel
from django import forms


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category Name"})
        }


# class ChannelForm(ModelForm):
#     class Meta:
#         model = Channel
#         fields = ["category"]
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop("user")
#         super(ChannelForm, self).__init__(*args, **kwargs)
#         self.fields['category'].queryset = Category.objects.filter(user_profile=user)
#         self.fields['category'].widget.attrs.update({'class': 'my_dropdown'})

class ChannelCategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label="Select Category",
                                      widget=forms.Select(attrs={"class": "form-select select-custom-style"}))

    # filter the categories that the user has
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ChannelCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user_profile=user)
