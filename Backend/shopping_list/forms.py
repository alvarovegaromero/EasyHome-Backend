from django import forms
from django.core.exceptions import ValidationError

from .models import Product, ProductToBuy


class ProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} (Group: {obj.group.name}, Group ID: {obj.group.id})"


class ProductToBuyForm(forms.ModelForm):
    product = ProductChoiceField(queryset=Product.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get("product")

        if product:
            if self.instance.id:  # edit mode - exclude current instance
                if (
                    ProductToBuy.objects.filter(product=product)
                    .exclude(id=self.instance.id)
                    .exists()
                ):
                    raise ValidationError(
                        "Another active instance is referencing the same product."
                    )
            else:  # create mode
                if ProductToBuy.objects.filter(product=product).exists():
                    raise ValidationError(
                        "Another active instance is referencing the same product."
                    )

        return cleaned_data

    class Meta:
        model = ProductToBuy
        fields = ["product"]
