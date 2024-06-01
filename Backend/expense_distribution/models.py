from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Expense(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE, related_name="expenses")
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paid_expenses")
    debtors = models.ManyToManyField(User, related_name="debtors")
    date_added = models.DateTimeField(auto_now_add=True)  # can't be changed
    date_paid = models.DateTimeField(default=timezone.now)  # can be changed in the future

    @staticmethod
    def getMinimumSettlements(expenses):
        """
        Get minimum number of transactions to settle debts between users using
        Cash flow minimization algorithm.
        Efficiency: O(n*log(n))
        """
        net_amounts = {}
        for expense in expenses:
            amount_per_debtor = expense.amount / len(expense.debtors.all())
            net_amounts[expense.paid_by.id] = (
                net_amounts.get(expense.paid_by.id, 0) + expense.amount
            )  # Use User ID

            for debtor in expense.debtors.all():
                net_amounts[debtor.id] = (
                    net_amounts.get(debtor.id, 0) - amount_per_debtor
                )  # Use User ID

        balances = list(net_amounts.items())

        debtors = sorted(
            [(i, balance) for i, balance in balances if balance < 0], key=lambda x: x[1]
        )
        creditors = sorted(
            [(i, balance) for i, balance in balances if balance > 0], key=lambda x: -x[1]
        )

        debtor_index = 0
        creditor_index = 0
        transactions = []

        while debtor_index < len(debtors) and creditor_index < len(creditors):
            debtor_id, debtor_balance = debtors[debtor_index]
            creditor_id, creditor_balance = creditors[creditor_index]

            transfer_amount = min(-debtor_balance, creditor_balance)

            transactions.append(
                {
                    "payer": debtor_id,
                    "receiver": creditor_id,
                    "amount": transfer_amount,
                }  # Use User IDs
            )

            debtors[debtor_index] = (debtor_id, debtor_balance + transfer_amount)
            creditors[creditor_index] = (creditor_id, creditor_balance - transfer_amount)

            if debtors[debtor_index][1] == 0:
                debtor_index += 1
            if creditors[creditor_index][1] == 0:
                creditor_index += 1

        return transactions
