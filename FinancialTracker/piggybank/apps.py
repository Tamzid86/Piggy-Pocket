from django.apps import AppConfig
import threading
import time
from datetime import datetime


def process_future_transactions():
    while True:
        try:
            from piggybank.models import FutureTransaction, TransactionHistory

            today = datetime.now().date()

            future_transactions = FutureTransaction.objects.filter(execute_date__lte=today)

            for transaction in future_transactions:
                TransactionHistory.objects.create(
                    amount=transaction.amount,
                    description=transaction.description,
                    date=transaction.date,
                    user=transaction.user,
                    category=transaction.category
                )
                transaction.delete()

            print(f"Processed and deleted {future_transactions.count()} future transactions and today is {today}")
        except Exception as e:
            print(f"Error processing future transactions: {e}")

        time.sleep(24 * 60 * 60)


def process_budget_tracker():
    while True:
        try:
            from piggybank.models import Budget

            budgets = Budget.objects.filter(end_date__lte=datetime.now().date())

            for budget in budgets:
                budget.create_tracker_entry()

            print(f"Tracker is tracking properly")
        except Exception as e:
            print(f"Error processing budgets: {e}")

        time.sleep(24 * 60 * 60)





class PiggybankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'piggybank'

    def ready(self):
        threading.Thread(target=process_future_transactions, daemon=True).start()
        threading.Thread(target=process_budget_tracker, daemon=True).start()