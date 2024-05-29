from django import forms

from .models import Expense, UserGroup

# from django.core.exceptions import ValidationError


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        group = cleaned_data.get("group")
        paid_by = cleaned_data.get("paid_by")
        debtors = cleaned_data.get("debtors")

        if paid_by and group and not UserGroup.objects.filter(user=paid_by, group=group).exists():
            self.add_error("paid_by", "The user who paid must be in the same group.")

        if debtors and group:
            for debtor in debtors:
                if not UserGroup.objects.filter(user=debtor, group=group).exists():
                    self.add_error("debtors", "All debtors must be in the same group.")

        return cleaned_data
