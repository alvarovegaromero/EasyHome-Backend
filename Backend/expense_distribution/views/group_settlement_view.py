from collections import defaultdict
from venv import logger

from expense_distribution.models import Expense
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class GroupSettlementView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, group_id):
        try:
            # Algoritmo de minimizacion de flujo de caja
            # Get all expenses in the group
            expenses = Expense.objects.filter(group_id=group_id)

            # Create a dictionary to hold the net amount for each user
            net_amounts = defaultdict(int)

            # Iterate over each expense
            for expense in expenses:
                # Get the amount each debtor owes for this expense
                amount_per_debtor = expense.amount / expense.debtors.count()

                # Add the amount to the payer's net amount
                net_amounts[expense.paid_by.id] += expense.amount

                # Subtract the amount from each debtor's net amount
                for debtor in expense.debtors.all():
                    net_amounts[debtor.id] -= amount_per_debtor

            # Create lists to hold the debtors and creditors
            debtors = []
            creditors = []

            # Populate the debtors and creditors lists
            for user, amount in net_amounts.items():
                if amount > 0:
                    creditors.append((user, amount))
                elif amount < 0:
                    debtors.append((user, -amount))

            # Create a list to hold the transactions
            transactions = []

            # While there are still debtors and creditors
            while debtors and creditors:
                # Get the debtor and creditor with the highest amounts
                debtor, debt = max(debtors, key=lambda x: x[1])
                creditor, credit = max(creditors, key=lambda x: x[1])

                # Calculate the transaction amount
                transaction_amount = min(debt, credit)

                # Add the transaction to the transactions list
                transactions.append(
                    {"payer": debtor, "receiver": creditor, "amount": transaction_amount}
                )

                # Update the debtor's and creditor's amounts
                if debt > credit:
                    debtors.remove((debtor, debt))
                    debtors.append((debtor, debt - transaction_amount))
                    creditors.remove((creditor, credit))
                elif debt < credit:
                    creditors.remove((creditor, credit))
                    creditors.append((creditor, credit - transaction_amount))
                    debtors.remove((debtor, debt))
                else:
                    debtors.remove((debtor, debt))
                    creditors.remove((creditor, credit))

            return Response(transactions, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during settlement retrieval: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
