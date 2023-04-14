from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import *



input_css_class = "form-control"


class ProductForm(forms.ModelForm) :
    class Meta :
        model = Product
        fields = (       
            "name", "price" , "brand" , "category", "category_sex", "discound", "description" ,)
        widgets = {
                'description': forms.Textarea(attrs=({"rows":"4","cols":"20"}))
            }
class ImageForm(forms.ModelForm) :
    class Meta :
        model = Images
        fields = (
            "image",
        )
        widgets = {
                'image': forms.ClearableFileInput(attrs={'multiple': True})
            }
        

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (       
            "name", "price" , "brand" , "category", "category_sex", "discound", "description" ,)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class
class ImageUpdateForm(forms.ModelForm) :
    class Meta :
        model = Images
        fields = (
            "image",
        )
        widgets = {
                'image': forms.ClearableFileInput(attrs={'multiple': True})
            }
        
class ProductAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProductAttachment
        fields = [          
            "inventory_quantity",
            "size_number",
            "size",
            "active",
            "is_available"

        ]
        
    def clean_inventory_quantity(self) :
        inventory_quantity = self.cleaned_data.get("inventory_quantity")
        if inventory_quantity < 0 :
            forms.ValidationError("you inventory quantity is not valid")
        return inventory_quantity
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field in ['is_free', 'active']:
                continue
            self.fields[field].widget.attrs['class'] = input_css_class

ProductAttachmentModelFormSet = modelformset_factory(
    ProductAttachment,
    form=ProductAttachmentForm,
    fields = ["inventory_quantity", "size_number", "size", "color", "active"],
    extra=0,
    can_delete=True
)

ProductAttachmentInlineFormSet = inlineformset_factory(
    Product,
    ProductAttachment,
    form = ProductAttachmentForm,
    formset = ProductAttachmentModelFormSet,
    fields = ["inventory_quantity", "size_number", "color", "size", "active"],
    extra=0,
    can_delete=True
)

