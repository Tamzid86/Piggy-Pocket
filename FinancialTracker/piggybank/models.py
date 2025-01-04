from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.core.mail import send_mail

from FinancialTracker import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
    bio = models.TextField()
    username= models.CharField(null=True, blank=True)
    email=models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user.email}"
    
    
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class TransactionHistory(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        budgets = Budget.objects.filter(user=self.user, start_date__lte=self.date, end_date__gte=self.date)
        for budget in budgets:
            budget.add_expense(self.amount)
        

    def __str__(self):
        return f"{self.amount} - {self.description} - {self.date}"
    
class FutureTransaction(models.Model):
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        description = models.CharField(max_length=255)
        date = models.DateField()
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        execute_date = models.DateField()

        def save(self, *args, **kwargs):
            if isinstance(self.execute_date, str):
                self.execute_date = datetime.strptime(self.execute_date, '%Y-%m-%d').date()
            if self.execute_date <= datetime.now().date():
                TransactionHistory.objects.create(
                    amount=self.amount,
                    description=self.description,
                    date=self.date,
                    user=self.user,
                    category=self.category
                )
            else:
                super().save(*args, **kwargs)

        def __str__(self):
            return f"{self.amount} - {self.description} - {self.execute_date}"
        
        
class Budget(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notified_80_percent = models.BooleanField(default=False)
    notified_exceeded = models.BooleanField(default=False)

    def __str__(self):
        return f"Budget for {self.user.username} from {self.start_date} to {self.end_date}"

    def add_expense(self, amount):
        self.expense += amount
        self.save()
        
        self.check_budget_percentage()
        
    def check_budget_percentage(self):
        percentage=(self.expense / self.amount)*100
        # if percentage >= 80:
        #     self.send_budget_warning_email()
        
        if not self.notified_80_percent and percentage >= 80:
            self.send_budget_warning_email()
            
        elif not self.notified_exceeded and percentage >= 100:
            self.send_budget_warning_email()
            
    def send_budget_warning_email(self):
        if not self.notified_80_percent:
            subject = f"Budget Warning for {self.user.username}"
            message = f"Hello {self.user.username},\n\nYou have used up 80% of your budget for the period {self.start_date} to {self.end_date}. Please consider reducing your expenses.\n\nRegards,\nFinancial Tracker"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [self.user.email]
            send_mail(subject, message, from_email, recipient_list)
            self.notified_80_percent = True
            self.save()
        else:
            subject = f"Budget Exceeded for {self.user.username}"
            message = f"Hello {self.user.username},\n\nYou have exceeded your budget for the period {self.start_date} to {self.end_date}. Please consider reducing your expenses.\n\nRegards,\nFinancial Tracker"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [self.user.email]
            send_mail(subject, message, from_email, recipient_list)
            self.notified_exceeded = True
            self.save()
        
        
    def create_tracker_entry(self):
            
        if Tracker.objects.filter(user=self.user, start_date=self.start_date, budget=self.amount).exists():
            print(f"Tracker entry already exists for {self.user.username} from {self.start_date} to {self.end_date}")
            return  

        
        if self.end_date <= datetime.now().date():
            days_planned = (self.end_date - self.start_date).days+1
            budget_expense_value = self.amount - self.expense
            Tracker.objects.create(
                user=self.user,
                start_date=self.start_date,
                days_planned=days_planned,
                budget=self.amount,
                budget_expense_value=budget_expense_value
            )
           
        

class Tracker(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    days_planned = models.IntegerField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    budget_expense_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Tracker for {self.user.username} from {self.start_date} for {self.days_planned} days"