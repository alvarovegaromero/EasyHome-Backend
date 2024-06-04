from decimal import ROUND_DOWN, Decimal

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
    date_paid = models.DateField(default=timezone.now().date)  # can be changed in the future

    @staticmethod
    def getMinimumSettlements(expenses):
        """
        Get minimum number of transactions to settle debts between users using
        Cash flow minimization algorithm.
        Efficiency: O(n*log(n))
        """

        net_amounts = {}
        for expense in expenses:
            debtors = list(expense.debtors.all())
            num_debtors = len(debtors)

            if num_debtors == 0:
                raise ValueError("Expense with id {} has no debtors".format(expense.id))

            total_amount = expense.amount
            net_amounts[expense.paid_by.id] = net_amounts.get(expense.paid_by.id, 0) + total_amount

            amount_per_debtor = (total_amount / num_debtors).quantize(
                Decimal("0.01"), rounding=ROUND_DOWN
            )

            for i, debtor in enumerate(debtors):
                if i < num_debtors - 1:
                    net_amounts[debtor.id] = net_amounts.get(debtor.id, 0) - amount_per_debtor
                else:  # last debtor what's remaining. Can pay 0.01 more to avoid rounding errors
                    last_debtor_amount = total_amount - amount_per_debtor * (num_debtors - 1)
                    net_amounts[debtor.id] = net_amounts.get(debtor.id, 0) - last_debtor_amount

        balances = list(net_amounts.items())

        # Sort balances in ascending order. If balance is negative, user is a debtor and vice versa
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
                    "payer": {
                        "id": debtor_id,
                        "username": User.objects.get(id=debtor_id).username,
                    },
                    "receiver": {
                        "id": creditor_id,
                        "username": User.objects.get(id=creditor_id).username,
                    },
                    "amount": "{:.2f}".format(transfer_amount),
                }
            )

            debtors[debtor_index] = (debtor_id, debtor_balance + transfer_amount)
            creditors[creditor_index] = (creditor_id, creditor_balance - transfer_amount)

            if debtors[debtor_index][1] == 0:
                debtor_index += 1
            if creditors[creditor_index][1] == 0:
                creditor_index += 1

        return transactions
